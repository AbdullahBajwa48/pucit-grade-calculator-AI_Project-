# PUCIT BS(CS) GPA & CGPA Conversational Agent

A script-based LangChain + Groq agent for PUCIT BS(CS) GPA and CGPA questions.
The model selects tools and phrases results; deterministic Python tools perform all arithmetic.

## Files

- `llm.py` — Groq model setup using `init_chat_model("groq:openai/gpt-oss-20b")`.
- `tools.py` — the seven required tools and the supplied BS(CS) course scheme.
- `agent.py` — `create_agent`, system prompt, history-carrying `run_turn`, and terminal chat.
- `.env.example` — key template to submit.
- `.env` — your real key; do not submit it.
- `requirements.txt` — dependencies.
- `app.py` — optional Streamlit GUI.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Put your real Groq key in `.env`:

```text
GROQ_API_KEY=your_key_here
```



## Terminal agent

```bash
python agent.py
```

The program explicitly carries the complete message history from one turn to the next.
This is the required stateless-model conversation pattern.

## Streamlit GUI

```bash
streamlit run app.py
```

## Example conversations to test

1. Underspecified:
   `What GPA do I need this semester?`
   The agent should ask for missing information rather than guessing.

2. Semester GPA:
   Give a semester and marks for the relevant courses. The agent should retrieve
   official credit hours, convert marks through `marks_to_grade_points`, and then
   call `calculate_semester_gpa`.

3. CGPA projection:
   Give current CGPA, completed credit hours, semester GPA, and semester credit hours.

4. Target planning:
   Give current semester, current CGPA, completed credit hours, and target CGPA.
   The agent should widen the horizon when the first required GPA is above the
   maximum possible GPA.

5. Saving:
   Ask explicitly to save a completed result. The agent should then call `save_report`.

