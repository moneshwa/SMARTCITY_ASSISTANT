import json
from pathlib import Path
from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel

# Define the structure of the feedback data we expect
class Feedback(BaseModel):
    name: str
    category: str
    message: str

router = APIRouter()

# Define the path for our log file
DATA_DIR = Path("app/data")
FEEDBACK_FILE = DATA_DIR / "feedback_log.json"

# Ensure the data directory exists
DATA_DIR.mkdir(exist_ok=True)

@router.post("/submit-feedback", tags=["Citizen Feedback"])
async def submit_feedback(feedback: Feedback):
    """
    Receives feedback from the user and appends it to a JSON file.
    """
    # Create a new record with a timestamp
    new_record = {
        "timestamp": datetime.now().isoformat(),
        "user": feedback.name,
        "category": feedback.category,
        "message": feedback.message,
    }

    # Read existing data, append new record, and write back
    try:
        if FEEDBACK_FILE.exists():
            with open(FEEDBACK_FILE, "r+") as f:
                data = json.load(f)
                data.append(new_record)
                f.seek(0)
                json.dump(data, f, indent=4)
        else:
            with open(FEEDBACK_FILE, "w") as f:
                json.dump([new_record], f, indent=4)
        
        return {"status": "success", "message": "Feedback submitted successfully."}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
