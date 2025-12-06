# backend/app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from app.database import engine, Base
from app.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION
)

# Configure CORS (allow frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== DATA MODELS ==========

# Model for assessment request
class AssessmentRequest(BaseModel):
    answers: List[str]  # List of 'yes', 'no', 'unsure' answers

# Model for assessment response
class AssessmentResponse(BaseModel):
    result: str
    remedies: List[str]
    severity: str

# Model for disorder info
class DisorderResponse(BaseModel):
    id: int
    name: str
    description: str
    remedies: List[str]

# ========== IN-MEMORY DATA ==========

# Sample disorders data (in real app, this would come from database)
DISORDERS_DATA = {
    1: {
        "name": "Depression",
        "description": "A mental health disorder characterized by persistent sadness and loss of interest.",
        "remedies": [
            "Therapy (Cognitive Behavioral Therapy)",
            "Medication (Antidepressants)",
            "Regular exercise",
            "Mindfulness meditation",
            "Healthy sleep schedule"
        ]
    },
    2: {
        "name": "Anxiety",
        "description": "Excessive worry and fear that interferes with daily activities.",
        "remedies": [
            "Therapy (CBT)",
            "Breathing exercises",
            "Medication",
            "Limit caffeine",
            "Regular routine"
        ]
    },
    3: {
        "name": "Bipolar Disorder",
        "description": "Mood swings ranging from depressive lows to manic highs.",
        "remedies": [
            "Mood stabilizers",
            "Therapy",
            "Regular sleep",
            "Stress management",
            "Support groups"
        ]
    }
}

# ========== API ROUTES ==========

@app.get("/")
def root():
    """Root endpoint - API health check"""
    return {
        "message": "Mental Wellness Checker API",
        "status": "running",
        "version": settings.VERSION
    }

@app.post("/api/assessments", response_model=AssessmentResponse)
def create_assessment(assessment: AssessmentRequest):
    """
    Process mental health assessment
    
    - Receives answers to 5 questions
    - Returns assessment result and remedies
    """
    
    # Check if we have 5 answers
    if len(assessment.answers) != 5:
        raise HTTPException(
            status_code=400, 
            detail="Please answer all 5 questions"
        )
    
    # Count 'yes' answers
    yes_count = sum(1 for answer in assessment.answers if answer.lower() == 'yes')
    
    # Determine result based on yes count
    if yes_count >= 3:
        return AssessmentResponse(
            result="You may benefit from professional support. Consider speaking with a mental health professional.",
            remedies=[
                "Schedule appointment with therapist",
                "Practice self-care daily",
                "Maintain sleep schedule",
                "Connect with support network",
                "Consider joining support group"
            ],
            severity="high"
        )
    elif yes_count >= 1:
        return AssessmentResponse(
            result="You're experiencing some symptoms. Monitor your mental health and practice self-care.",
            remedies=[
                "Practice mindfulness",
                "Maintain daily routine",
                "Exercise regularly",
                "Talk to trusted friends",
                "Monitor your mood"
            ],
            severity="medium"
        )
    else:
        return AssessmentResponse(
            result="You appear to be managing well. Continue healthy habits.",
            remedies=[
                "Continue current habits",
                "Stay connected with others",
                "Practice stress management",
                "Regular self-check-ins",
                "Maintain work-life balance"
            ],
            severity="low"
        )

@app.get("/api/disorders", response_model=List[DisorderResponse])
def get_all_disorders():
    """Get list of all available disorders"""
    disorders_list = []
    
    for disorder_id, data in DISORDERS_DATA.items():
        disorders_list.append(
            DisorderResponse(
                id=disorder_id,
                name=data["name"],
                description=data["description"],
                remedies=data["remedies"]
            )
        )
    
    return disorders_list

@app.get("/api/disorders/search")
def search_disorder(name: str):
    """Search for disorder by name"""
    name_lower = name.lower().strip()
    
    for disorder_id, data in DISORDERS_DATA.items():
        if name_lower in data["name"].lower():
            return DisorderResponse(
                id=disorder_id,
                name=data["name"],
                description=data["description"],
                remedies=data["remedies"]
            )
    
    # If not found
    raise HTTPException(status_code=404, detail="Disorder not found")

# ========== RUN APPLICATION ==========

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)