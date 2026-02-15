# 🚀 DataPulse: SQL AI Agent

DataPulse is a specialized AI tool that translates English questions into executable PostgreSQL queries. It features a dual-interface for querying data and exploring database schemas.
live url : https://sql-agent-app-ahmad.streamlit.app/

<img width="960" height="448" alt="sql1" src="https://github.com/user-attachments/assets/f94c3fab-8c6a-4c90-971b-8ff1544fe940" />
<img width="960" height="449" alt="sql2" src="https://github.com/user-attachments/assets/2189878a-fe3d-4f7c-83e6-ec63b41f0265" />
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
