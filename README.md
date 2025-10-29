## Personal Transport API

A lightweight REST API for managing personal transport rentals — including bikes, scooters, and future vehicle types.
Built for clarity, simplicity, and collaborative development.
---

## Features

- CRUD endpoints for bikes and rentals
- JSON-based REST architecture
- Clean GitHub workflow (Issues → Branches → PRs → Merge)
- Project board flow: To Do → In Progress → Done
- Modular foundation for future expansion

### Planned Enhancements
- Migration to **FastAPI** for async + auto-docs
- Authentication & Authorization
- Payments and transaction tracking
- Availability and inventory management logic
- Automated test suite and CI integration
---

### Tech Stack
- **Python 3.10+**
- **Flask**
- **JSON REST API**
- **GitHub Projects + Actions**
---

## Getting Started
If you’re setting this up for the first time, follow these steps exactly.

### 1) Clone
git clone https://github.com/MelEUsher/PersonalTransportAPI.git
cd PersonalTransportAPI

### 2) Create & activate a virtual environment

**macOS/Linux**
python3 -m venv .venv
source .venv/bin/activate
**Windows (CMD)**
python -m venv .venv
.venv\Scripts\activate

### 3) Install dependencies
pip install -r requirements.txt

### 4) Run the app
Preferred:
python app.py

Alternative:
# macOS/Linux
export FLASK_APP=app.py
flask run --port 5000

# Windows CMD
set FLASK_APP=app.py
flask run --port 5000

# Windows PowerShell
$Env:FLASK_APP="app.py"
flask run --port 5000
Visit: http://localhost:5000

## Project Structure

PersonalTransportAPI/
├─ .github/
│  ├─ ISSUE_TEMPLATE/
│  │  ├─ config.yml
│  │  └─ task.md
│  ├─ workflows/
│  └─ pull_request_template.md
├─ app/
│  ├─ __init__.py
│  ├─ routes/
│  │  ├─ bikes.py
│  │  ├─ rentals.py
│  │  └─ __init__.py
│  ├─ models/
│  │  ├─ bike_model.py
│  │  ├─ rental_model.py
│  │  └─ __init__.py
│  └─ utils/
│     ├─ helpers.py
│     └─ __init__.py
├─ tests/
│  ├─ __init__.py
│  └─ test_routes.py
├─ app.py
├─ app.json
├─ CONTRIBUTING.md
├─ Procfile
├─ requirements.txt
├─ scooter_db.json
└─ .gitignore


## Development Workflow
Keep it simple and consistent.

### 1) Create an Issue
Each new task starts as an Issue using the Task template.
Track it in the GitHub Project board.
### 2) Create a branch
Use strict naming:
feature/issue-##
bugfix/issue-##
chore/issue-##

Examples:
feature/issue-12-rentals-endpoint
bugfix/issue-7-auth-timezone
chore/issue-3-readme-update

CLI:
git checkout master
git pull
git checkout -b feature/issue-12-rentals-endpoint

### 3) Do the work, commit small, push
git add .
git commit -m "Issue #12: implement /rentals endpoints and validation"
git push -u origin feature/issue-12-rentals-endpoint

### 4) Open a Pull Request
In your PR description, include:
Closes #<issue-number>
GitHub will automatically close the Issue when the PR merges.

### 5) Merge process
PR review required — direct pushes to master are disabled.

## Working With the Project Board
- New Issues auto-add to the Project
- Move Issues manually between To Do, In Progress, and Done
- Simplicity over automation — manual tracking is expected

## Testing
(Placeholder — test suite integration coming soon)

Expected:
pytest -q
or
make test

### Contributing

See **CONTRIBUTING.md** for:
- Branch naming conventions
- Issue → Branch → PR workflow
- Review and merge checklist

### License
If a LICENSE file is added, it will be referenced here.

### Project History
This repository began as a fork of KaranErry/scooterAPI.
It’s now evolving into a Personal Transport API —
a unified, modernized backend for managing small vehicle rentals (bikes, scooters, etc.).
Current owner & direction: Mel Usher
Repository: MelEUsher/PersonalTransportAPI
