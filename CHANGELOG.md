## [feature/issue-6-bikes-refactor] - 2025-10-29
**Summary:** Converted the project from scooters to bikes and replaced scooter references with Bike model and data persistence.

**Changes**
- app.py: replaced all scooter logic with Bike terminology and updated data access
- bike_db.json: created as new backing store for bike data
- README.md: updated to describe bikes instead of scooters
- tests/test_placeholder.py: added placeholder test to ensure pytest passes

**Verification**
- grep -R "scooter" app/ → no matches
- pytest → all tests passing

---

## [feature/issue-5-db-models] - 2025-10-28
**Summary:** Added SQLAlchemy models and Alembic setup for bikes, users, and rentals to initialize the database schema.

**Changes**
- app/models/bike.py: added Bike model with AvailabilityStatus enum and rental relationship
- app/models/user.py: defined User model with unique email and rental relationship
- app/models/rental.py: created Rental model linking bikes and users with pricing and timestamps
- app/models/__init__.py: exported Base
- alembic/env.py, alembic/versions/879c2c21ff31_create_initial_tables.py: initialized Alembic migration
- .gitignore: added dev.db
- README.md, script.py.mayo: updated references for database setup

**Verification**
- .venv/bin/alembic upgrade head → created tables in dev.db
- confirmed tables present via SQLite inspection

---

## [chore/issue-4-init-backend] - 2025-10-27
**Summary:** Set up FastAPI backend scaffolding with environment config and health route to replace Flask setup.

**Changes**
- app/main.py: added FastAPI app with /health route returning {"status": "ok"}
- app/db.py: configured Base, engine, and SessionLocal
- .env.example: created template with DATABASE_URL
- requirements.txt: replaced Flask dependencies with FastAPI stack
- app/models/, app/schemas/, app/routers/, app/services/: created empty directories for project organization

**Verification**
- uvicorn app.main:app → confirmed /health returns {"status": "ok"}
- project runs successfully without Flask dependencies

---
