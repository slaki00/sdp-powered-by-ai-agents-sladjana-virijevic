# BankOCR

A command-line tool that reads bank account numbers from OCR scan files and
produces a validated, human-readable result file. Built as the capstone project
for the course **Software Development Processes Powered by AI Agents** (LabSoft).
Every stage of the development lifecycle (Git workflow, architecture
documentation, requirements derivation, CI/CD pipeline, and test-driven
development) was driven by dedicated Kiro AI agents.

## What the kata solves

BankOCR is a classic coding kata. A bank scanner produces files where each
account number is drawn with pipe and underscore characters across three lines.
This program:

1. Parses each 27-character-wide, 3-line entry and maps the segments to digits.
2. Validates the nine-digit result with a weighted checksum (mod 11).
3. Labels entries as valid, `ERR` (bad checksum), or `ILL` (unreadable digit).
4. Attempts to auto-correct `ERR` and `ILL` entries by flipping exactly one
   segment; marks as `AMB` when more than one valid alternative exists.

Example output for a six-entry scan:

```
345882865
222222222 ERR
?00000000 ILL
664371485
123456789
490067715 AMB
```

## Tech stack and architecture overview

| Concern | Choice |
|---|---|
| Language | Python 3.12 (standard library only for the application) |
| Test runner | pytest 9.1.1 (pinned) |
| Packaging | Docker (python:3.12-slim base image) |
| Linting / formatting | ruff, black, isort |
| Security scanning | bandit, detect-secrets |
| Pre-commit hooks | pre-commit |
| Documentation | Sphinx + MyST, published to GitHub Pages |
| CI/CD | GitHub Actions |

The application is structured as three independent modules under `src/bankocr/`:

- `recognition.py`: maps OCR pixel patterns to digit characters
- `validation.py`: runs the weighted checksum and assigns `ILL`/`ERR` status
- `reporting.py`: attempts single-segment error correction, formats output lines
- `__main__.py`: CLI entry point; reads `scan.txt`, writes `result.txt`

The architecture is documented in full arc42 format under `docs/architecture/`,
with C4 context, container and component diagrams and four ADRs covering
language choice, Docker packaging, pytest as test runner, and the exact build
and run commands (ADR-004).

## Build and run locally

You need only Docker installed. Python does not need to be on your machine.

**Build the image:**

```bash
docker build -t bankocr .
```

**Prepare a scan file:**

```bash
mkdir -p data
# Place your OCR scan in data/scan.txt
```

The file format is entries of 4 lines each: 3 lines of exactly 27 characters
(the OCR glyph rows) followed by one blank line.

**Run the kata:**

```bash
docker run --rm -v "$(pwd)/data":/data bankocr
```

The program reads `data/scan.txt` and writes the results to `data/result.txt`.
To use different file names, pass them as arguments:

```bash
docker run --rm -v "$(pwd)/data":/data bankocr /data/input.txt /data/output.txt
```

## Run tests

The same image contains pytest (pinned at 9.1.1). Override the entry point to
run all 54 tests:

```bash
docker run --rm --entrypoint pytest bankocr
```

All 54 tests pass. The suite covers digit recognition, checksum validation,
error correction, ambiguity detection, CLI argument handling, and infrastructure
smoke tests.

## Live documentation

Full architecture documentation (arc42 chapters, ADRs, C4 diagrams, user
stories) is published with Sphinx to GitHub Pages:

**https://slaki00.github.io/sdp-powered-by-ai-agents-sladjana-virijevic/**

Docs are rebuilt and deployed when `README.md` or `docs/**` change on a push to
`main` or `feature/module-6-final-project` (see `.github/workflows/docs-deploy.yml`).

## Project structure

```
.
├── .github/
│   └── workflows/
│       ├── ci.yml               # CI: build Docker image + run tests on every push
│       └── docs-deploy.yml      # Deploy Sphinx docs to GitHub Pages
├── .kiro/
│   └── agents/                  # Kiro AI agent definitions (Git, architecture,
│                                #   requirements, CI/CD, TDD/BDD)
├── docs/
│   ├── architecture/            # arc42 chapters 01–12 + PlantUML/SVG diagrams
│   ├── user-stories/            # Derived user stories (recognition, validation,
│   │                            #   reporting)
│   ├── arc42-summary.md
│   ├── conf.py                  # Sphinx configuration
│   └── index.rst
├── scripts/
│   ├── hooks/
│   │   ├── check-commit-msg.sh  # commit-msg hook: enforces #<issue> type(scope): desc
│   │   └── docker-test.sh       # pre-commit hook: builds image and runs pytest
│   ├── agent_prompt.py
│   └── generate-plantuml.sh
├── src/
│   └── bankocr/
│       ├── __init__.py
│       ├── __main__.py          # CLI entry point
│       ├── recognition.py       # OCR pattern → digit mapping
│       ├── validation.py        # Weighted checksum
│       └── reporting.py         # Error correction + output formatting
├── tests/
│   ├── test_recognition.py
│   ├── test_validation.py
│   ├── test_reporting.py
│   ├── test_cli.py
│   ├── test_smoke.py
│   └── test_infra.py            # INFRA and E2E tests
├── Dockerfile
├── pyproject.toml               # Black, isort, ruff, pytest configuration
├── requirements.txt             # pytest==9.1.1
├── .pre-commit-config.yaml
└── LICENSE                      # MIT
```

## Author

**Sladjana Virijevic**, [@slaki00](https://github.com/slaki00)

Built as part of the course *Software Development Processes Powered by AI Agents*
(LabSoft), using Kiro AI agents for every phase of the software development
lifecycle.

## License

[MIT](https://github.com/slaki00/sdp-powered-by-ai-agents-sladjana-virijevic/blob/main/LICENSE)
