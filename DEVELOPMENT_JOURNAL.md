# Development Journal

This document serves as a chronological log of the development process for the Litestar Reddit Clone Backend. It captures technical decisions, architecture implementations, challenges faced, and successful resolutions.
No debugging information should be added to this file.

---

## 📅 Phase 1: Foundation & User Identity

### 1. Project Initialization & Architecture
**Goal:** Establish a high-performance, async-first Python web framework setup.
- **Tech Stack Selection:**
    - **Framework:** `Litestar` (for speed and DI).
    - **ORM:** `Piccolo` (Async logic, simple migrations).
    - **Database:** Postgres (Neon).
    - **Validation/Serialization:** `msgspec` (Performance over Pydantic).
- **Configuration:**
    - Created `piccolo_conf.py` and `app/piccolo_app.py` to register the app with Piccolo's migration manager.
    - Set up `app/main.py` with Basic Litestar app structure, lifecycle hooks for DB connection pooling, and OpenAPI generation.

### 2. User Domain Implementation
**Goal:** Allow users to register, login, and view profiles.
- **Data Modeling (`app/models/user.py`):**
    - Defined `User` table.
    - **Challenge:** The table naming. Initially relying on default inference caused issues later. Eventually enforced `tablename="users"` to avoid collision with Postgres reserved keyword `user`.
- **Security:**
    - **Password Hashing:** Integrated `argon2-cffi` for secure password storage.
    - **JWT:** Implemented `app/services/auth_service.py` to issue Bearer tokens.
    - **Middleware:** Created `JWTAuthenticationMiddleware` (`app/middleware/auth.py`) to intercept requests, decode tokens, and inject the `User` object into `request.user`.
- **API Layers:**
    - **Service (`UserService`):** Encapsulated business logic (existence checks, hashing).
    - **Controller (`UserController`):** Handled HTTP concerns. Defined endpoints:
        - `POST /api/users/register`
        - `POST /api/users/login`
        - `GET /api/users/me` (Protected)
        - `GET /api/users/{username}`

### 3. Hardening & Refactoring (The "Strict" Standard)
**Goal:** Professional-grade type safety and testing.
- **Strict Typing:**
    - Removed broad types like `Any` or `Optional` in favor of precise unions (e.g., `str | None`).
    - Enforced return types on all functions.
- **Testing Architecture Pivot:**
    - **Initial State:** A single `tests/test_api.py`.
    - **Evolution:** Split into domain-specific directories (`tests/users/`).
    - **Snapshots:** Introduced `syrupy`. Instead of asserting every field manually, we verify the entire JSON response structure against a stored baseline (`assert response.json() == snapshot`).
    - **Async Fixtures:** Configured `tests/conftest.py` with `pytest-asyncio` strict mode to properly handle the Async `Litestar` app and `httpx.AsyncClient` lifecycle.

---

## 📅 Phase 2: Core Domain (Reddits & Posts)

### 1. Domain Modeling
**Goal:** Implement the "Reddit" part of the clone.
- **Subreddit Model (`app/models/subreddit.py`):**
    - Fields: `name` (Unique), `description`, `owner` (FK to User).
- **Post Model (`app/models/post.py`):**
    - Fields: `title`, `content`, `url`, `subreddit` (FK), `author` (FK).
- **Relationships:** Established Foreign Keys ensuring data integrity (e.g., Posts belong to Subreddits and Authors).

### 2. CRUD Implementation
- **Subreddit Service/Controller:**
    - Implemented `POST /api/subreddits` (Create Community).
    - Implemented `GET /api/subreddits/` (List) and `GET /api/subreddits/{name}`.
- **Post Service/Controller:**
    - Implemented `POST /api/r/{subreddit}/posts` (Contextual creation).
    - Implemented `GET /api/r/{subreddit}/posts` (List posts by subreddit).
    - Implemented `GET /api/posts/{id}` (Direct access).

---

## 📅 Phase 3: Standardization & Operational Excellence

### 1. Automation (`Makefile`)
**Goal:** Simplify developer experience.
- Created a `Makefile` to abstract complex commands:
    - `make migration-new`: Auto-generate migrations.
    - `make migrate`: Apply migrations.
    - `make test`: Run all tests.
    - `make test-snapshot`: Update snapshot baselines.
    - `make clean`: Remove pycache artifacts.

### 2. Comprehensive Testing Standards
**Goal:** Standardize how tests are written across the team (or future students).
- **Rule 1: Isolation.** One test file per endpoint (e.g., `test_create_post.py` is separate from `test_list_posts.py`).
- **Rule 2: HTTPStatus.** Used `http.HTTPStatus` constants (`HTTPStatus.CREATED`) instead of magic numbers (`201`).
- **Rule 3: Snapshots.** All endpoint tests verify full JSON payloads using `syrupy`.
- **Outcome:** A test suite with 100% endpoint coverage (happy paths + key edge cases) that runs in parallel and is easy to maintain.

### 3. Test Refactoring: Strict Unit Isolation
**Goal:** Transition from integration tests hitting the database to pure unit tests using mocks.
- **Tools:**
    - **`pytest-mock`:** Replaced direct calls with `mocker.patch`.
    - **`polyfactory`:** Used to generate robust, typed DTOs and Model instances for test data.
- **Architecture Change:**
    - **Lambda Providers:** Litestar's `dependencies` are evaluated at definition time. To enable runtime patching of services, we refactored Controllers to use a lambda indirection: `dependencies = {"service": Provide(lambda: provide_service())}`.
- **Outcome:** Tests are now fully isolated, faster, and do not require a running database container.

---

## Current Status
- **Core User System:** ✅ Complete & Verified.
- **Core Reddit Domain:** ✅ Complete & Verified.
- **Testing Infrastructure:** ✅ Robust & Standardized.
- **Next Steps:** Phase 3 - Social Interactions (Comments & Voting).
