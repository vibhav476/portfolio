"""
Architecture Diagram Agent
Converts system architecture descriptions into Mermaid diagram syntax using Claude.
"""

from anthropic import Anthropic

DIAGRAM_SYSTEM_PROMPT = """You are an expert at creating clear, readable Mermaid diagrams for software system architectures.

Given a system architecture description, generate a Mermaid diagram using graph TD (top-down) syntax.

Rules:
1. Use descriptive node labels (e.g., User["User / Browser"], LB["Load Balancer"])
2. Use arrows with labels where helpful (e.g., --> |"REST API"|)
3. Group related services using subgraph blocks
4. Keep diagrams clean - no more than 15-20 nodes
5. Include infrastructure components (CDN, Load Balancer, Cache, etc.) when mentioned
6. Return ONLY the Mermaid code, no markdown fences, no explanation

Example output:
graph TD
    User["User / Browser"] --> CDN["CloudFront CDN"]
    CDN --> LB["Load Balancer"]
    LB --> API["API Server"]
    API --> DB["PostgreSQL"]
    API --> Cache["Redis Cache"]"""


class DiagramAgent:
    """Agent 2: Generates Mermaid architecture diagrams from descriptions."""

    def __init__(self, client: Anthropic):
        self.client = client

    def generate(self, architecture: str) -> str:
        """Generate a Mermaid diagram from the architecture description."""
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=DIAGRAM_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"Generate a Mermaid architecture diagram for:\n{architecture}",
                }
            ],
        )

        raw = message.content[0].text.strip()
        # Strip markdown fences if present
        if raw.startswith("\`\`\`"):
            raw = raw.split("\n", 1)[1]
            raw = raw.rsplit("\`\`\`", 1)[0].strip()
        return raw


# ---------------------------------------------------------------------------
# Demo / fallback diagram
# ---------------------------------------------------------------------------

DEMO_DIAGRAM = """graph TD
    User["User / Browser"] --> React["React Frontend"]
    React --> CDN["CloudFront CDN"]
    React --> LB["Load Balancer (ALB)"]

    subgraph Backend
        LB --> API1["Node.js API #1"]
        LB --> API2["Node.js API #2"]
    end

    subgraph Data Layer
        API1 --> Cache["Redis Cache"]
        API2 --> Cache
        API1 --> DB_Primary["PostgreSQL Primary"]
        API2 --> DB_Primary
        DB_Primary --> DB_Replica["PostgreSQL Replica"]
    end

    subgraph Infrastructure
        API1 --> Queue["SQS Queue"]
        API2 --> Queue
        Queue --> Worker["Worker Service"]
        API1 --> Monitor["CloudWatch"]
    end"""
