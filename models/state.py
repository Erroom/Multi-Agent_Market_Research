from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class AppModel(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra="forbid")


class SourceReference(AppModel):
    title: str
    url: str | None = None
    source_type: Literal["web", "sample"]


class ResearchFinding(AppModel):
    claim: str
    source_title: str
    source_url: str | None = None
    evidence_snippet: str | None = None


class ResearchData(AppModel):
    topic: str
    source_mode: Literal["web", "sample"]
    findings: list[ResearchFinding] = Field(default_factory=list)
    competitors: list[str] = Field(default_factory=list, max_length=2)
    missing_information: list[str] = Field(default_factory=list)


class ResearchBrief(AppModel):
    summary: str
    competitors: list[str] = Field(default_factory=list, max_length=2)
    key_observations: list[str] = Field(default_factory=list)
    sources: list[SourceReference] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)


class CriticFeedback(AppModel):
    approved: bool
    score: int = Field(ge=0, le=100)
    feedback: str
    issues: list[str] = Field(default_factory=list)


class ResearchState(AppModel):
    query: str = Field(min_length=3)
    research: ResearchData | None = None
    draft: ResearchBrief | None = None
    critic_feedback: CriticFeedback | None = None
    revision_count: int = Field(default=0, ge=0, le=1)
    final_report: ResearchBrief | None = None
    workflow_status: Literal[
        "initialized", "researching", "analyzing",
        "reviewing", "completed", "failed"
    ] = "initialized"
