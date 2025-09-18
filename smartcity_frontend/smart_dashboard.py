import streamlit as st
import pandas as pd
from api_client import * # Import all functions

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="Smart City Assistant", page_icon="🏙️", layout="wide")
local_css("styles/style.css")

# --- NEW SIDEBAR LAYOUT ---
with st.sidebar:
    st.header("Navigation")
    selected_page = st.radio(
        "Go to",
        ["Policy Summarizer", "Citizen Feedback", "Document Management", "Chat Assistant", "KPI Forecasting", "Anomaly Detection"],
        label_visibility="collapsed"
    )
    
    # Add a visual separator
    st.divider()

    # Add a new section at the bottom
    st.header("Help")
    st.info("This is a demo project for Naan Mudhalvan. Select a feature above to get started.")
    # The st.sidebar.image line has been removed

st.title("Sustainable Smart City Assistant")

# --- Page Content (The rest of the code is unchanged) ---
if selected_page == "Policy Summarizer":
    st.header("Policy Summarizer")
    policy_text = st.text_area("Paste policy text:", height=200, label_visibility="collapsed")
    if st.button("Generate Summary"):
        if policy_text:
            with st.spinner("Summarizing..."):
                summary = get_summary_from_backend(policy_text)
                if summary: st.write(summary)
        else: st.warning("Please paste some policy text.")

elif selected_page == "Citizen Feedback":
    st.header("Submit Your Feedback")
    with st.form("feedback_form"):
        name = st.text_input("Your Name")
        category = st.selectbox("Type of Issue", ["Garbage", "Water", "Lights", "Other"])
        message = st.text_area("Describe the issue")
        if st.form_submit_button("Submit"):
            if name and message:
                if submit_feedback_to_backend(name, category, message):
                    st.success("Feedback submitted!")
            else: st.warning("Please fill out all fields.")

elif selected_page == "Document Management":
    st.header("Upload & Search Documents")
    uploaded_file = st.file_uploader("Upload a .txt policy document", type="txt")
    if uploaded_file:
        if st.button("Process and Upload"):
            with st.spinner("Processing..."):
                upload_document_to_backend(uploaded_file)
    st.divider()
    st.header("Search Documents")
    search_query = st.text_input("Enter search query")
    if st.button("Search"):
        if search_query:
            with st.spinner("Searching..."):
                results = search_documents_in_backend(search_query)
                if results:
                    for r in results:
                        with st.container(border=True):
                            st.write(r['text'])
                            st.caption(f"Relevance: {r['score']:.4f}")
                else: st.warning("No results found.")
        else: st.warning("Please enter a query.")

elif selected_page == "Chat Assistant":
    st.header("Chat Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        with st.spinner("Thinking..."):
            response = get_chat_response_from_backend(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)

elif selected_page == "KPI Forecasting":
    st.header("📈 Key Performance Indicator Forecasting")
    uploaded_csv = st.file_uploader("Choose a CSV file with a 'year' column", type="csv")
    if uploaded_csv is not None:
        kpi_column = st.text_input("Enter the name of the column to forecast (e.g., 'energy')")
        if st.button("Forecast Next Year"):
            if kpi_column:
                with st.spinner("Calculating forecast..."):
                    result = get_forecast_from_backend(uploaded_csv, kpi_column)
                    if result:
                        st.success(f"Forecast for '{result['kpi']}' in {result['predicted_year']}: **{result['predicted_value']}**")
            else: st.warning("Please enter the column name.")

elif selected_page == "Anomaly Detection":
    st.header("⚠️ Anomaly Detection")
    uploaded_csv = st.file_uploader("Choose a CSV file to check for anomalies", type="csv")
    if uploaded_csv is not None:
        df = pd.read_csv(uploaded_csv)
        st.write("Data Preview:")
        st.dataframe(df.head())
        kpi_column = st.selectbox("Select the column to check", df.columns)
        threshold = st.number_input("Set the threshold value", value=1000.0)
        if st.button("Check for Anomalies"):
            uploaded_csv.seek(0)
            with st.spinner("Checking..."):
                result = get_anomalies_from_backend(uploaded_csv, kpi_column, threshold)
                if result:
                    st.success(f"Found **{result['anomaly_count']}** anomalies.")
                    if result['anomalies']:
                        st.write("Anomalous Records:")
                        st.dataframe(pd.DataFrame(result['anomalies']))