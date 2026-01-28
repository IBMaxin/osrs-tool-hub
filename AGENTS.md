# AGENTS.md — OSRS Tool Hub (Authoritative Agent Instructions)

You are working inside a mature, highly-tested monorepo.
Your primary responsibility is to **extend or modify the system without breaking contracts, degrading quality, or introducing hidden risk**.

This repository prioritizes:
- Backward compatibility
- Explicit contracts
- High test coverage
- Minimal, intentional diffs

You are not here to “clean up” or refactor unless explicitly instructed.

---

## Repo map (ground truth)

### Backend (FastAPI + SQLModel, Python ^3.13)
- Routes (thin only): `backend/api/v1/**`
- API schemas / contracts:
  - `backend/api/v1/schemas.py`
  - `backend/api/v1/gear/schemas.py`
- Business logic: `backend/services/**`
- DB + sessions: `backend/db/**`
- App wiring (factory, middleware, scheduler): `backend/app/**`
- Static data: `backend/data/**`
- Tests:
  - Unit: `backend/tests/services/**`
  - API / contract: `backend/tests/api/**`
  - Integration: `backend/tests/test_integration_*`
  - E2E: `backend/tests/e2e/**`, `backend/tests/test_e2e_*.py`

### Frontend (React 18 + TypeScript strict + Vite)
- Feature code: `frontend/src/features/**`
- Typed API client: `frontend/src/lib/api/**`
- Shared hooks/components/utils: `frontend/src/lib/**`
- Theme: `frontend/src/theme/osrs-theme.ts`
- Tests: `frontend/src/test/**`

**Do not reorganize this structure.**

---

## Operating modes (mandatory)

Every response MUST begin by selecting **exactly one** mode:

- `MODE: ANALYSIS_ONLY`
- `MODE: SAFE_PATCH`
- `MODE: FEATURE_ADD`

If the user does not specify a mode, default to **MODE: ANALYSIS_ONLY**.

### MODE: ANALYSIS_ONLY
Allowed:
- Inspect code
- Explain behavior
- Propose plans and diffs

Forbidden:
- Writing or editing files

---

### MODE: SAFE_PATCH
Purpose: fix bugs or correctness issues with the smallest possible diff.

Allowed:
- Bug fixes
- Targeted internal refactors strictly required for the fix
- Adding or adjusting tests

Forbidden:
- Moving or renaming files/directories
- Renaming/removing routes or response fields
- DB schema changes
- Changing global error schema
- Unrelated formatting or cleanup

---

### MODE: FEATURE_ADD
Purpose: add **new, additive functionality only**.

Allowed:
- New endpoints
- New optional fields
- New modules or services

Required:
- Backward-compatible API changes only
- Full test coverage for new behavior

Forbidden:
- Removing or renaming existing endpoints or fields
- Breaking frontend contracts
- Architectural refactors

---

## Non-negotiables (hard rules)

### Backward compatibility
- Never remove or rename:
  - API routes
  - Request fields
  - Response fields
  - Shared TypeScript types
- Changes must be **additive only** unless explicitly approved.

### Error schema is locked
- All errors must conform to `ErrorResponse` / `ErrorDetail`.
- Do not introduce alternative error formats.
- Routes must declare `response_model` where applicable.

### No “cleanup refactors”
- Do not reformat files, rename symbols, or reorganize folders “for clarity”.
- Only touch what the task explicitly requires.

### Tests are mandatory
If behavior changes, tests must prove:
- Happy path
- Validation failure
- Service/error path (where applicable)
- Contract stability for public APIs

---

## Code quality standards (must enforce)

### General
- Prefer small, composable functions.
- Keep diffs minimal and intentional.
- No dead code.
- No silent behavior changes.

### Python (backend)
- Type hints everywhere (public functions, services, routes).
- Docstrings for non-trivial public functions (Google style preferred).
- No broad `except Exception` unless re-raised with context and tests.
- Logging:
  - Use project logger only.
  - Never log secrets, tokens, or user identifiers.
- Validation:
  - Validate inputs at boundaries (routes/validators).
  - Service layer assumes validated inputs.
- Routes must be thin:
  - request → validate → service → response model

### TypeScript (frontend)
- TypeScript strict:
  - No `any`
  - No unsafe casts (`as unknown as`)
  - No suppression comments unless explicitly justified
- All API calls go through the typed client (`frontend/src/lib/api/**`).
- No direct fetch/axios usage in components.
- UI must remain consistent with Mantine + OSRS theme.

---

## CI-mirrored quality gates (definition of done)

You must behave **as if CI is running and blocking you**.

If you cannot reasonably argue that CI would pass, you are not done.

### Backend gates
- `poetry run ruff check .`
- `poetry run black --check .`
- `poetry run mypy .`
- `poetry run pytest`

### Frontend gates
- `cd frontend && npm run lint`
- `cd frontend && npm run build`
- `cd frontend && npm run test:run`

Rules:
- Do not bypass or weaken these checks.
- If a command cannot be executed in-context, state that explicitly and still reason about pass/fail.
- Fix failures in the same change; do not defer.

---

## Required workflow (PLAN → ACT → VERIFY → REVISE)

For `SAFE_PATCH` and `FEATURE_ADD`, every response must follow:

### PLAN
- Files to touch (minimal)
- Contracts that must remain stable
- Test strategy

### ACT
- Exact diffs or full file replacements
- Only planned files may change

### VERIFY
- List the exact CI-mirrored commands required
- State assumptions if verification cannot be run

### REVISE
- Fix anything that would fail
- No follow-up “cleanup” passes

---

## Release-safe feature checklist (mandatory for FEATURE_ADD)

Before considering a feature complete, verify **all** of the following:

### API & contracts
- [ ] No existing endpoint removed or renamed
- [ ] No existing request/response field removed or changed type
- [ ] New fields are optional or additive
- [ ] Error responses still match `ErrorResponse`

### Backend correctness
- [ ] New logic covered by unit tests
- [ ] Validation failures tested
- [ ] Service errors tested
- [ ] No broad exception swallowing

### Frontend safety
- [ ] Frontend types updated if API touched
- [ ] No `any` or unsafe casts introduced
- [ ] Hooks still compile and typecheck
- [ ] UI handles new optional fields safely

### Data & state
- [ ] No silent DB schema changes
- [ ] Defaults exist for new fields
- [ ] Existing data continues to load correctly

### CI readiness
- [ ] Ruff passes
- [ ] Black passes
- [ ] MyPy passes
- [ ] Pytest passes
- [ ] Frontend lint/build/tests pass

If any box is unchecked, the feature is **not release-safe**.

---

## Output requirements (strict)

### SAFE_PATCH or FEATURE_ADD
Every response MUST include:
1. MODE
2. PLAN
3. ACT (diffs or files)
4. VERIFY commands
5. Risk check (contracts, data, frontend, tests)

### ANALYSIS_ONLY
- MODE
- Findings
- Recommended plan
- No code edits

---

## Prohibited changes (auto-reject)
- Renaming or moving directories/files
- Changing `/api/v1` behavior globally
- Altering error response shape
- Introducing `any` in TypeScript
- Removing existing endpoints or fields
- Silent DB schema changes

---

End of AGENTS.md
