import os
import streamlit as st
from dotenv import load_dotenv

from agents.orchestrator import run_research

load_dotenv()

st.set_page_config(
    page_title="Multi-Agent Market Research",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Multi-Agent Market Research")
st.caption("A sequential AI research workflow powered by four specialized agents.")

with st.sidebar:
    st.header("Configuration")
    openai_ready = bool(os.getenv("OPENAI_API_KEY"))
    tavily_ready = bool(os.getenv("TAVILY_API_KEY"))
    st.write("OpenAI API:", "✅ Configured" if openai_ready else "❌ Missing")
    st.write("Tavily API:", "✅ Configured" if tavily_ready else "⚠️ Missing — sample research fallback will be used")
    st.info("Keep your API keys in the local .env file. Never upload that file to GitHub.")

query = st.text_area(
    "What company or industry should we research?",
    placeholder="Example: Analyze the food delivery market in Nepal.",
    height=100,
)

if st.button("Start research", type="primary", disabled=not bool(query.strip())):
    if not openai_ready:
        st.error("OpenAI API key is missing. Add OPENAI_API_KEY to your .env file and restart Streamlit.")
    else:
        progress = st.progress(0)
        status = st.empty()
        events = {
            "orchestrator": ("Orchestrator", 5),
            "researcher": ("Researcher", 30),
            "analyst": ("Analyst", 60),
            "critic": ("Critic", 80),
            "revision": ("Analyst revision", 90),
            "complete": ("Workflow completed", 100),
        }

        def update_progress(stage, message):
            label, value = events.get(stage, ("Working", 10))
            progress.progress(value)
            status.info(f"**{label}:** {message}")

        try:
            with st.spinner("Agents are working on your research..."):
                result = run_research(query.strip(), progress_callback=update_progress)

            progress.progress(100)
            status.success("Research workflow completed.")

            st.divider()
            st.subheader("Research brief")
            if result["research"].source_mode == "sample":
                st.warning("Sample research mode: web search was unavailable. The findings below are illustrative and are not verified current market facts.")
            brief = result["final_report"]

            st.markdown("### Summary")
            st.write(brief.summary)

            st.markdown("### Competitors")
            if brief.competitors:
                for competitor in brief.competitors[:2]:
                    st.write(f"- {competitor}")
            else:
                st.write("No competitors were identified from the available evidence.")

            st.markdown("### Key observations")
            for item in brief.key_observations:
                st.write(f"- {item}")

            st.markdown("### Sources")
            if brief.sources:
                for source in brief.sources:
                    if source.url:
                        st.markdown(f"- [{source.title}]({source.url}) — `{source.source_type}`")
                    else:
                        st.write(f"- {source.title} — `{source.source_type}`")
            else:
                st.write("No sources were available.")

            st.markdown("### Missing information")
            if brief.missing_information:
                for item in brief.missing_information:
                    st.write(f"- {item}")
            else:
                st.write("No major information gaps were identified by the agents.")

            with st.expander("Agent workflow details"):
                st.write(f"**Research mode:** {result['research'].source_mode}")
                st.write(f"**Research findings collected:** {len(result['research'].findings)}")
                st.write(f"**Critic score:** {result['critic_feedback'].score}/100")
                st.write(f"**Critic approved:** {'Yes' if result['critic_feedback'].approved else 'No'}")
                st.write(f"**Revisions used:** {result['revision_count']}")
                st.write("**Critic feedback:**")
                st.write(result["critic_feedback"].feedback)
                if result["critic_feedback"].issues:
                    st.write("**Issues:**")
                    for issue in result["critic_feedback"].issues:
                        st.write(f"- {issue}")

            st.download_button(
                "Download research brief (JSON)",
                data=brief.model_dump_json(indent=2),
                file_name="research_brief.json",
                mime="application/json",
            )
        except Exception as exc:
            st.error(f"The workflow could not be completed: {exc}")
            st.caption("Check your API keys, internet connection, and terminal error details.")
