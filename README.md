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

6. Start the application:

   ```powershell
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

## Sample output

See [`outputs/sample_output.md`](outputs/sample_output.md). It is clearly labelled as illustrative and is not presented as verified market research.

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

## Limitations

- Web search results depend on Tavily availability and the sources it retrieves.
- The LLM may make mistakes; the critic is a quality-control step, not a guarantee of factual correctness.
- Sample fallback content is illustrative and must not be cited as current market evidence.
- This is a student prototype, not a substitute for professional market due diligence.
