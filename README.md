# AI Career Companion Agent

A production-ready multi-agent AI system that helps users improve their careers.

## Features
- **Resume Analysis**: Extract skills, experience, and projects.
- **Target Role Interpretation**: Understand what specific roles require.
- **Skill Gap Reasoning**: Identify the delta between your resume and target role.
- **Career Roadmap**: Personalised week-by-week learning plan.
- **Interview Simulation**: Practice questions tailored to your profile.

## Tech Stack
- **Backend**: FastAPI, Pydantic AI, Loguru.
- **Frontend**: Next.js 14, Tailwind CSS, Lucide Icons, Framer Motion.
- **Model**: OpenRouter (Gemini / Llama).

## Setup

### Backend
1. `cd backend`
2. `pip install -r requirements.txt`
3. Create `.env` from `.env.example` and add your `OPENROUTER_API_KEY`.
4. `python main.py`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Agent Architecture
Built using **Pydantic AI** for strict validation, retries, and structured outputs. Each agent is specialized for a single part of the career growth journey.
