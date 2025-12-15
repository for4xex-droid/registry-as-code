# AI-Native Project

## Overview
(Brief description of the project goal.)

## Architecture
- **Core:** Pure business logic. `Result` pattern only. No Exceptions.
- **Infrastructure:** External adapters (DB, API, IO).
- **Interface:** Entry points (CLI, API).

## Commands
- Setup: `make setup`
- Run: `make run`
- Test: `make test`

## Rules for AI
- Read `.agent/rules.md` carefully.
- No `print()`, No `raise`, No Global `random`.
