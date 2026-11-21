from models.state import ResearchData, ResearchFinding
from tools.web_search import search_web


def _sample_research(query: str) -> ResearchData:
    """Clearly labelled fallback; these are prompts for research, not verified facts."""
    return ResearchData(
        topic=query,
        source_mode="sample",
        findings=[
            ResearchFinding(
                claim="The topic requires current market-size, customer-demand, and growth evidence before firm conclusions can be made.",
                source_title="Illustrative sample finding",
                evidence_snippet="Sample fallback only; no external source was retrieved.",
            ),
            ResearchFinding(
                claim="Competitor positioning, geographic coverage, pricing, and customer experience are useful comparison areas.",
                source_title="Illustrative sample finding",
                evidence_snippet="Suggested research dimensions, not verified market facts.",
            ),
        ],
        competitors=[],
        missing_information=[
            "Current market size and growth rate",
            "Verified competitor market shares",
            "Recent customer and pricing data",
        ],
    )


def run_researcher(query: str) -> ResearchData:
    try:
        results = search_web(query, max_results=6)
        if not results:
            return _sample_research(query)

        findings = []
        for result in results:
            findings.append(
                ResearchFinding(
                    claim=result["content"][:1200] or f"Relevant source found: {result['title']}",
                    source_title=result["title"],
                    source_url=result["url"],
                    evidence_snippet=result["content"][:1200] or None,
                )
            )

        return ResearchData(
            topic=query,
            source_mode="web",
            findings=findings,
            competitors=[],
            missing_information=[
                "Market-share figures may not be available in the retrieved sources.",
                "Search findings should be checked against primary industry reports.",
            ],
        )
    except Exception:
        # The app remains demonstrable, but sample mode is explicitly disclosed.
        return _sample_research(query)
