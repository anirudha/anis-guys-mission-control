# Repository Guidelines

## Project Structure & Module Organization
- `backend/`: FastAPI service. App code lives in `backend/app/` (routes in `backend/app/api/`, models in `backend/app/models/`, schemas in `backend/app/schemas/`, workers in `backend/app/workers/`). DB migrations are in `backend/alembic/` (generated files in `backend/alembic/versions/`).
- `frontend/`: Next.js app. Routes live in `frontend/src/app/`; shared UI in `frontend/src/components/`; utilities in `frontend/src/lib/`; generated API client in `frontend/src/api/generated/` (do not edit by hand).
- `templates/`: shared templates packaged into the backend image (used by gateway integrations).
- `docs/`: protocol/architecture notes (see `docs/openclaw_gateway_ws.md`).

## Build, Test, and Development Commands
From repo root:
- `make setup`: install/sync backend + frontend dependencies.
- `make check`: CI-equivalent suite (lint, typecheck, tests/coverage, frontend build).
- `docker compose -f compose.yml --env-file .env up -d --build`: run full stack (includes Postgres + Redis).

Fast local dev loop:
- `docker compose -f compose.yml --env-file .env up -d db redis`
- Backend: `cd backend && uv sync --extra dev && uv run uvicorn app.main:app --reload --port 8000`
- Frontend: `cd frontend && npm install && npm run dev`

Other useful targets: `make backend-migrate` (alembic upgrade), `make api-gen` (regenerate TS client; backend must be running on `127.0.0.1:8000`).

## Coding Style & Naming Conventions
- Python: Black + isort (line length 100), flake8 (`backend/.flake8`), mypy is strict (`backend/pyproject.toml`). Prefer `snake_case` for modules/functions.
- TypeScript/React: ESLint (Next.js config) + Prettier (`make frontend-format`). Prefer `PascalCase` components and `camelCase` vars; prefix intentionally-unused destructured props with `_` (see `frontend/eslint.config.mjs`).
- Optional: `pre-commit install` to run formatting/lint hooks on commit.

## Testing Guidelines
- Backend: pytest in `backend/tests/` (files `test_*.py`); run `make backend-test` or `make backend-coverage` (writes `backend/coverage.xml`).
- Frontend: vitest + testing-library; prefer `*.test.ts(x)` near the code (example: `frontend/src/lib/backoff.test.ts`); run `make frontend-test` (writes `frontend/coverage/`).

## Commit & Pull Request Guidelines
- Use Conventional Commits (seen in history): `feat: ...`, `fix: ...`, `docs: ...`, `chore: ...`, `refactor: ...` with optional scope like `feat(chat): ...`.
- PRs should include: what/why, how to test (ideally `make check`), linked issue (if any), and screenshots for UI changes. Never commit secrets; use `.env.example` files as templates.
