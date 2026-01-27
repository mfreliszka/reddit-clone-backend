# DEVELOPMENT_PLAN.md

## 1. Project Overview & Architecture

**Goal:** Build a production-grade Reddit clone with a "Full Async-First" Python backend (Litestar) and a React frontend.
**Agentic Workflow:** The project will be executed by an AI agent, following the *PRAR Protocol* (Perceive, Reason, Act, Refine).

### Tech Stack
*   **Backend:** Litestar, Granian (server), asyncpg (driver), msgspec (serialization).
*   **Database:** Neon (Serverless PostgreSQL) + Piccolo ORM.
*   **Frontend:** React + Vite + TailwindCSS.
*   **Infrastructure:** Google Cloud Run (target).

---

## 2. Phase 1: API Core & User System

**Objective:** specific basic user management and authentication.

### 2.1. Database Schema
*   [ ] **Initialize Piccolo**: specific `piccolo_conf.py` and `app/db.py` (already likely done, verify).
*   [ ] **Table: `User`** (`app/models/user.py`)
    *   Fields: `username` (unique), `email` (unique), `password_hash`, `created_at`, `avatar_url`.
*   [ ] **Command**: `uv run piccolo migrations new app_name --auto` -> `uv run piccolo migrations forwards all`.

### 2.2. Services & Logic (`app/services/user_service.py`)
*   [ ] **Hashing**: Implement robust password hashing (e.g., `passlib` or `argon2-cffi`).
*   [ ] **Auth Logic**: `register_user()`, `authenticate_user()`.
*   [ ] **DTOs**: Ensure `msgspec.Struct` is used for `UserRegisterDTO`, `UserLoginDTO`, `UserResponseDTO`.

### 2.3. Controllers (`app/controllers/user.py`)
*   [ ] `POST /api/users/register`: Create new user.
*   [ ] `POST /api/users/login`: Return JWT or Session cookie.
*   [ ] `GET /api/users/me`: Get current user profile (protected).
*   [ ] `GET /api/users/{username}`: Public user profile.

### 2.4. Verification (`tests/`)
*   [ ] Test registration flow.
*   [ ] Test login with valid/invalid credentials.
*   [ ] specific token persistence.

---

## 3. Phase 2: Core Domain - Reddits & Posts

**Objective:** specific communities and the ability to post content.

### 3.1. Database Schema
*   [ ] **Table: `Subreddit`** (`app/models/subreddit.py`)
    *   Fields: `name` (unique), `description`, `creator_id` (FK -> User).
*   [ ] **Table: `Post`** (`app/models/post.py`)
    *   Fields: `title`, `content` (text/json), `subreddit_id` (FK), `author_id` (FK), `created_at`.

### 3.2. Services (`app/services/content_service.py`)
*   [ ] **Subreddit Logic**: Create, List, Join (optional for now).
*   [ ] **Post Logic**: Create post in subreddit, validate author.
*   [ ] **Feed Logic**: Basic `SELECT * FROM post ORDER BY created_at DESC`.

### 3.3. Controllers
*   [ ] **`app/controllers/subreddit.py`**
    *   `POST /api/subreddits/`: Create community.
    *   `GET /api/subreddits/`: List all.
    *   `GET /api/subreddits/{name}`: Get details.
*   [ ] **`app/controllers/post.py`**
    *   `POST /api/subreddits/{name}/posts`: Create post.
    *   `GET /api/posts/{id}`: Get single post.
    *   `GET /api/posts/feed`: Global feed (paginated).

---

## 4. Phase 3: Social Interactions (Votes & Comments)

**Objective:** Add engagement features to make it a social platform.

### 4.1. Database Schema
*   [ ] **Table: `Vote`** (`app/models/vote.py`)
    *   Fields: `user_id` (FK), `post_id` (FK, nullable), `comment_id` (FK, nullable), `value` (+1/-1).
    *   Constraint: Unique(user, post) / Unique(user, comment).
*   [ ] **Table: `Comment`** (`app/models/comment.py`)
    *   Fields: `content`, `author_id` (FK), `post_id` (FK), `parent_id` (FK, nullable, for nesting).

### 4.2. Services (`app/services/interaction_service.py`)
*   [ ] **Voting**: Handle upsert logic (if already voted, update/remove). Recalculate scores.
*   [ ] **Commenting**: Handle threaded comments (adjacency list or recursive CTE query).

### 4.3. Controllers
*   [ ] **`app/controllers/vote.py`**: `POST /api/posts/{id}/vote`.
*   [ ] **`app/controllers/comment.py`**:
    *   `POST /api/posts/{id}/comments`: Add comment.
    *   `GET /api/posts/{id}/comments`: Get tree of comments.

---

## 5. Phase 4: Frontend Implementation

**Objective:** Build a React UI to consume the API.

### 5.1. Setup
*   [ ] Initialize Vite project (`npm create vite@latest frontend -- --template react-ts`).
*   [ ] Configure TailwindCSS.
*   [ ] Setup `axios` or `fetch` wrapper with base URL.

### 5.2. Features
*   [ ] **Auth Context**: Store token, handle login/logout state.
*   [ ] **Pages**:
    *   `CreateAccount` / `Login`.
    *   `Home`: Main feed.
    *   `Subreddit`: View specific community.
    *   `PostDetail`: View post + comments.

### 5.3. Integration
*   [ ] Connect Register/Login forms.
*   [ ] Display Feed with infinite scroll or pagination.
*   [ ] Implement Upvote/Downvote buttons (opt: optimistic UI updates).
*   [ ] Comment tree rendering.

---

## 6. Execution Strategy for AI Agent

1.  **Read `GEMINI.md`** before every task to ensure compliance.
2.  **Schema First**: always define `app/models/` first.
3.  **Service Second**: implement logic in `app/services/`.
4.  **Controller Last**: expose via Litestar in `app/controllers/`.
5.  **Docstrings Required**: Every class, method, and function MUST have a docstring explaining its purpose, arguments, and return values.
6.  **Variable Typing**: All variables must have type hints like for example `elements: List[dict[str, int | None]] = []`.
7.  **Variable Naming**: Use descriptive variable names like for example `elements` instead of `e`.
8.  **Type Hinting**: Don't use `Any` type hint. Don't use `Optional` type hint, use `... | None` type hint instead.
9.  **Strict Typing**: Check types.
10. **Tests**:
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
11.  **Update `DEVELOPMENT_JOURNAL.md`** after every task and add/change information about what and how development have been done.