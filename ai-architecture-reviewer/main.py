"""
AI System Architecture Reviewer - FastAPI Backend
==================================================
Two AI agents powered by the Anthropic Claude API:
  Agent 1: Architecture Review (score, strengths, risks, recommendations)
  Agent 2: Diagram Generation (Mermaid syntax)

Run:  uvicorn main:app --reload --port 8000
Docs: http://localhost:8000/docs
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from architecture_agent import ArchitectureReviewAgent, DEMO_REVIEW
from diagram_agent import DiagramAgent, DEMO_DIAGRAM

load_dotenv()

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = FastAPI(
    title="AI System Architecture Reviewer",
    description="Analyze and improve your system architecture using AI agents.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class ArchitectureRequest(BaseModel):
    architecture: str = Field(..., min_length=10, description="System architecture description")
    tech_stack: str = Field("", description="Technology stack summary")
    traffic: str = Field("", description="Expected traffic / scale")

class ArchitectureResponse(BaseModel):
    analysis: dict
    diagram: str
    demo_mode: bool = False

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/")
def root():
    return {"status": "running", "service": "AI System Architecture Reviewer"}


@app.get("/health")
def health():
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    return {
        "status": "healthy",
        "api_configured": bool(api_key),
        "demo_mode": not bool(api_key),
    }


@app.post("/analyze-architecture", response_model=ArchitectureResponse)
def analyze_architecture(req: ArchitectureRequest):
    """
    Main endpoint. Runs two AI agents in sequence:
      1. Architecture Review Agent  -> structured analysis JSON
      2. Diagram Agent              -> Mermaid diagram string

    If ANTHROPIC_API_KEY is not set, returns realistic demo data.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY", "")

    # -- Demo mode (no API key) --
    if not api_key:
        return ArchitectureResponse(
            analysis=DEMO_REVIEW,
            diagram=DEMO_DIAGRAM,
            demo_mode=True,
        )

    # -- Live mode --
    try:
        from anthropic import Anthropic

        client = Anthropic(api_key=api_key)

        review_agent = ArchitectureReviewAgent(client)
        diagram_agent = DiagramAgent(client)

        analysis = review_agent.analyze(
            architecture=req.architecture,
            tech_stack=req.tech_stack,
            traffic=req.traffic,
        )
        diagram = diagram_agent.generate(req.architecture)

        return ArchitectureResponse(
            analysis=analysis,
            diagram=diagram,
            demo_mode=False,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Example test payloads (visible at /docs)
# ---------------------------------------------------------------------------
EXAMPLE_PAYLOADS = {
    "basic_web_app": {
        "architecture": "Frontend: React\nBackend: Node.js\nDatabase: PostgreSQL\nInfrastructure: AWS EC2\nTraffic: 100k users/day",
        "tech_stack": "React, Node.js, PostgreSQL, AWS EC2",
        "traffic": "100k users per day",
    },
    "microservices": {
        "architecture": "Frontend: Next.js on Vercel\nAPI Gateway: Kong\nServices: User Service (Go), Order Service (Python), Payment Service (Java)\nDatabase: MongoDB (users), PostgreSQL (orders), Redis (cache)\nMessage Queue: RabbitMQ\nInfrastructure: Kubernetes on AWS EKS\nTraffic: 1M requests/day",
        "tech_stack": "Next.js, Go, Python, Java, MongoDB, PostgreSQL, Redis, RabbitMQ, K8s",
        "traffic": "1M requests per day",
    },
    "startup_mvp": {
        "architecture": "Frontend: Vue.js SPA\nBackend: Django REST Framework\nDatabase: SQLite\nHosting: Single DigitalOcean droplet\nTraffic: 500 users/day",
        "tech_stack": "Vue.js, Django, SQLite, DigitalOcean",
        "traffic": "500 users per day",
    },
}
