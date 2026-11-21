# Multi-Agent Market Research App

A simple Streamlit application that generates a short company or industry research brief through a sequential four-agent workflow.

## Features

- **Orchestrator:** initializes shared state and coordinates the workflow.
- **Researcher:** retrieves web results using Tavily. If Tavily is unavailable, it uses explicitly labelled illustrative sample research.
- **Analyst:** uses OpenAI to produce a structured research brief from the collected evidence.
- **Critic:** reviews evidence, completeness, and clarity. It can request at most one revision.
- **Shared data:** Pydantic models validate research findings, the brief, critic feedback, and workflow state.
- **Streamlit UI:** displays the brief, sources, missing information, and workflow details.

## Requirements

- Python 3.10 or newer
- OpenAI API key
- Tavily API key for live web research
- Internet connection

The application uses `gpt-4.1-mini` by default. You can change the model using `OPENAI_MODEL` in `.env` to a model available to your OpenAI account.

## Setup on Windows (PowerShell)

1. Download or clone this repository.
2. Open the project folder in VS Code or PowerShell.
3. Create and activate a virtual environment:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Create your local `.env` file by copying `.env.example`:

   ```powershell
   Copy-Item .env.example .env
   ```

6. Open `.env` and add your own API keys:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_MODEL=gpt-4.1-mini
   TAVILY_API_KEY=your_tavily_api_key
   ```

7. Start the application:

   ```powershell
   streamlit run app.py
   ```

8. Streamlit will provide a local URL, usually `http://localhost:8501`. Open it in your browser.

## Setup on macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Add your API keys to `.env`, then run:

```bash
streamlit run app.py
```

## How the workflow works

```text
User query
   |
Orchestrator
   |
Researcher ---- Tavily web search
   |             (sample fallback if unavailable)
   |
Analyst ------- OpenAI generates structured brief
   |
Critic -------- OpenAI reviews the brief
   |
   +-- Approved --> Final brief
   |
   +-- Not approved --> One analyst revision --> Final brief
```

All agent handoffs use the shared `ResearchState` and related Pydantic models in `models/state.py`.

## Sample output

See [`outputs/sample_output.md`](outputs/sample_output.md). It is clearly labelled as illustrative and is not presented as verified market research.

## Run the data-model check

```powershell
python -c "from models.state import ResearchState; s=ResearchState(query='Analyze the food delivery market in Nepal'); print(s.model_dump_json(indent=2))"
```

## Project structure

```text
multi-agent-market-research/
├── app.py
├── agents/
│   ├── common.py
│   ├── orchestrator.py
│   ├── researcher.py
│   ├── analyst.py
│   └── critic.py
├── models/
│   └── state.py
├── tools/
│   └── web_search.py
├── sample_data/
│   └── sample_research.json
├── outputs/
│   └── sample_output.md
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Security

- Never commit `.env` or API keys.
- Commit `.env.example` with placeholder values only.
- Do not paste API keys into issue trackers, screenshots, or public repositories.

## Limitations

- Web search results depend on Tavily availability and the sources it retrieves.
- The LLM may make mistakes; the critic is a quality-control step, not a guarantee of factual correctness.
- Sample fallback content is illustrative and must not be cited as current market evidence.
- This is a student prototype, not a substitute for professional market due diligence.
