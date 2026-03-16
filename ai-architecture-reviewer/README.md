# AI System Architecture Reviewer

An intelligent AI agent that evaluates software system architectures and provides expert-level feedback on design, scalability, security, and performance.

## Overview

This tool uses a **multi-agent architecture** powered by Anthropic's Claude API. Users input a system architecture description and receive:

- **Architecture Score** (1-10) with detailed rationale
- **Strengths** identified in the current design
- **Risks** and potential failure points
- **Scalability Issues** and bottleneck detection
- **Security Concerns** and vulnerability analysis
- **Recommended Improvements** with actionable steps
- **Auto-generated Architecture Diagram** (Mermaid.js)

## How It Works

The backend orchestrates two specialized AI agents:

1. **Architecture Review Agent** - Analyzes the system and returns structured JSON with scores, risks, and recommendations
2. **Diagram Agent** - Converts the architecture description into a Mermaid diagram for visualization

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Single HTML file (zero build step) |
| Backend | Python FastAPI |
| AI Engine | Anthropic Claude API |
| Diagrams | Mermaid.js (client-side rendering) |

## Quick Start

\`\`\`bash
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --port 8000
\`\`\`

Without an API key, the system runs in **demo mode** with realistic sample responses.

## API Endpoint

**POST** \`/analyze-architecture\`

## Project Structure

\`\`\`
ai-architecture-reviewer/
  main.py                  - FastAPI app, routes, orchestration
  architecture_agent.py    - Review Agent (Claude prompt + parser)
  diagram_agent.py         - Diagram Agent (Mermaid generation)
  requirements.txt         - Python dependencies
  .env.example             - Environment variable template
  index.html               - Frontend UI
  Product_Document.docx    - Full product specification
\`\`\`

## Author

**Vibhav Pamidi** - [@vibhav476](https://github.com/vibhav476)
