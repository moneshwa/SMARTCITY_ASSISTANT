import os
import traceback
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Check for the GOOGLE_API_KEY
if not os.getenv("GOOGLE_API_KEY"):
    raise EnvironmentError("GOOGLE_API_KEY not found in .env file")

# Initialize the Google Gemini model with the correct, official name
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")

def ask_llm(prompt_text: str) -> str:
    """
    A simple function to send a prompt to the LLM and get a response.
    """
    try:
        response = llm.invoke(prompt_text)
        return response.content
    except Exception as e:
        print("--- AN ERROR OCCURRED ---")
        traceback.print_exc()
        print("-------------------------")
        return "Sorry, I ran into an error while trying to respond."