## Personal Transport API

Lightweight FastAPI scaffold for powering personal bike transport services (and beyond).
The initial goal is a deterministic, reproducible backend foundation that the team can grow rapidly.

---

## Current Capabilities
- FastAPI application bootstrap with `/health` returning `{"status": "ok"}`
- SQLAlchemy engine + session factory configured via environment variables
- Ready-to-extend module layout for models, schemas, routers, and services
- SQLite database default for local development (override with `DATABASE_URL`)

## Tech Stack
- Python 3.10+
- FastAPI
- SQLAlchemy + Alembic
- SQLite (development)
- Uvicorn
- python-dotenv

---

## Getting Started
Follow these steps exactly to spin up the local backend.

1. **Clone and enter the project**
   ```
   git clone https://github.com/MelEUsher/PersonalTransportAPI.git
   cd PersonalTransportAPI
   ```
2. **Create & activate a virtual environment**
   - macOS/Linux
     ```
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - Windows (PowerShell)
     ```
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
3. **Install dependencies**
   ```
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. **Configure environment variables**
   ```
   cp .env.example .env
   ```
   Adjust `DATABASE_URL` if you are not using the default SQLite database.
5. **Run the development server**
   ```
   uvicorn app.main:app --reload
   ```
6. **Smoke test the API**
   Visit http://localhost:8000/health or run:
   ```
   curl http://localhost:8000/health
   ```
   Expect: `{"status":"ok"}`

---

## Project Structure
```
PersonalTransportAPI/
├─ .env.example
├─ .gitignore
├─ app/
│  ├─ __init__.py
│  ├─ db.py
│  ├─ main.py
│  ├─ models/
│  ├─ routers/
│  ├─ schemas/
│  └─ services/
├─ requirements.txt
└─ (additional project docs and configs)
```

---

## Development Workflow
Keep the workflow simple and predictable:
- Open an **Issue** for each piece of work.
- Branch from `master` using the format `feature/issue-#/short-name`, `bugfix/issue-#/short-name`, or `chore/issue-#/short-name`.
- Open a **Pull Request** that references the Issue (`Closes #<issue-number>`).
- Merge when checks pass; the Issue will close automatically.
- Keep the GitHub Project board in sync (To Do → In Progress → Done).
