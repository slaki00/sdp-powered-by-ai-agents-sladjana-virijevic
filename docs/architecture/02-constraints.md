# 2. Architecture Constraints

Constraints are requirements the team must respect but did not choose. They
come from the kata specification, the repository configuration and the course
process.

## 2.1 Technical Constraints

| Constraint | Detail | Source |
|------------|--------|--------|
| **Language** | Python 3.12. | ADR-001, `pyproject.toml` (`requires-python = ">=3.12"`) |
| **Dependencies** | Standard library only for the program. pytest is used only for running tests (ADR-003). | ADR-001, ADR-003 |
| **Framework** | No application framework. The program is a CLI built with `argparse` or plain `sys.argv`. | ADR-001 |
| **Data storage** | Plain text files on the local file system. No database. | ADR-001 |
| **Input format** | Each entry is 4 lines: 3 lines of 27 characters (`_`, `\|`, space) and one blank line. An account number has exactly 9 digits. | Kata description |
| **Checksum formula** | `(1·d₁ + 2·d₂ + … + 9·d₉) mod 11 = 0`, where d₁ is the rightmost digit and d₉ is the leftmost. | Kata description |
| **Output format** | One account number per line. Append `ERR`, `ILL` or `AMB` after the number when applicable. | Kata description |
| **Packaging** | The program is packaged as a Docker image and runs as a single CLI process in a local container. | Instructor decision, ADR-002 |

## 2.2 Organizational Constraints

| Constraint | Detail | Source |
|------------|--------|--------|
| **Process** | Issue, branch, pull request, instructor review, squash merge. | Course process |

## 2.3 Conventions

| Convention | Detail | Source |
|------------|--------|--------|
| **Code style** | Black formatting, isort import sorting, ruff linting rules as configured in `pyproject.toml`. | `pyproject.toml`, `.pre-commit-config.yaml` |
| **Pre-commit hooks** | Trailing whitespace, end-of-file fixer, YAML/JSON/TOML checks, large-file check, merge-conflict check, bandit security scan, detect-secrets, commit-message format check, PlantUML validation. | `.pre-commit-config.yaml` |
| **Git conventions** | Commit message format: `#<issue> <type>(<scope>): <description>`. Branch naming and PR template as defined by the Git agent. | `.kiro/agents/git-agent.json` |
| **Documentation** | Architecture documentation in arc42 format using Markdown files. Markdown references the `.svg` files generated from the `.puml` diagrams. | Course instructions |
