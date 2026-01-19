import logging
from typing import Any
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from backend.config import settings
from backend.models import (
    ResumeAnalysis, 
    RoleRequirements, 
    SkillGapAnalysis, 
    CareerRoadmap, 
    InterviewSimulation
)

# Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_agent(output_type: Any, system_prompt: str) -> Agent:
    """
    Creates an agent with the first available model. 
    The model will be swapped dynamically during runtime if it fails.
    """
    # Start with the first model in the list
    initial_model = OpenAIModel(
        model_name=settings.model_list[0],
        provider='openrouter'
    )
    return Agent(
        initial_model,
        output_type=output_type,
        system_prompt=system_prompt,
        retries=1 # We handle retries/failover manually across models
    )

# --- Define Agents ---
resume_analyzer_agent = get_agent(
    ResumeAnalysis,
    "You are an expert HR and Career Consultant. Analyze the provided resume text and extract structured information."
)

role_interpreter_agent = get_agent(
    RoleRequirements,
    "You are a Technical Recruiter. Analyze the given target job role and provide specific skills and experience required."
)

skill_gap_agent = get_agent(
    SkillGapAnalysis,
    "You are a Career Growth Strategist. Compare the user's resume with the target role and identify skill gaps."
)

roadmap_agent = get_agent(
    CareerRoadmap,
    "You are a Learning and Development specialist. Create a week-by-week learning roadmap based on skill gaps."
)

interview_agent = get_agent(
    InterviewSimulation,
    "You are a Senior Hiring Manager. Create challenging interview questions based on the target role and identified weak areas."
)

async def run_agent_with_failover(agent: Agent, prompt: str) -> Any:
    """
    Attempts to run an agent through the list of models in settings.model_list.
    """
    last_error = None
    for model_name in settings.model_list:
        try:
            logger.info(f"Attempting agent run with model: {model_name}")
            agent.model = OpenAIModel(model_name=model_name, provider='openrouter')
            result = await agent.run(prompt)
            
            # Additional check for empty or invalid results from free models
            if not result.output:
                raise ValueError("Model returned an empty result")
                
            return result.output
        except Exception as e:
            last_error = e
            error_msg = str(e)
            logger.warning(f"Model {model_name} failed: {error_msg}")
            # If it's a 401, don't bother trying other models
            if "401" in error_msg or "Unauthorized" in error_msg:
                raise e
            continue
    
    logger.error("All models failed for agent run.")
    raise last_error

# --- Public API Functions ---

async def run_resume_analysis(text: str) -> ResumeAnalysis:
    return await run_agent_with_failover(resume_analyzer_agent, f"Resume Text:\n{text}")

async def run_role_interpretation(role_name: str) -> RoleRequirements:
    return await run_agent_with_failover(role_interpreter_agent, f"Target Role: {role_name}")

async def run_skill_gap_analysis(resume_data: ResumeAnalysis, role_data: RoleRequirements) -> SkillGapAnalysis:
    prompt = f"Resume Info: {resume_data.model_dump()}\nTarget Role Requirements: {role_data.model_dump()}"
    return await run_agent_with_failover(skill_gap_agent, prompt)

async def run_roadmap_generation(gap_data: SkillGapAnalysis) -> CareerRoadmap:
    prompt = f"Skill Gaps: {gap_data.model_dump()}"
    return await run_agent_with_failover(roadmap_agent, prompt)

async def run_interview_simulation(role_data: RoleRequirements, gap_data: SkillGapAnalysis) -> InterviewSimulation:
    prompt = f"Target Role: {role_data.model_dump()}\nSkill Gaps: {gap_data.model_dump()}"
    return await run_agent_with_failover(interview_agent, prompt)
