from models.state import CriticFeedback, ResearchState
from agents.common import ask_for_json


def run_critic(state: ResearchState) -> CriticFeedback:
    if state.research is None or state.draft is None:
        raise ValueError("Research and draft are required before review.")

    system_prompt = """
You are a strict quality reviewer for a market research brief.
Check that every factual claim is supported by the supplied findings, the brief
has a summary, no more than two competitors, key observations, sources, and
missing information, and unsupported claims are qualified. Do not demand facts
that are not available; missing data should be disclosed.
Approve only if the brief is clear, evidence-aware, and contains all required
sections. Return JSON: approved (boolean), score (integer 0-100),
feedback (string), issues (array of strings).
"""
    payload = {
        "query": state.query,
        "research": state.research.model_dump(),
        "draft": state.draft.model_dump(),
    }
    data = ask_for_json(system_prompt, str(payload))
    return CriticFeedback(
        approved=bool(data.get("approved", False)),
        score=max(0, min(100, int(data.get("score", 0)))),
        feedback=data.get("feedback", "No feedback was returned."),
        issues=data.get("issues", []),
    )
