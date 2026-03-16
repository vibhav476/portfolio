"""
Architecture Review Agent
Analyzes software system architectures using the Anthropic Claude API.
Returns structured feedback: score, strengths, risks, scalability, security, recommendations.
"""

import json
from anthropic import Anthropic

REVIEW_SYSTEM_PROMPT = """You are a senior software architect with 20+ years of experience reviewing system architectures at companies like Google, AWS, and Netflix.

Analyze the given system architecture and return a JSON object with exactly this structure:

{
  "score": <number 1-10>,
  "summary": "<2-3 sentence overview>",
  "strengths": ["<strength 1>", "<strength 2>", ...],
  "risks": ["<risk 1>", "<risk 2>", ...],
  "scalability_issues": ["<issue 1>", "<issue 2>", ...],
  "security_issues": ["<issue 1>", "<issue 2>", ...],
  "recommendations": ["<recommendation 1>", "<recommendation 2>", ...]
}

Scoring guide:
- 1-3: Critical issues, architecture needs major rework
- 4-5: Significant gaps, needs substantial improvements
- 6-7: Solid foundation with notable areas for improvement
- 8-9: Well-designed with minor refinements needed
- 10: Exceptional, production-grade architecture

Be specific and actionable. Reference concrete technologies and patterns.
Return ONLY valid JSON, no markdown or extra text."""


class ArchitectureReviewAgent:
    """Agent 1: Reviews system architecture and provides structured analysis."""

    def __init__(self, client: Anthropic):
        self.client = client

    def analyze(self, architecture: str, tech_stack: str = "", traffic: str = "") -> dict:
        """Run the architecture review analysis."""
        user_input = f"Architecture Description:\n{architecture}"
        if tech_stack:
            user_input += f"\n\nTechnology Stack: {tech_stack}"
        if traffic:
            user_input += f"\n\nExpected Traffic: {traffic}"

        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=REVIEW_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_input}],
        )

        raw = message.content[0].text.strip()
        # Strip markdown fences if present
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1]
            raw = raw.rsplit("```", 1)[0]

        return json.loads(raw)


# ---------------------------------------------------------------------------
# Demo / fallback response (no API key required)
# ---------------------------------------------------------------------------

DEMO_REVIEW = {
    "score": 6,
    "summary": "The architecture follows a standard three-tier pattern with React, Node.js, and PostgreSQL. It covers the basics but lacks high-availability and caching layers needed for 100k daily users.",
    "strengths": [
        "Well-established technology stack with large community support",
        "PostgreSQL is a strong choice for relational data with ACID compliance",
        "React provides a performant, component-based frontend",
        "Node.js allows JavaScript across the full stack, simplifying development",
    ],
    "risks": [
        "Single EC2 instance is a single point of failure",
        "No load balancer means zero horizontal scaling capability",
        "No CDN for static assets increases latency for global users",
        "Missing monitoring and alerting infrastructure",
    ],
    "scalability_issues": [
        "Single database instance will become a bottleneck beyond 50k concurrent connections",
        "No caching layer (Redis/Memcached) means every request hits the database",
        "Lack of auto-scaling groups means manual intervention during traffic spikes",
        "No message queue for async processing of heavy tasks",
    ],
    "security_issues": [
        "No mention of HTTPS/TLS termination",
        "Missing Web Application Firewall (WAF)",
        "No rate limiting or DDoS protection",
        "Database not placed in a private subnet",
        "No secrets management solution (e.g., AWS Secrets Manager)",
    ],
    "recommendations": [
        "Add an Application Load Balancer (ALB) with auto-scaling groups",
        "Introduce Redis as a caching layer for frequently accessed data",
        "Place the database in a private subnet with read replicas",
        "Add CloudFront CDN for static asset delivery",
        "Implement AWS WAF and Shield for DDoS protection",
        "Set up CloudWatch monitoring with alerting thresholds",
        "Use RDS Multi-AZ deployment for database high availability",
        "Add an SQS queue for asynchronous task processing",
    ],
}
