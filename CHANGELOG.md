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

## [feature/issue-7-schemas-repositories] - 2025-10-29
**Summary:** Implemented Pydantic v2 schemas and repository helpers for bikes, users, and rentals to establish a clean, modular data layer.

**Changes**
- app/schemas/bike_schema.py: added BikeCreate and BikeRead schemas with AvailabilityStatus enum and ConfigDict(from_attributes=True) for ORM compatibility
- app/schemas/user_schema.py: added UserCreate and UserRead schemas including optional phone field
- app/schemas/rental_schema.py: added RentalCreate and RentalRead schemas covering date fields and created_at on the read model
- app/repositories/bike_repo.py: implemented create_bike, get_bike_by_id, and get_all_bikes using SQLAlchemy 2.0-style queries
- app/repositories/user_repo.py: implemented create_user, get_user_by_id, and get_all_users helpers
- app/repositories/rental_repo.py: implemented create_rental, get_rental_by_id, and get_all_rentals helpers
- app/repositories/init.py: declared repositories package for import consistency

**Verification**
- python3 -m app.schemas.* and python3 -m app.repositories.* → all modules import successfully
- pytest → no import or schema mismatches detected

## [feature/issue-8-rental-service] - 2025-10-30
**Summary:** Implemented and tested pure business logic for rental validation and pricing.

**Changes**
- app/services/rental_service.py: added functions for validating date ranges, computing total price, and checking availability
- tests/test_rental_service.py: full coverage for valid/error paths and mixed input types

**Verification**
- pytest confirms all branches and error conditions pass
- all functions deterministic, with no database or HTTP interactions

## [feature/issue-9-bikes-router] - 2025-10-30
**Summary:** Implemented a read-only /api/bikes endpoint to expose all available bikes.

**Changes**
- app/routers/bikes.py: added GET /api/bikes route using get_available_bikes() and BikeRead schema.
- app/repositories/bike_repo.py: introduced get_available_bikes() query filtering bikes by AvailabilityStatus.AVAILABLE.
- app/main.py: registered the bikes router for /api/bikes routes.

**Verification**
- Run uvicorn app.main:app --reload and confirm GET /api/bikes returns an HTTP 200 JSON array of available bikes.
- Optionally seed a few available bikes to verify non-empty responses.
  
## [feature/issue-10-rentals-router] - 2025-10-30
**Summary:** Implemented rentals API routing for creating and retrieving rental records, leveraging the service layer for validation, pricing, and consistent error handling.

**Changes**
- app/routers/rentals.py: added POST /api/rentals and GET /api/rentals/{id} endpoints with validation, availability checks, computed pricing, and structured JSON error responses.
- app/main.py: registered the rentals router so endpoints are served under `/api/rentals`.

**Verification**
- Run `uvicorn app.main:app --reload` and test:
  - ✅ `POST /api/rentals` → returns 200 with `RentalRead` for valid requests.  
  - ❌ Invalid range → 400 `INVALID_RANGE`.  
  - ❌ Bike unavailable → 409 `UNAVAILABLE`.  
  - ❌ Missing rental ID → 404 `NOT_FOUND`.  
- `pytest` confirms no regressions and validates core service logic.

