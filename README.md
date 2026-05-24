# AI Engineering Course

Hands-on exercises for learning AI engineering concepts in Python—from tokenization to tool-using agents.

## Prerequisites

- Python 3.10+ (3.14 used in development)
- An [OpenAI API key](https://platform.openai.com/api-keys) (for lessons that call the API)

## Setup

1. **Clone and enter the repo**

   ```bash
   cd "AI Engineering Course"
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root (never commit it):

   ```env
   OPENAI_API_KEY=sk-your-key-here
   ```

## Project structure

```
.
├── 01_tokenization/     # Tiktoken: encode/decode text
├── weather_agent/       # Multi-step agent with tool calls (wttr.in)
├── requirements.txt     # Shared dependencies for all lessons
├── venv/                # Local virtual environment (gitignored)
└── .env                 # API keys (gitignored)
```

## Lessons

### 01 — Tokenization

Explore how text is split into tokens with `tiktoken`.

```bash
python 01_tokenization/main.py
```

### Weather agent

A planning agent that uses structured outputs (Pydantic), calls a `getWeather` tool, and answers weather questions for a city.

```bash
python weather_agent/main.py
```

Example flow: `START` → `PLAN` → `TOOL_CALL` → `OUTPUT`. Type a city or question when prompted (e.g. `What is the weather in Kolkata?`).

## Managing dependencies

Install new packages with the project venv active, then update the shared lockfile:

```bash
pip install <package>
pip freeze > requirements.txt
```

On a new machine, run `pip install -r requirements.txt` after creating the venv.

## Security

- Do not commit `.env` or API keys.
- `venv/` and `.env` are listed in `.gitignore`.
