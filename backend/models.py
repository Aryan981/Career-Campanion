from pydantic import BaseModel, Field
from typing import List, Literal, Optional

# --- Agent 1: Resume Analyzer ---
class ResumeAnalysis(BaseModel):
    name: str = Field(..., description="Full name of the candidate")
    years_of_experience: int = Field(..., description="Total years of professional experience")
    skills: List[str] = Field(..., description="List of technical and soft skills identified")
    projects: List[str] = Field(..., description="Key projects mentioned in the resume")
    strengths: List[str] = Field(..., description="Identified professional strengths")
    weaknesses: List[str] = Field(..., description="Areas for improvement or missing skills")

# --- Agent 2: Target Role Interpreter ---
class RoleRequirements(BaseModel):
    required_skills: List[str] = Field(..., description="Skills mandatory for the role")
    expected_experience: str = Field(..., description="Years or type of experience expected")
    common_tools: List[str] = Field(..., description="Tools or software commonly used in this role")
    role_summary: str = Field(..., description="A brief summary of what the role entails")

# --- Agent 3: Skill Gap Reasoning ---
class SkillGap(BaseModel):
    skill_name: str
    current_level: int = Field(..., ge=0, le=5, description="Current proficiency (0-5)")
    required_level: int = Field(..., ge=0, le=5, description="Required proficiency (0-5)")
    priority: Literal["low", "medium", "high"]
    reasoning: str

class SkillGapAnalysis(BaseModel):
    gaps: List[SkillGap]

# --- Agent 4: Career Roadmap Planner ---
class RoadmapStep(BaseModel):
    week_number: int
    learning_goal: str
    recommended_resources: List[str]
    estimated_hours: int

class CareerRoadmap(BaseModel):
    roadmap: List[RoadmapStep]

# --- Agent 5: Interview Simulation ---
class InterviewQuestion(BaseModel):
    question: str
    difficulty: Literal["easy", "medium", "hard"]
    expected_answer_points: List[str]

class InterviewSimulation(BaseModel):
    questions: List[InterviewQuestion]

# --- Combined Response Schema ---
class CareerCompanionReport(BaseModel):
    resume_analysis: ResumeAnalysis
    role_requirements: RoleRequirements
    skill_gaps: List[SkillGap]
    roadmap: List[RoadmapStep]
    interview_questions: List[InterviewQuestion]
