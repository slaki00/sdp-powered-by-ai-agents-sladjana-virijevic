# Recognition

Domain: RECOGNITION. Bounded context: Recognition (`architecture/05-building-block-view.md`, 5.3).

## RECOGNITION-STORY-001: Read each entry as a 9-digit account number

AS AN Operator I WANT BankOCR to read each entry in the scan file and recognise the 9-digit account number SO THAT I do not have to transcribe account numbers by hand

**Priority:** Core

**Architecture references:**
- `architecture/05-building-block-view.md`, 5.3 Recognition component
- `architecture/01-introduction-and-goals.md`, 1.2 F1 Read scan file
- `architecture/04-solution-strategy.md`, 4.2 System Decomposition
- `architecture/06-runtime-view.md`, 6.1 Happy Path: All Digits Recognised and Checksum Passes

**Out of scope:** unreadable digits and the ? marker (RECOGNITION-STORY-002), checksum validation and the ERR marker (VALIDATION-STORY-001), the ILL marker for numbers with unreadable digits (VALIDATION-STORY-002), writing the result file (REPORTING-STORY-001), correction and the AMB marker (REPORTING-STORY-002, REPORTING-STORY-003), errors when the scan file is missing or unreadable (RECOGNITION-STORY-003).

### SCENARIO 1: Multiple entries recognised in one scan file

**Scenario ID**: RECOGNITION-STORY-001-S1

**GIVEN**
* A scan file with two entries representing the account numbers 123456789 and 345882865

**WHEN**
* The Operator runs BankOCR with the scan file

**THEN**
* The result file has two lines
* Line 1 is "123456789" with no marker
* Line 2 is "345882865" with no marker

## FE

Not applicable. BankOCR is a CLI program with no graphical interface (ADR-001). Recognition shows nothing to the Operator directly; the recognised account numbers are written to the result file by Reporting & Correction (REPORTING-STORY-001).

## BE

### RECOGNITION-BE-001.1: Read the scan file and split it into 4-line entries

Given the input file path from the CLI Entry Point, read the scan file and split it into entries. Each entry is 4 lines: 3 lines of 27 characters and 1 blank line.

**Architecture references:** `architecture/05-building-block-view.md`, 5.3 Recognition and 5.4 Important Interfaces; `architecture/08-cross-cutting-concepts.md`, 8.4 File I/O Conventions

#### SCENARIO 1: A file with two entries is split into two 4-line blocks

**Scenario ID**: RECOGNITION-BE-001.1-S1

**GIVEN**
* A scan file containing two entries, each consisting of 3 lines of 27 characters and 1 blank line

**WHEN**
* Recognition reads the file and splits it into entries

**THEN**
* Two entries are identified
* Each entry has 3 lines of 27 characters

### RECOGNITION-BE-001.2: Convert ASCII digit patterns to numeric digits

Given an entry of 3 lines of 27 characters, match each 3-by-3 character grid against the ten known digit patterns to produce a 9-digit account number.

**Architecture references:** `architecture/05-building-block-view.md`, 5.3 Recognition; `architecture/01-introduction-and-goals.md`, 1.2 F1; `architecture/11-risks-and-technical-debts.md`, R1

#### SCENARIO 1: Entry with digits 1 through 9 is recognised correctly

**Scenario ID**: RECOGNITION-BE-001.2-S1

**GIVEN**
* An entry whose 3 lines of 27 characters are:

```
    _  _     _  _  _  _  _ 
  | _| _||_||_ |_   ||_||_|
  ||_  _|  | _||_|  ||_| _|

```

**WHEN**
* Recognition converts the patterns to numeric digits

**THEN**
* The recognised account number is 123456789

#### SCENARIO 2: Entry containing digit 0 is recognised correctly

**Scenario ID**: RECOGNITION-BE-001.2-S2

**GIVEN**
* An entry whose 3 lines of 27 characters are:

