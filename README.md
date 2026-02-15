# 🚀 DataPulse: SQL AI Agent

DataPulse is a specialized AI tool that translates English questions into executable PostgreSQL queries. It features a dual-interface for querying data and exploring database schemas.

## ✨ Features
- **Natural Language to SQL**: Powered by OpenAI/Gemini to generate precise queries.
- **Interactive Editor**: Review and edit SQL before execution.
- **Database Explorer**: Preview tables and download results as CSV.
- **Modern UI**: Dark-themed, high-contrast interface.

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **AI**: OpenAI API / Google GenAI
- **Database**: PostgreSQL (psycopg2)
- **Environment**: uv / Python 3.12+

## 🚀 Local Setup
1. Clone the repo: `git clone <your-repo-url>`
2. Install dependencies: `uv sync`
3. Set up your `.env` with DB and AI credentials.
4. Seed the database: `uv run seed_data.py`
5. Run the app: `uv run streamlit run app.py`