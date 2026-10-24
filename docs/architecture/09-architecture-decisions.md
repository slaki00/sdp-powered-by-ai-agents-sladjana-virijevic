# 9. Architecture Decisions

## ADR-001: Technology decisions (Language, Framework, Data Storage)

**Status:** Accepted

**Context:**
We need to choose the programming language, the application framework and the
way data is stored. Input and output are text files with fixed formats, each
file has about 500 entries, and nothing needs to be kept between runs.
Accuracy and easy testing matter more than speed.

**Decision:**
- **Language:** Python 3.12.
- **Framework:** No application framework. A command-line program built with
  the Python standard library only.
- **Data storage:** Plain text files on the file system. No database.

**Rationale:**
- Python 3.12 is the language set for the repository (`pyproject.toml`), and it
  has strong built-in support for reading and processing text.
- The whole job is "file in, file out", so a web application or API would add
  code and setup without adding value.
- Using only the standard library means no external dependencies to install,
  update or secure.
- Every file is processed on its own and nothing needs to be remembered between
  runs, so a database would add complexity with no benefit.
- Plain text files match the formats already required by the scanner and the
  bank system.

**Consequences:**
- (+) Simple to run, test and understand; no infrastructure to maintain.
- (+) Recognition, validation and reporting can be tested separately with small
  text inputs.
- (−) There is no history of past runs. If the bank later needs reports over
  time, a data store has to be added in a new ADR.
- (−) The operator has only a command line, without a graphical interface.
- (−) Python is slower than compiled languages, but for files of this size the
  difference is not noticeable.

## ADR-002: Packaging and execution with Docker

**Status:** Accepted

**Context:**
The instructor decided that the program should be packaged as a Docker image
and run on the Operator's local machine.

**Decision:**
- The program is packaged as a Docker image containing Python 3.12.
- The Operator starts the container locally with Docker.
- The container runs one CLI process and exits when it finishes.
- A folder on the local machine is mounted into the container as a volume so
  the CLI can read the scan file and write the result file.

**Rationale:**
- Docker provides a predictable runtime environment regardless of what is
  installed on the local machine.
- Only Docker needs to be installed on the local machine; Python 3.12 is inside
  the image.
- A mounted volume is the simplest way to exchange files between the host and
  the container without hardcoding paths.

**Consequences:**
- (+) The Operator does not need to install Python or any dependencies.
- (+) The runtime environment is identical across machines.
- (−) The Operator needs Docker installed and must know how to start a
  container and mount a folder.
- (−) File paths inside the container differ from paths on the host, so the
  mount point must be documented.

## ADR-003: pytest as test runner

**Status:** Accepted

**Context:**
The course requires automated tests to be run in the CI/CD pipeline. Module 4
starter `cicd-agent.json` specifies "The default CMD must run pytest", and
Module 5 covers test-driven development. We need a test runner, while keeping
ADR-001 valid: the BankOCR program itself uses only the Python 3.12 standard
library.

**Decision:**
- pytest is used to run the tests. It is a development and CI dependency only;
  the BankOCR program itself uses only the Python 3.12 standard library.
- pytest is listed in `requirements.txt` with a pinned version 9.1.1.
- pytest is installed in the Docker image so tests can run inside the container.
- Source code lives in `src/bankocr` and tests in `tests/`.

**Rationale:**
- The course uses pytest: Module 4 starter `cicd-agent.json` specifies "The
  default CMD must run pytest", and Module 5 covers test-driven development.
- Pinning the version (9.1.1) ensures reproducible test runs across machines
  and CI pipelines.
- Installing pytest in the Docker image means the default CMD can run pytest
  without any additional setup on the local machine.

**Consequences:**
- (+) Tests can run in the Docker container with a single command, matching the
  Module 4 CI/CD requirement.
- (+) The test setup is reproducible because the version is pinned.
- (+) ADR-001 stays valid: the BankOCR program itself has no external
  dependencies.
- (−) The Docker image is larger because it contains pytest in addition to
  Python 3.12 and the program.
- (−) pytest is an external package, so it must be pinned and kept up to date
  for security and compatibility.

## ADR-004: Docker commands and CLI defaults

**Status:** Accepted

**Context:**
ADR-002 decided to package BankOCR as a Docker image and run it with a mounted
volume, but did not record the exact build and run commands or the default file
paths. ADR-003's rationale states that the default CMD can run pytest, because
the Module 4 starter (`cicd-agent.json`) required it. Module 6 grades
"docker build && docker run" as a functional kata, which means `docker run`
must run the kata, not pytest. Chapter 7.3 confirms that the container starts a
single CLI process. A new default CMD is therefore needed, along with a
documented way to run tests.

**Decision:**
- ADR-003 stays Accepted; this ADR replaces only its point that the default CMD
  runs pytest.
- The image is built with `docker build -t bankocr .`. The image name `bankocr`
  replaces `kata-tests` from Module 4.
- The Operator runs the kata with
  `docker run --rm -v "$(pwd)/data":/data bankocr`.
- The data folder is mounted at `/data` inside the container.
- The CLI accepts two arguments: the input file path and the output file path.
  Without arguments, it uses `/data/scan.txt` as the input file and
  `/data/result.txt` as the output file.
- Tests are run with `docker run --rm --entrypoint pytest bankocr`.
- pytest stays a development dependency, pinned in `requirements.txt`.

**Rationale:**
- Module 6 grades "docker build && docker run" as a functional kata, so
  `docker run` must start the CLI process, not pytest.
- Chapter 7.3 states that the container starts a single CLI process, which is
  consistent with the CLI being the default entry point.
- The mount point `/data` is documented here as required by ADR-002.
- Default paths `/data/scan.txt` and `/data/result.txt` match the mount point
  and spare the Operator from typing paths on every run.
- Keeping `--entrypoint pytest` for tests preserves ADR-003: pytest remains in
  the image and tests can still run with a single Docker command.

**Consequences:**
- (+) The Operator can run the kata with a single `docker run` command.
- (+) The mount point and default file names are documented in one place.
- (+) Tests can still run inside the same image without a separate test image.
- (−) The CI workflow, the docker-test pre-commit hook and the TDD/BDD agent
  hook all use `docker run --rm kata-tests` and must be updated to use
  `docker run --rm --entrypoint pytest bankocr`.
- (−) If the Operator places files under different names, they must pass the
  paths explicitly as arguments.
