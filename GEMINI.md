# GEMINI.md

# Project: Litestar Reddit Clone (Udemy Course)

## 🎯 Core Objectives

* **Primary Goal:** Build a production-grade, high-performance Reddit clone API and frontend to demonstrate modern Python web development.
* **Target Audience:** Udemy students and intermediate/senior Python developers.
* **Key Success Metrics:** - Full asynchronous execution from request to database.
* Low-latency response times using `msgspec` and `asyncpg`.
* Seamless deployment to Google Cloud Run with Neon Postgres.



---

## 🛠 Tech Stack & Standards

* **Runtime:** Python 3.12+ (emphasizing performance and type safety).
* **Frameworks:** Litestar (Backend), React + Vite (Frontend).
* **Database:** Neon PostgreSQL (Serverless) using Piccolo ORM.
* **Serialization:** `msgspec` (Strictly preferred over Pydantic).
* **Server:** Granian (Rust-based ASGI server) with `uvloop`.
* **Driver:** `asyncpg` (Direct binary protocol for PostgreSQL).

---

## 🤖 AI Behavior & Directives

Follow these rules strictly when interacting with this codebase:

1. **The PRAR Protocol:**
* **Perceive:** Scan `app/models/` for table definitions and `app/dtos/` for existing schemas before proposing API changes.
* **Reason:** Explain architectural choices, specifically regarding async safety and serialization efficiency.
* **Act:** Provide code snippets that adhere to the modular monolith structure.
* **Refine:** Ensure all code passes strict type-checking and adheres to the "Full Async-First" rule.


2. **Code Style:**
* **Async-First:** Never use blocking libraries. Use `httpx` for external requests and `anyio` for file/time operations.
* **Performance First:** Prefer `msgspec.Struct` for data validation.
* **Piccolo Patterns:** Use Piccolo's query builder; avoid raw strings for SQL to maintain migration integrity.
* **Type Safety:** Ensure 100% type coverage for all service and controller methods.
* **Documentation:** Each class, method, and function must have a docstring.
* **Variable Method Types:** Each variable must have a type defined (e.g., `users: list[dict[int, str | None]]`).
* **Return Types:** Each function and method must have a return type defined (e.g., `-> list[dict[int, str | None]]`).


3. **Terminal Execution:**
* **uv run:** Usage of any terminal command related to this project must be preceded by `uv run` (e.g., `uv run piccolo migrations ...`).

4. **Workspace Memory:**
* Document any performance bottlenecks or common student pitfalls in a specialized `COURSE_NOTES.md`.
* Maintain a list of specific Neon-Postgres quirks (e.g., connection string SNI requirements) for troubleshooting.

5. **Testing:**
* each endpoint should have a corresponding test file in the `tests` directory.
* each endpoint should be covered by at least one test, ideally multiple tests.
* each test file should cover the happy path and at least one edge case.
* each test should rely on mocked data, mocked functions and mocked database
* each test file should be able to run in isolation.
* each test file should be able to run in parallel.
* each endpoint test should be using syrupy snapshot assertion - something like this:
```python
assert response.json() == snapshot
```
* each endpoint test should have expected status code check:
```python
assert response.status_code == HTTPStatus.OK
```


---

## 📂 Project Map (Critical Paths)

* `app/controllers/`: Route handlers (API Interface layer).
* `app/services/`: Pure business logic (Reddit domain logic like following, feed generation).
* `app/models/`: Piccolo Table definitions (Postgres schema).
* `app/dtos/`: Validation schemas using `PiccoloDTO` and `msgspec`.
* `frontend/src/`: React application source code.
* `migrations/`: Piccolo auto-generated migration files.
* `static/`: Production-ready frontend assets.

---

## ⚙️ Operational Commands

* **Install Dependencies:** `pip install -r requirements.txt`
* **Development (Backend):** `litestar run --reload`
* **Development (Frontend):** `cd frontend && npm run dev`
* **Database Migration (New):** `piccolo migrations new app_name --auto`
* **Database Migration (Apply):** `piccolo migrations forwards all`
* **Production Server:** `granian --interface asgi app:app --host 0.0.0.0 --port 8080`

---

## 🚫 Constraints (The "Never" List)

* **NEVER** use synchronous database drivers or the `psycopg2` (legacy) driver.
* **NEVER** use Pydantic unless a legacy third-party dependency requires it.
* **NEVER** write business logic inside the Controllers; keep it in the Services layer.
* **NEVER** hardcode the Neon database password; use environment variables or Secret Manager.
* **NEVER** manually edit files in the `migrations/` folder.

---

**Would you like me to generate the initial `app/models/user.py` file to get your Piccolo schema started according to these rules?**