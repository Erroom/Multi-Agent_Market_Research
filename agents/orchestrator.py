from collections.abc import Callable

from models.state import ResearchState
from agents.researcher import run_researcher
from agents.analyst import run_analyst
from agents.critic import run_critic


def run_research(
    query: str,
    progress_callback: Callable[[str, str], None] | None = None,
) -> dict:
    """Run Orchestrator -> Researcher -> Analyst -> Critic, with at most one revision."""
    state = ResearchState(query=query)

    def notify(stage: str, message: str):
        if progress_callback:
            progress_callback(stage, message)

    try:
        notify("orchestrator", "Received query and initialized shared workflow state.")
        state.workflow_status = "researching"

        notify("researcher", "Searching the web or preparing clearly labelled sample research.")
        state.research = run_researcher(state.query)

        state.workflow_status = "analyzing"
        notify("analyst", "Analyzing the collected findings and drafting the brief.")
        state.draft = run_analyst(state)

        state.workflow_status = "reviewing"
        notify("critic", "Reviewing evidence, completeness, and clarity.")
        state.critic_feedback = run_critic(state)

        if not state.critic_feedback.approved:
            state.revision_count = 1
            notify("revision", "Critic requested improvements; analyst is revising once.")
            state.draft = run_analyst(
                state,
                revision_instructions=state.critic_feedback.feedback
                + "\nIssues: " + "; ".join(state.critic_feedback.issues),
            )
            # Review the revised version. No further revision is permitted.
            notify("critic", "Checking the revised brief. No additional revision will be made.")
            state.critic_feedback = run_critic(state)

        state.final_report = state.draft
        state.workflow_status = "completed"
        notify("complete", "Final brief is ready.")
        return {
            "research": state.research,
            "final_report": state.final_report,
            "critic_feedback": state.critic_feedback,
            "revision_count": state.revision_count,
            "workflow_status": state.workflow_status,
        }
    except Exception:
        state.workflow_status = "failed"
        raise
