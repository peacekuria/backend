# FastAPI application for mental wellness assessment and disorder information
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.database import engine, Base

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application instance
app = FastAPI(
    title="Mental Wellness Checker API",
    version="1.0.0"
)

# Enable CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== IN-MEMORY DATA ==========

# Sample disorders database (in production, this would come from database)
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

# Root endpoint - health check
@app.get("/")
def root():
    """API health check endpoint"""
    return {
        "message": "Mental Wellness Checker API",
        "status": "running",
        "version": "1.0.0"
    }

# Assessment endpoint - evaluate mental health
@app.post("/api/assessments")
def create_assessment(assessment: dict):
    """
    Process mental health assessment based on user answers
    - Expects 5 yes/no answers
    - Returns severity level and treatment recommendations
    """
    
    answers = assessment.get("answers", [])
    
    # Validate we have exactly 5 answers
    if len(answers) != 5:
        raise HTTPException(
            status_code=400, 
            detail="Please answer all 5 questions"
        )
    
    # Count positive responses (yes answers)
    yes_count = sum(1 for answer in answers if isinstance(answer, str) and answer.lower() == 'yes')
    
    # Return assessment based on symptom severity
    if yes_count >= 3:
        return {
            "result": "You may benefit from professional support. Consider speaking with a mental health professional.",
            "remedies": [
                "Schedule appointment with therapist",
                "Practice self-care daily",
                "Maintain sleep schedule",
                "Connect with support network",
                "Consider joining support group"
            ],
            "severity": "high"
        }
    elif yes_count >= 1:
        return {
            "result": "You're experiencing some symptoms. Monitor your mental health and practice self-care.",
            "remedies": [
                "Practice mindfulness",
                "Maintain daily routine",
                "Exercise regularly",
                "Talk to trusted friends",
                "Monitor your mood"
            ],
            "severity": "medium"
        }
    else:
        return {
            "result": "You appear to be managing well. Continue healthy habits.",
            "remedies": [
                "Continue current habits",
                "Stay connected with others",
                "Practice stress management",
                "Regular self-check-ins",
                "Maintain work-life balance"
            ],
            "severity": "low"
        }

# Get all disorders endpoint
@app.get("/api/disorders")
def get_all_disorders():
    """Retrieve list of all mental health disorders in the database"""
    disorders_list = []
    
    for disorder_id, data in DISORDERS_DATA.items():
        disorders_list.append({
            "id": disorder_id,
            "name": data["name"],
            "description": data["description"],
            "remedies": data["remedies"]
        })
    
    return disorders_list

# Search disorder endpoint
@app.get("/api/disorders/search")
def search_disorder(name: str):
    """Search for disorder by name"""
    name_lower = name.lower().strip()
    
    for disorder_id, data in DISORDERS_DATA.items():
        if name_lower in data["name"].lower():
            return {
                "id": disorder_id,
                "name": data["name"],
                "description": data["description"],
                "remedies": data["remedies"]
            }
    
    # If not found
    raise HTTPException(status_code=404, detail="Disorder not found")

# ========== RUN APPLICATION ==========

# Start the FastAPI server
if __name__ == "__main__":
    # Run on all interfaces, port 8000, with auto-reload for development
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
