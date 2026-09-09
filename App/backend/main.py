import os
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

from App.database.database import get_connection
from App.database.create_tables import create_tables
from App.services.database_service import DatabaseService
from App.services.document_loader_service import get_file_loader
from App.services.matching_service import MatchingService
from App.agents.resume_parser_agent import ResumeParserAgent
from App.agents.job_description_agent import JobDescriptionAgent
from App.models.job_description_model import JobDescription
from App.models.candidate_profile_model import CandidateProfile

app = FastAPI(title="Recruiter AI Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    create_tables()
    # Ensure upload directories exist
    os.makedirs("App/uploads/assets/resumes", exist_ok=True)
    os.makedirs("App/uploads/assets/job_descriptions", exist_ok=True)

@app.get("/health")
def health_check():
    return {"status": "ok"}

# --- Jobs ---

@app.get("/jobs")
def get_jobs():
    db = DatabaseService()
    try:
        jobs = db.get_all_jobs()
        return jobs
    finally:
        db.close()

@app.post("/jobs")
def create_job(job: JobDescription):
    db = DatabaseService()
    try:
        if db.job_exists(job):
            raise HTTPException(status_code=400, detail="Job already exists")
        job_id = db.save_job(job)
        return {"id": job_id, "message": "Job created successfully"}
    finally:
        db.close()

@app.post("/jobs/upload")
async def upload_job_description(file: UploadFile = File(...)):
    if file.filename == "":
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    jd_path = os.path.join("App/uploads/assets/job_descriptions", file.filename)
    with open(jd_path, "wb") as f:
        f.write(await file.read())
        
    try:
        docs = get_file_loader(jd_path)
        jd_text = "\n".join(doc.page_content for doc in docs)
        
        agent = JobDescriptionAgent()
        job = agent.parse_job_description(jd_text)
        return {"job": job.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse JD: {str(e)}")

# --- Candidates ---

@app.get("/candidates")
def get_candidates():
    db = DatabaseService()
    try:
        candidates = db.get_all_candidates()
        return candidates
    finally:
        db.close()

@app.get("/candidates/{candidate_id}")
def get_candidate(candidate_id: int):
    db = DatabaseService()
    try:
        candidate = db.get_candidate_by_id(candidate_id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        return candidate
    finally:
        db.close()

@app.post("/candidates/screen")
async def screen_candidate(file: UploadFile = File(...)):
    """Uploads a resume, parses it, and returns the parsed candidate data."""
    if file.filename == "":
        raise HTTPException(status_code=400, detail="No file uploaded")
        
    resume_path = os.path.join("App/uploads/assets/resumes", file.filename)
    with open(resume_path, "wb") as f:
        f.write(await file.read())
        
    try:
        docs = get_file_loader(resume_path)
        resume_text = "\n".join(doc.page_content for doc in docs)
        
        agent = ResumeParserAgent()
        result = agent.parse_resume(resume_text)
        
        return {
            "candidate": result["candidate"].model_dump(),
            "analysis": result["analysis"].model_dump()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {str(e)}")

@app.post("/candidates")
def save_candidate(candidate: CandidateProfile):
    db = DatabaseService()
    try:
        if db.candidate_exists(candidate):
            raise HTTPException(status_code=400, detail="Candidate already exists")
        candidate_id = db.save_candidate(candidate)
        return {"id": candidate_id, "message": "Candidate saved successfully"}
    finally:
        db.close()

# --- Matching ---

class MatchRequest(BaseModel):
    candidate: dict
    job: dict

@app.post("/match")
def calculate_match(request: MatchRequest):
    try:
        candidate_obj = CandidateProfile(**request.candidate)
        match = MatchingService.calculate_match(candidate_obj, request.job)
        return match
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Match calculation failed: {str(e)}")

# --- Interviews ---
class InterviewRequest(BaseModel):
    candidate_id: int
    job_id: int
    interview_date: str
    interview_time: str
    interviewer: str
    meeting_link: str
    notes: str

@app.get("/interviews")
def get_interviews():
    db = DatabaseService()
    try:
        interviews = db.get_all_interviews()
        return interviews
    finally:
        db.close()

@app.post("/interviews")
def schedule_interview(req: InterviewRequest):
    db = DatabaseService()
    try:
        db.schedule_interview(
            candidate_id=req.candidate_id,
            job_id=req.job_id,
            interview_date=req.interview_date,
            interview_time=req.interview_time,
            interviewer=req.interviewer,
            meeting_link=req.meeting_link,
            notes=req.notes
        )
        return {"message": "Interview scheduled successfully"}
    finally:
        db.close()

@app.delete("/interviews/{interview_id}")
def delete_interview(interview_id: int):
    db = DatabaseService()
    try:
        db.delete_interview(interview_id)
        return {"message": "Interview deleted successfully"}
    finally:
        db.close()
