import logging
from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import PyPDF2
import io

from backend.agents import (
    run_resume_analysis,
    run_role_interpretation,
    run_skill_gap_analysis,
    run_roadmap_generation,
    run_interview_simulation
)
from backend.models import CareerCompanionReport, ResumeAnalysis, RoleRequirements, SkillGapAnalysis
from backend.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("career-companion")

app = FastAPI(title="AI Career Companion API")

# Check for API key on startup
@app.on_event("startup")
async def startup_event():
    if not settings.openrouter_api_key or "your_openrouter_api_key" in settings.openrouter_api_key:
        logger.warning("OPENROUTER_API_KEY is missing or using placeholder! Agents will fail.")
    else:
        logger.info("OPENROUTER_API_KEY detected.")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RoleSelectionRequest(BaseModel):
    role_name: str

class FullAnalysisRequest(BaseModel):
    resume_text: str
    target_role: str

@app.get("/")
async def root():
    return {"message": "AI Career Companion API is running"}

@app.post("/analyze-full")
async def analyze_full(request: FullAnalysisRequest):
    """
    Runs the entire pipeline in one go for simplicity or step-by-step.
    """
    try:
        logger.info(f"Starting full analysis for role: {request.target_role}")
        
        # 1. Analyze Resume
        resume_info = await run_resume_analysis(request.resume_text)
        
        # 2. Interpret Role
        role_info = await run_role_interpretation(request.target_role)
        
        # 3. Analyze Gaps
        gap_info = await run_skill_gap_analysis(resume_info, role_info)
        
        # 4. Generate Roadmap
        roadmap_info = await run_roadmap_generation(gap_info)
        
        # 5. Interview Simulation
        interview_info = await run_interview_simulation(role_info, gap_info)
        
        return CareerCompanionReport(
            resume_analysis=resume_info,
            role_requirements=role_info,
            skill_gaps=gap_info.gaps,
            roadmap=roadmap_info.roadmap,
            interview_questions=interview_info.questions
        )
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "Unauthorized" in error_msg:
            error_msg = "OpenRouter API Key is invalid or missing. Please check your .env file."
        logger.error(f"Full analysis failed: {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)

@app.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    """
    Extracts text from PDF/Text and runs initial resume analysis.
    """
    try:
        content = await file.read()
        if file.content_type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        else:
            text = content.decode("utf-8")
        
        if not text.strip():
            raise ValueError("Resume text is empty")

        analysis = await run_resume_analysis(text)
        return {"resume_text": text, "analysis": analysis}
    except Exception as e:
        import traceback
        error_msg = str(e)
        logger.error(f"Resume parsing failed: {error_msg}")
        logger.error(traceback.format_exc())
        
        if "401" in error_msg or "Unauthorized" in error_msg:
            error_msg = "OpenRouter API Key is invalid or missing. Please set YOUR_API_KEY in the .env file and restart the backend."
        elif "empty" in error_msg.lower():
            error_msg = "The uploaded file contains no text."
        
        raise HTTPException(status_code=400, detail=error_msg)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
