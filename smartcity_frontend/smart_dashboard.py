import streamlit as st
import pandas as pd
from api_client import * # Import all functions
from streamlit_option_menu import option_menu # Import the new menu

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="Smart City Assistant", page_icon="🏙️", layout="wide")
local_css("styles/style.css")

# --- NEW SIDEBAR LAYOUT using streamlit-option-menu ---
with st.sidebar:
    selected_page = option_menu(
        menu_title="Smart City Assistant",  # Main title
        options=["Summarizer", "Feedback", "Documents", "Chat", "Forecasting", "Anomalies"], # Page names
        icons=['text-paragraph', 'chat-quote-fill', 'file-earmark-text', 'chat-dots-fill', 'bar-chart-line', 'exclamation-triangle'],  # Bootstrap icons
        menu_icon="cast",  # Main icon
        default_index=0,  # Default page
        styles={
            "container": {"padding": "0!important", "background-color": "#0E1117"},
            "icon": {"color": "white", "font-size": "20px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#4A4A6A"},
            "nav-link-selected": {"background-color": "#4A4A6A"},
        }
    )

st.title("Sustainable Smart City Assistant")

# --- Page Content (The logic is the same, but the page names are updated) ---
if selected_page == "Summarizer":
    st.header("Policy Summarizer")
    policy_text = st.text_area("Paste policy text:", height=200, label_visibility="collapsed")
    if st.button("Generate Summary"):
        if policy_text:
            with st.spinner("Summarizing..."):
                summary = get_summary_from_backend(policy_text)
                if summary: st.write(summary)
        else: st.warning("Please paste some policy text.")

elif selected_page == "Feedback":
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

elif selected_page == "Documents":
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

elif selected_page == "Chat":
    st.header("Chat Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    if prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        with st.spinner("Thinking..."):
            response = get_chat_response_from_backend(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)

elif selected_page == "Forecasting":
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

elif selected_page == "Anomalies":
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