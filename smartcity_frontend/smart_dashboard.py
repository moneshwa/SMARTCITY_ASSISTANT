import streamlit as st
import pandas as pd
from api_client import (
    get_summary_from_backend,
    submit_feedback_to_backend,
    upload_document_to_backend,
    search_documents_in_backend,
    get_chat_response_from_backend,
    get_forecast_from_backend,
    get_anomalies_from_backend
)

# Function to load a local CSS file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Page Configuration ---
st.set_page_config(
    page_title="Smart City Assistant",
    page_icon="🏙️",
    layout="wide"
)
local_css("styles/style.css")

# --- Sidebar Navigation ---
with st.sidebar:
    st.header("Navigation")
    # Add the final pages to the options
    selected_page = st.radio(
        "Go to",
        ["Policy Summarizer", "Citizen Feedback", "Document Management", "Chat Assistant", "KPI Forecasting", "Anomaly Detection"],
        label_visibility="collapsed"
    )
    st.sidebar.image("https://images.pexels.com/photos/325185/pexels-photo-325185.jpeg", use_container_width=True)

# --- Main App Title ---
st.title("Sustainable Smart City Assistant")

# --- Page Content ---
if selected_page == "Policy Summarizer":
    st.header("Policy Summarizer")
    policy_text = st.text_area("Paste the policy text you want to summarize:", height=200, label_visibility="collapsed")
    if st.button("Generate Summary"):
        if policy_text:
            with st.spinner("Summarizing..."):
                summary = get_summary_from_backend(policy_text)
                if summary:
                    st.subheader("Summary:")
                    st.write(summary)
        else:
            st.warning("Please paste some policy text to summarize.")

elif selected_page == "Citizen Feedback":
    st.header("Submit Your Feedback or Report an Issue")
    
    # Create a form for feedback submission
    with st.form("feedback_form"):
        name = st.text_input("Your Name")
        category = st.selectbox(
            "Type of Issue",
            ["Garbage", "Water Supply", "Street Lights", "Public Transport", "Other"]
        )
        message = st.text_area("Describe the issue or suggestion")
        
        # Submit button for the form
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            if name and message:
                with st.spinner("Submitting..."):
                    success = submit_feedback_to_backend(name, category, message)
                    if success:
                        st.success("Thank you! Your feedback has been submitted.")
                    else:
                        st.error("There was an issue submitting your feedback.")
            else:
                st.warning("Please fill out your name and a message.")

elif selected_page == "Document Management":
    st.header("Upload Policy Documents for Semantic Search 📤")
    st.write("Upload a .txt file containing a city policy or document. It will be processed and stored for future searches.")
    
    uploaded_file = st.file_uploader("Choose a .txt file", type="txt")
    
    if uploaded_file is not None:
        st.info(f"File selected: {uploaded_file.name}")
        if st.button("Process and Upload Document"):
            with st.spinner("Processing document... This may take a moment."):
                upload_document_to_backend(uploaded_file)
    
    # --- Search Section ---
    st.divider()
    st.header("Search Uploaded Documents")
    search_query = st.text_input("Enter your question or keyword to search")
    
    if st.button("Search"):
        if search_query:
            with st.spinner("Searching..."):
                results = search_documents_in_backend(search_query)
                if results:
                    st.subheader("Search Results:")
                    for result in results:
                        with st.container(border=True):
                            st.write(result['text'])
                            st.caption(f"Relevance Score: {result['score']:.4f}")
                else:
                    st.warning("No results found or an error occurred.")
        else:
            st.warning("Please enter a search query.")

# --- ADD THIS NEW PAGE ---
elif selected_page == "Chat Assistant":
    st.header("Chat with the Smart City Assistant")

    # Initialize chat history in session state if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How can I help you with the smart city today?"}]

    # Display past messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Get user input using the chat input widget
    if prompt := st.chat_input("What is up?"):
        # Add user message to history and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_chat_response_from_backend(prompt)
                st.markdown(response)
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- ADD THESE FINAL TWO PAGES ---
elif selected_page == "KPI Forecasting":
    st.header("📈 Key Performance Indicator Forecasting")
    st.write("Upload a CSV file with historical data to predict the next year's value.")
    
    uploaded_csv = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_csv is not None:
        kpi_column = st.text_input("Enter the name of the column to forecast (e.g., 'energy', 'water_usage')")
        if st.button("Forecast Next Year"):
            if kpi_column:
                with st.spinner("Calculating forecast..."):
                    result = get_forecast_from_backend(uploaded_csv, kpi_column)
                    if result:
                        st.success(f"Forecast for '{result['kpi']}' in {result['predicted_year']}: **{result['predicted_value']}**")
            else:
                st.warning("Please enter the column name.")

elif selected_page == "Anomaly Detection":
    st.header("⚠️ Anomaly Detection")
    st.write("Upload a CSV file to check for anomalies based on a threshold value.")
    
    uploaded_csv = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_csv is not None:
        df = pd.read_csv(uploaded_csv)
        st.write("Data Preview:")
        st.dataframe(df.head())
        
        kpi_column = st.selectbox("Select the column to check for anomalies", df.columns)
        threshold = st.number_input("Set the threshold value (records above this will be flagged)", value=1000.0)
        
        if st.button("Check for Anomalies"):
            # Reset file read position for API call
            uploaded_csv.seek(0)
            with st.spinner("Checking..."):
                result = get_anomalies_from_backend(uploaded_csv, kpi_column, threshold)
                if result:
                    st.success(f"Found **{result['anomaly_count']}** anomalies.")
                    if result['anomalies']:
                        st.write("Anomalous Records:")
                        st.dataframe(pd.DataFrame(result['anomalies']))
