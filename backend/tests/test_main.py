import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from backend.main import app
from backend.models import ResumeAnalysis, RoleRequirements, SkillGapAnalysis, CareerRoadmap, InterviewSimulation

client = TestClient(app)

@pytest.fixture
def mock_resume_analysis():
    return ResumeAnalysis(
        name="John Doe",
        years_of_experience=5,
        skills=["Python", "FastAPI"],
        projects=["AI Agent"],
        strengths=["Coding"],
        weaknesses=["None"]
    )

@pytest.fixture
def mock_role_requirements():
    return RoleRequirements(
        required_skills=["Python", "Cloud"],
        expected_experience="5+ years",
        common_tools=["Docker"],
        role_summary="A cool role"
    )

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI Career Companion API is running"}

@patch("backend.main.run_resume_analysis")
@patch("backend.main.run_role_interpretation")
@patch("backend.main.run_skill_gap_analysis")
@patch("backend.main.run_roadmap_generation")
@patch("backend.main.run_interview_simulation")
def test_analyze_full(
    mock_interview, 
    mock_roadmap, 
    mock_gap, 
    mock_role, 
    mock_resume,
    mock_resume_analysis,
    mock_role_requirements
):
    # Setup mocks
    mock_resume.return_value = mock_resume_analysis
    mock_role.return_value = mock_role_requirements
    mock_gap.return_value = SkillGapAnalysis(gaps=[])
    mock_roadmap.return_value = CareerRoadmap(roadmap=[])
    mock_interview.return_value = InterviewSimulation(questions=[])

    response = client.post("/analyze-full", json={
        "resume_text": "Sample resume text",
        "target_role": "Software Engineer"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["resume_analysis"]["name"] == "John Doe"
    assert "role_requirements" in data
    assert "skill_gaps" in data
