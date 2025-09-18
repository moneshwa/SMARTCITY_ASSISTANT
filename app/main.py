from fastapi import FastAPI
# This is the corrected import statement
from app.api.policy_router import router as policy_router
from app.api.feedback_router import router as feedback_router  # <-- ADD THIS
from app.api.vector_router import router as vector_router # <-- ADD THIS

app = FastAPI(title="Sustainable Smart City Assistant API")

# Now this line will work correctly
app.include_router(policy_router, prefix="/policy")
app.include_router(feedback_router, prefix="/feedback")  # <-- AND THIS
app.include_router(vector_router, prefix="/vectors") # <-- AND THIS

@app.get("/")
def read_root():
    return {"message": "Welcome to the Smart City Assistant API"}