```
    _  _  _  _  _  _     _ 
|_||_|| ||_||_   |  |  ||_ 
  | _||_||_||_|  |  |  | _|

```

**WHEN**
* Recognition converts the patterns to numeric digits

**THEN**
* The recognised account number is 490867715

## INFRA

### RECOGNITION-INFRA-001.1: Package Recognition in the BankOCR Docker image

The Recognition module is part of the BankOCR Docker image and runs as one CLI process. The program uses the Python 3.12 standard library only; pytest in the image is used only for the tests (ADR-003).

**Architecture references:** `architecture/09-architecture-decisions.md`, ADR-001, ADR-002 and ADR-003; `architecture/07-deployment-view.md`

#### SCENARIO 1: Recognition runs inside the container

**Scenario ID**: RECOGNITION-INFRA-001.1-S1

**GIVEN**
* The BankOCR Docker image
* A folder mounted as a volume with a scan file containing one entry representing 123456789

**WHEN**
* The Operator starts the container

**THEN**
* The result file in the mounted folder contains "123456789" with no marker
* The container exits with code 0

### RECOGNITION-INFRA-001.2: File storage in the mounted data folder

The scan file and the result file are plain text files in a data folder on the local machine, mounted into the container as a volume. There is no database.

**Architecture references:** `architecture/09-architecture-decisions.md`, ADR-001; `architecture/07-deployment-view.md`, 7.1 Infrastructure (Data Folder)

#### SCENARIO 1: Scan file is read from the mounted data folder

**Scenario ID**: RECOGNITION-INFRA-001.2-S1

**GIVEN**
* A data folder on the local machine with a scan file containing one entry representing 345882865
* The data folder is mounted into the container

**WHEN**
* The Operator starts the container

**THEN**
* A result file is created in the same data folder on the local machine
* The result file contains "345882865" with no marker

### RECOGNITION-INFRA-001.3: Monitoring through standard error

BankOCR writes no log files. Diagnostic messages go to standard error. A recognised entry is a normal result, not an error, so it produces no diagnostic message.

**Architecture references:** `architecture/08-cross-cutting-concepts.md`, 8.1 Error Handling and 8.3 Logging

#### SCENARIO 1: Recognised entries produce no diagnostic messages

**Scenario ID**: RECOGNITION-INFRA-001.3-S1

**GIVEN**
* A scan file containing one entry representing 123456789 where all digits are recognised

**WHEN**
* The Operator runs BankOCR

**THEN**
* Nothing is written to standard error
* The result file is the only file written to the data folder

### Event handling

Not applicable. The CLI Entry Point runs the modules in a fixed order, without events (`architecture/04-solution-strategy.md`, 4.2).

### RECOGNITION-INFRA-001.4: Test environment

Tests run locally in Docker, not in the cloud. The Dockerfile builds with `docker build -t kata-tests .` and the test suite runs inside the container with `docker run --rm kata-tests` using pytest. The dependencies from `requirements.txt` are installed in the image. The project structure (`src/bankocr`, `tests/`) supports pytest discovery. The test environment is shared by all stories.

**Architecture references:** `architecture/09-architecture-decisions.md`, ADR-003; `architecture/08-cross-cutting-concepts.md`, 8.5 Testing

#### SCENARIO 1: Dockerfile builds the test image

**Scenario ID**: RECOGNITION-INFRA-001.4-S1

**GIVEN**
* The project root directory containing the Dockerfile

**WHEN**
* `docker build -t kata-tests .` is run

**THEN**
* The Docker image `kata-tests` is built successfully

#### SCENARIO 2: Test suite runs inside the container with pytest

**Scenario ID**: RECOGNITION-INFRA-001.4-S2

**GIVEN**
* The `kata-tests` Docker image is built

**WHEN**
* `docker run --rm kata-tests` is run

**THEN**
* pytest runs inside the container and executes the tests in `tests/`
* The container exits with code 0 when all tests pass

#### SCENARIO 3: Dependencies from requirements.txt are installed in the image

