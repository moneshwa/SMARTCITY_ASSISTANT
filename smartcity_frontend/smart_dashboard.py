import streamlit as st
from api_client import (
    get_summary_from_backend,
    submit_feedback_to_backend,
    upload_document_to_backend,
    search_documents_in_backend,
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
    selected_page = st.radio(
        "Go to",
        ["Policy Summarizer", "Citizen Feedback", "Document Management"],
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
