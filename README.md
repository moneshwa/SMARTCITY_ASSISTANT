# Sustainable Smart City Assistant

## Overview
The Sustainable Smart City Assistant is an AI-powered platform that uses IBM's Granite LLM (via Hugging Face) to support urban sustainability, governance, and citizen engagement. It integrates modules for policy summarization, KPI forecasting, anomaly detection, and a citizen chat assistant.

## Features
* **AI Policy Summarizer:** Simplifies complex city policies into easy-to-understand summaries.
* **KPI Forecasting:** Uses machine learning to predict future city metrics (e.g., energy usage) based on historical data.
* **Anomaly Detection:** Scans datasets to identify unusual data points that may indicate infrastructure issues.
* **Citizen Feedback:** A simple form for residents to report issues directly to the city.
* **Interactive Chat Assistant:** A conversational AI to answer questions about sustainability and city services.
* **Document Management:** Allows for uploading and performing semantic search on policy documents.

## Architecture
The project is built with a modern tech stack:
* **Frontend:** Streamlit
* **Backend:** FastAPI
* **AI Model:** IBM Granite LLM from Hugging Face Hub
* **Framework:** LangChain
* **Vector Database:** Pinecone
* **Data Analysis:** Pandas & Scikit-learn

## How to Run the Project

Follow these steps to set up and run the project locally:

**1. Clone the repository:**
   ```bash
   git clone [your-github-repository-url]
   cd [your-repository-name]