**Scenario ID**: RECOGNITION-INFRA-001.4-S3

**GIVEN**
* The Dockerfile and `requirements.txt` in the project root

**WHEN**
* `docker build -t kata-tests .` is run

**THEN**
* The `kata-tests` image contains Python 3.12 and the dependencies listed in `requirements.txt`, including pytest

#### SCENARIO 4: Project structure supports pytest discovery

**Scenario ID**: RECOGNITION-INFRA-001.4-S4

**GIVEN**
* The project structure with source code in `src/bankocr` and tests in `tests/`

**WHEN**
* `docker run --rm kata-tests` is run

**THEN**
* pytest collects the tests in `tests/`, and the tests can import the bankocr package from `src/` because the image sets PYTHONPATH to /app/src

## Implementation Order

1. RECOGNITION-INFRA-001.1: Package Recognition in the BankOCR Docker image
2. RECOGNITION-INFRA-001.2: File storage in the mounted data folder
3. RECOGNITION-INFRA-001.3: Monitoring through standard error
4. RECOGNITION-INFRA-001.4: Test environment
5. RECOGNITION-BE-001.1: Read the scan file and split it into 4-line entries
6. RECOGNITION-BE-001.2: Convert ASCII digit patterns to numeric digits
7. RECOGNITION-STORY-001-S1: end-to-end check of the whole story

## Traceability

| Scenario ID | Architecture | Parent story | Testable assertion (THEN) |
|-------------|--------------|--------------|---------------------------|
| RECOGNITION-STORY-001-S1 | 5.3 Recognition; 1.2 F1; 4.2; 6.1 Happy Path | RECOGNITION-STORY-001 | Result file has two lines: "123456789" and "345882865", both with no marker |
| RECOGNITION-BE-001.1-S1 | 5.3 Recognition; 5.4; 8.4 File I/O Conventions | RECOGNITION-BE-001.1 | Two entries identified, each with 3 lines of 27 characters |
| RECOGNITION-BE-001.2-S1 | 5.3 Recognition; 1.2 F1; 11 R1 | RECOGNITION-BE-001.2 | Recognised account number is 123456789 |
| RECOGNITION-BE-001.2-S2 | 5.3 Recognition; 1.2 F1; 11 R1 | RECOGNITION-BE-001.2 | Recognised account number is 490867715 |
| RECOGNITION-INFRA-001.1-S1 | 9 ADR-001, ADR-002, ADR-003; 7 Deployment View | RECOGNITION-INFRA-001.1 | Result file contains "123456789" with no marker; container exits with code 0 |
| RECOGNITION-INFRA-001.2-S1 | 9 ADR-001; 7.1 Infrastructure (Data Folder) | RECOGNITION-INFRA-001.2 | Result file created in data folder, contains "345882865" with no marker |
| RECOGNITION-INFRA-001.3-S1 | 8.1 Error Handling; 8.3 Logging | RECOGNITION-INFRA-001.3 | Nothing on standard error; result file is the only file written |
| RECOGNITION-INFRA-001.4-S1 | 9 ADR-003; 8.5 Testing | RECOGNITION-INFRA-001.4 | Docker image `kata-tests` is built successfully |
| RECOGNITION-INFRA-001.4-S2 | 9 ADR-003; 8.5 Testing | RECOGNITION-INFRA-001.4 | pytest runs inside the container and executes the tests in `tests/`; container exits with code 0 when all tests pass |
| RECOGNITION-INFRA-001.4-S3 | 9 ADR-003; 8.5 Testing | RECOGNITION-INFRA-001.4 | Image contains Python 3.12 and dependencies from `requirements.txt`, including pytest |
| RECOGNITION-INFRA-001.4-S4 | 9 ADR-003; 8.5 Testing | RECOGNITION-INFRA-001.4 | pytest collects tests in `tests/` and tests can import bankocr from `src/` because PYTHONPATH is /app/src |
