## Personal Transport API

Lightweight FastAPI scaffold for powering personal bike transport services (and beyond).
The initial goal is a deterministic, reproducible backend foundation that the team can grow rapidly.

---

## Authentication & Security
- JWT-based authentication protects all write routes. Obtain a token via `POST /auth/login` and include it in the `Authorization` header:
  ```
  Authorization: Bearer <your-access-token>
  ```
- `GET` routes remain publicly accessible for read-only scenarios.
- Access tokens expire after the configured window (default 60 minutes); request a new token by logging in again.
- **Developer setup checklist**
  1. Copy environment template: `cp .env.example .env`
  2. Set `DATABASE_URL` (if not using SQLite) and a strong `JWT_SECRET_KEY`
  3. Start the API: `uvicorn app.main:app`
  4. Register a user (`POST /auth/register`), log in, and call protected routes with the Bearer token
- Always deploy behind HTTPS so tokens are never transmitted over plaintext connections.

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
   Adjust `DATABASE_URL` if you are not using the default SQLite database and set a strong value for `JWT_SECRET_KEY`.
5. **Run the development server**
   ```
   uvicorn app.main:app
   ```
6. **Smoke test the API**
   Visit http://localhost:8000/health or run:
   ```
   curl http://localhost:8000/health
   ```
   Expect: `{"status":"ok"}`

---

## Environment Variables
| Name | Description | Example |
| --- | --- | --- |
| `DATABASE_URL` | SQLAlchemy connection string; defaults to local SQLite database | `sqlite:///./dev.db` |
| `JWT_SECRET_KEY` | Long, random signing key used to secure JWT tokens | `super-long-random-string` |
| `JWT_ALGORITHM` | JWT signing algorithm; must match clients | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Minutes before issued access tokens expire | `60` |

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

## Authentication & Security
- Register accounts via `POST /auth/register`, then obtain JWT bearer tokens with `POST /auth/login`.
- Include the returned token in the `Authorization: Bearer <token>` header when calling any write route (e.g., `POST /api/rentals`); read-only `GET` routes remain public.
- Login and registration endpoints are rate limited to five requests per minute per client IP.

> **Deployment note:** Always front this API with HTTPS (for example, via a TLS-terminating reverse proxy such as Nginx or a managed load balancer) and redirect any plain HTTP traffic at the edge before it reaches the application server.

---

## Development Workflow
Keep the workflow simple and predictable:
- Open an **Issue** for each piece of work.
- Branch from `master` using the format `feature/issue-#/short-name`, `bugfix/issue-#/short-name`, or `chore/issue-#/short-name`.
- Open a **Pull Request** that references the Issue (`Closes #<issue-number>`).
- Merge when checks pass; the Issue will close automatically.
- Keep the GitHub Project board in sync (To Do → In Progress → Done).

---

## Deployment
- Terminate TLS in front of the API (e.g., managed HTTPS on Render, Railway, Vercel, or a reverse proxy) and redirect any HTTP traffic to HTTPS.
- Keep the `.env` file and its secrets out of version control and deployment logs.
- Run the app with debug tooling disabled and without auto-reload in production.
- Restrict CORS to the trusted frontend origins defined in `app.main`.
- Rotate JWT signing keys on a regular cadence and revoke tokens if keys are compromised.
