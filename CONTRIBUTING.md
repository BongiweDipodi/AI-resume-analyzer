# Contributing to ResumeMatch AI

Thank you for your interest in contributing. This project follows production-grade practices: tests, linting, and CI must pass before merge.

## Development setup

```bash
git clone https://github.com/dondolo2/AI-resume-analyzer.git
cd AI-resume-analyzer
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
python -m spacy download en_core_web_sm
cp .env.example .env
```

## Running tests

```bash
pytest tests/ -v --cov=app --cov-fail-under=85
```

## Code style

- Format with **Black** (line length 88)
- Lint with **flake8**
- Type-check with **mypy** (`--ignore-missing-imports`)
- Google-style docstrings on public functions and classes
- Type hints on all function signatures

```bash
black app tests
flake8 app
mypy app --ignore-missing-imports
```

## Pull request checklist

- [ ] Tests pass locally
- [ ] Coverage remains ≥ 85%
- [ ] New features include unit tests
- [ ] README or docs updated if behavior changes
- [ ] Commit messages use conventional style (`feat:`, `fix:`, `docs:`)

## Architecture

Place business logic in `app/core/`, orchestration in `app/services/`, and I/O in `app/utils/`. See [docs/architecture.md](docs/architecture.md).
