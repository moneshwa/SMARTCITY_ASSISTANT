import requests
import streamlit as st

# The base URL of your running FastAPI backend
API_BASE_URL = "http://127.0.0.1:8000"

def get_summary_from_backend(text: str) -> str:
    """
    Sends text to the backend's summarize-policy endpoint and returns the summary.
    """
    try:
        url = f"{API_BASE_URL}/policy/summarize-policy"
        payload = {"text": text}
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            return response.json().get("summary", "Could not parse summary.")
        else:
            st.error(f"Error from API: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the backend API: {e}")
        return None

def submit_feedback_to_backend(name: str, category: str, message: str) -> bool:
    """
    Sends feedback data to the backend and returns True on success.
    """
    try:
        url = f"{API_BASE_URL}/feedback/submit-feedback"
        payload = {"name": name, "category": category, "message": message}
        response = requests.post(url, json=payload)

        if response.status_code == 200 and response.json().get("status") == "success":
            return True
        else:
            st.error(f"Error submitting feedback: {response.status_code} - {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the backend API: {e}")
        return False

def upload_document_to_backend(uploaded_file):
    """Sends a .txt file to the backend for embedding and returns the response."""
    try:
        url = f"{API_BASE_URL}/vectors/upload-document"
        # Prepare the file for the POST request
        files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        response = requests.post(url, files=files)
        
        if response.status_code == 200:
            st.success(response.json().get("message", "File processed successfully."))
            return True
        else:
            st.error(f"Error uploading file: {response.status_code} - {response.json().get('detail')}")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the backend API: {e}")
        return False

def search_documents_in_backend(query: str):
    """Sends a search query to the backend and returns the results."""
    try:
        url = f"{API_BASE_URL}/vectors/search-documents"
        payload = {"query": query}
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            st.error(f"Error during search: {response.status_code} - {response.json().get('detail')}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the backend API: {e}")
        return []
