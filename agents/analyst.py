from models.state import ResearchBrief, ResearchState
from agents.common import ask_for_json


def run_analyst(state: ResearchState, revision_instructions: str | None = None) -> ResearchBrief:
    research = state.research
    if research is None:
        raise ValueError("Research findings are missing.")

    system_prompt = """
You are a careful market research analyst.
Use only the supplied research evidence. Do not invent statistics, market shares,
dates, company facts, or citations. If evidence is weak or absent, say so in
missing_information and qualify the summary. Competitors must be supported by
the supplied evidence; include no more than two. Return valid JSON with:
summary (string), competitors (array of strings, max 2),
key_observations (array of strings), sources (array of objects with title,
url, source_type), missing_information (array of strings).
source_type must be 'web' or 'sample'.
"""
    evidence = {
        "query": state.query,
        "source_mode": research.source_mode,
        "findings": [item.model_dump() for item in research.findings],
        "research_competitors": research.competitors,
        "missing_information": research.missing_information,
        "revision_instructions": revision_instructions or "No revision requested.",
    }
    data = ask_for_json(system_prompt, str(evidence))
    # Preserve provenance from retrieved evidence rather than trusting invented URLs.
    allowed_sources = {
        (f.source_title, f.source_url)
        for f in research.findings
    }
    cleaned_sources = []
    for source in data.get("sources", []):
        key = (source.get("title"), source.get("url"))
        if key in allowed_sources:
            cleaned_sources.append({
                "title": key[0],
                "url": key[1],
                "source_type": research.source_mode,
            })
    if not cleaned_sources:
        cleaned_sources = [
            {
                "title": f.source_title,
                "url": f.source_url,
                "source_type": research.source_mode,
            }
            for f in research.findings
        ]

    return ResearchBrief(
        summary=data.get("summary", "The available evidence is insufficient for a reliable summary."),
        competitors=(data.get("competitors") or research.competitors)[:2],
        key_observations=data.get("key_observations", []),
        sources=cleaned_sources,
        missing_information=list(dict.fromkeys(
            research.missing_information + data.get("missing_information", [])
        )),
    )
