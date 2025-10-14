SHELL := /bin/bash

.PHONY: dev api fe migrate seed test fmt

dev:
\t(cd api && uvicorn app.main:app --reload) & (cd frontend && pnpm dev)

api:
\tcd api && uvicorn app.main:app --reload

fe:
\tcd frontend && pnpm dev

migrate:
\tcd api && alembic upgrade head

seed:
\tcd api && python -m app.scripts.etl_nightly --seed

test:
\tcd api && pytest -q

fmt:
\tcd api && ruff check . --fix || true
