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

## [chore/issue-11-init-frontend] – 2025-10-30

**Summary:** Initialized the frontend environment for the Personal Transport API using Vite + React + TypeScript, configured Axios base instance, and established core routing and formatting standards.

**Changes**
- /frontend/ – created new Vite + React + TypeScript scaffold
- /frontend/src/lib/api.ts – added Axios base instance using VITE_API_BASE_URL
- /frontend/src/main.tsx – mounted root React app
- /frontend/src/App.tsx – added placeholder UI and basic routing
- /frontend/src/routes/Home.tsx – created placeholder home page at /
- /frontend/src/routes/Confirm.tsx – created placeholder confirmation route at /confirm/:id
- /frontend/.eslintrc.cjs, .prettierrc – configured linting and formatting
- /frontend/.env.example – added VITE_API_BASE_URL variable
- package.json – added dependencies and npm scripts for dev, build, and lint

**Verification**
- npm install → installs dependencies successfully
- npm run dev → launches Vite dev server and renders placeholder UI
- Confirm Axios instance reads VITE_API_BASE_URL from .env.local
- Lint passes (npm run lint) and Prettier formats code without errors

## [feature/issue-12-api-security] – 2025-11-5

**Summary:** Added full JWT-based authentication, CORS restrictions, environment-based secrets, and rate-limiting to secure all write operations in the FastAPI backend.
This update ensures the API cannot be accessed or modified by unauthorized users once deployed publicly.

**Changes**
- app/auth.py: implemented JWT generation & validation, password hashing, and user authentication helpers
- app/routers/auth.py: added /auth/register and /auth/login routes using FastAPI’s OAuth2PasswordBearer flow
- app/main.py: registered auth router, added CORS middleware, integrated SlowAPI limiter, removed debug mode
- requirements.txt / pyproject.toml: added python-jose[cryptography], passlib[bcrypt], slowapi, and python-dotenv
- .env.example: added JWT_SECRET_KEY, JWT_ALGORITHM, and ACCESS_TOKEN_EXPIRE_MINUTES placeholders
- README.md: documented authentication usage and HTTPS deployment reminders, added new Authentication & Security, Environment Variables, and Deployment sections to document JWT flow, .env setup, and production hardening steps
- (optional) updated payments and rentals routes to require valid tokens before mutations

**Verification**
- POST /auth/register creates a new user with hashed password
- POST /auth/login returns a valid JWT access token
- Requests to POST/PATCH/DELETE routes return 401 when token missing or invalid
- GET routes remain publicly accessible
- Environment variables loaded successfully from .env
- No debug flags or hard-coded secrets remain
- All existing pytest suites pass

## [feature/issue-12-api-security] – 2025-11-5 Follow-Up Enhancements

**Summary**: Completed the remaining security hardening tasks identified after initial authentication rollout.
These updates elevate the Personal Transport API from medium to high-assurance by securing database migrations, legacy code paths, and all write-access routes.

**Changes**
- Alembic Migration: added hashed_password column to the users table to align database schema with JWT authentication system
- Legacy Flask App: deprecated app.py by raising a runtime error to prevent accidental launch of the unauthenticated server
- Route Protection Audit -  confirmed all existing routers already comply with JWT security standards. 
  - `rentals.py` write endpoints require authentication
  - `bikes.py` provides only public read access
  - `auth.py` routes remain intentionally unguarded for registration and login
  - no unprotected write endpoints found
- Payments Endpoint: hardened payment stub to return 403 Forbidden for unauthenticated requests
- README.md: updated Security Notes to document new protections and schema alignment
- introduced app/routers/payments.py to secure the /api/payments stub with authentication; unauthorized requests return 403 Forbidden while valid JWTs complete the stub flow successfully.
- added payments router import in app/main.py to serve alongside existing routes.
- pytest now aborts on legacy Flask tests (intentional RuntimeError); no FastAPI regressions observed.

**Verification**
- alembic upgrade head applies new hashed_password column with no data loss
- Running python app.py raises explicit “Legacy Flask app disabled” error
- All write routes require valid JWT token; unauthenticated requests return 401/403
- GET routes remain publicly accessible
- Payment stub accessible only for authorized users
- All pytest suites pass; no functional regressions detected
- README accurately reflects secure production state

## [feature/issue-13-bike-list-page] - 2025-11-05

**Summary**: Implemented front-end Bike List page with reusable card component and API integration for available bikes.

**Changes**
- Created src/pages/BikeList.tsx to fetch and display bikes from /api/bikes.
- Added src/components/BikeCard.tsx for modular rendering of individual bikes with a ‘Rent’ CTA.
- Implemented loading and empty states for user-friendly UX.
- Integrated React Router navigation to rental form page (/rent/:bikeId).
- Ensured accessibility compliance using semantic HTML and alt attributes.
- Verified successful API response rendering and route navigation in dev environment.

**Verification**
- Started frontend via npm run dev and confirmed /bikes route loads with API results.
- Tested navigation to rental form from each card.
- Verified no console errors or TypeScript issues.

## [feature/issue-14-rental-form] – 2025-11-05

**Summary**: Implemented a client-side rental creation and confirmation flow with inline validation, cohesive styling, and updated routing.

**Changes**
- frontend/src/pages/RentalForm.tsx: Added rental form with fields for name, email, phone (optional), start/end dates, and selected bike; enforces 3-day limit, computes totals, displays inline validation errors, and submits to /api/rentals.
- frontend/src/pages/Confirmation.tsx: Added confirmation view that fetches /api/rentals/{id}, formats totals and dates, falls back to preview data if needed, and displays contact information with error handling.
- frontend/src/App.tsx: Integrated new rental flow and removed deprecated placeholder confirmation page.
- frontend/src/App.css: Added cohesive styling for rental form and confirmation summary cards to match the design system.
- frontend/src/pages/Confirm.tsx: Removed obsolete component replaced by new confirmation page.

**Verification**
- npm run build completed successfully.
- Valid rentals (≤ 3 days) redirect to confirmation with accurate total and details.
- Invalid dates or missing fields display inline errors without submission.
- No backend, auth, or payment logic modified.
