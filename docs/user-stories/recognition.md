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

**Architecture references:** `architecture/09-architecture-decisions.md`, ADR-001, ADR-002 and ADR-004; `architecture/07-deployment-view.md`

#### SCENARIO 1: Recognition runs inside the container

**Scenario ID**: RECOGNITION-INFRA-001.1-S1

**GIVEN**
* The BankOCR image has been built with `docker build -t bankocr .`
* A `data` folder on the local machine contains a `scan.txt` with one entry representing 123456789

**WHEN**
* The Operator runs `docker run --rm -v "$(pwd)/data":/data bankocr`

**THEN**
* The container reads `/data/scan.txt` and writes `/data/result.txt`
* `data/result.txt` on the local machine contains "123456789" with no marker
* The container exits with code 0

### RECOGNITION-INFRA-001.2: File storage in the mounted data folder

The scan file and the result file are plain text files in a data folder on the local machine, mounted into the container as a volume. There is no database.

**Architecture references:** `architecture/09-architecture-decisions.md`, ADR-001, ADR-004; `architecture/07-deployment-view.md`, 7.1 Infrastructure (Data Folder)

#### SCENARIO 1: Scan file is read from the mounted data folder

**Scenario ID**: RECOGNITION-INFRA-001.2-S1

**GIVEN**
* A `data` folder on the local machine contains `scan.txt` with one entry representing 345882865
* No `result.txt` exists in the `data` folder

**WHEN**
* The Operator runs `docker run --rm -v "$(pwd)/data":/data bankocr`

**THEN**
* `data/result.txt` is created on the local machine
* `data/result.txt` contains "345882865" with no marker

### RECOGNITION-INFRA-001.3: Monitoring through standard error

BankOCR writes no log files. Diagnostic messages go to standard error. A recognised entry is a normal result, not an error, so it produces no diagnostic message.

**Architecture references:** `architecture/08-cross-cutting-concepts.md`, 8.1 Error Handling and 8.3 Logging

#### SCENARIO 1: Recognised entries produce no diagnostic messages

**Scenario ID**: RECOGNITION-INFRA-001.3-S1

**GIVEN**
* A scan file containing one entry representing 123456789 where all digits are recognised

**WHEN**
* The Operator runs `docker run --rm -v "$(pwd)/data":/data bankocr`

**THEN**
* Nothing is written to standard error
* `data/result.txt` is the only file written to the data folder

### Event handling

Not applicable. The CLI Entry Point runs the modules in a fixed order, without events (`architecture/04-solution-strategy.md`, 4.2).

### RECOGNITION-INFRA-001.4: Test environment

Tests run locally in Docker, not in the cloud. The image is built with `docker build -t bankocr .` and the test suite runs inside the same image with `docker run --rm --entrypoint pytest bankocr`. The dependencies from `requirements.txt` are installed in the image. The project structure (`src/bankocr`, `tests/`) supports pytest discovery. The test environment is shared by all stories.

**Architecture references:** `architecture/09-architecture-decisions.md`, ADR-003, ADR-004; `architecture/08-cross-cutting-concepts.md`, 8.5 Testing

#### SCENARIO 1: Dockerfile builds the bankocr image

**Scenario ID**: RECOGNITION-INFRA-001.4-S1

**GIVEN**
* The project root directory contains the Dockerfile

**WHEN**
* `docker build -t bankocr .` is run

**THEN**
* The Docker image `bankocr` is built successfully

#### SCENARIO 2: Test suite runs inside the container with pytest

**Scenario ID**: RECOGNITION-INFRA-001.4-S2

**GIVEN**
* The `bankocr` Docker image has been built with `docker build -t bankocr .`

**WHEN**
* `docker run --rm --entrypoint pytest bankocr` is run

**THEN**
* pytest runs inside the container and executes the tests in `tests/`
* The container exits with code 0 when all tests pass

#### SCENARIO 3: Dependencies from requirements.txt are installed in the image

**Scenario ID**: RECOGNITION-INFRA-001.4-S3

**GIVEN**
* The Dockerfile and `requirements.txt` are in the project root

**WHEN**
* `docker build -t bankocr .` is run

**THEN**
* The `bankocr` image contains Python 3.12 and the dependencies listed in `requirements.txt`, including pytest 9.1.1

#### SCENARIO 4: Project structure supports pytest discovery

**Scenario ID**: RECOGNITION-INFRA-001.4-S4

**GIVEN**
* The project structure has source code in `src/bankocr` and tests in `tests/`

**WHEN**
* `docker run --rm --entrypoint pytest bankocr` is run

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
| RECOGNITION-INFRA-001.1-S1 | 9 ADR-001, ADR-002, ADR-004; 7 Deployment View | RECOGNITION-INFRA-001.1 | data/result.txt contains "123456789" with no marker; container exits with code 0 |
| RECOGNITION-INFRA-001.2-S1 | 9 ADR-001, ADR-004; 7.1 Infrastructure (Data Folder) | RECOGNITION-INFRA-001.2 | data/result.txt is created and contains "345882865" with no marker |
| RECOGNITION-INFRA-001.3-S1 | 8.1 Error Handling; 8.3 Logging | RECOGNITION-INFRA-001.3 | Nothing on standard error; data/result.txt is the only file written to the data folder |
| RECOGNITION-INFRA-001.4-S1 | 9 ADR-003, ADR-004; 8.5 Testing | RECOGNITION-INFRA-001.4 | Docker image `bankocr` is built successfully |
| RECOGNITION-INFRA-001.4-S2 | 9 ADR-003, ADR-004; 8.5 Testing | RECOGNITION-INFRA-001.4 | pytest runs inside the container and executes the tests in `tests/`; container exits with code 0 when all tests pass |
| RECOGNITION-INFRA-001.4-S3 | 9 ADR-003, ADR-004; 8.5 Testing | RECOGNITION-INFRA-001.4 | `bankocr` image contains Python 3.12 and dependencies from `requirements.txt`, including pytest 9.1.1 |
| RECOGNITION-INFRA-001.4-S4 | 9 ADR-003, ADR-004; 8.5 Testing | RECOGNITION-INFRA-001.4 | pytest collects tests in `tests/` and tests can import bankocr from `src/` because PYTHONPATH is /app/src |

---

## RECOGNITION-STORY-002: Mark unreadable digits with ? and continue with the next entry

AS AN Operator I WANT BankOCR to mark any digit it cannot recognise as ? and continue processing the remaining entries SO THAT every entry in the scan file produces a result, even when one or more digits are unreadable

**Priority:** Supporting

**Architecture references:**
- `architecture/05-building-block-view.md`, 5.3 Recognition component
- `architecture/01-introduction-and-goals.md`, 1.2 F1 Read scan file
- `architecture/01-introduction-and-goals.md`, 1.3 Robustness quality goal
- `architecture/08-cross-cutting-concepts.md`, 8.1 Error Handling
- `architecture/06-runtime-view.md`, 6.2 Unreadable Digit: ILL, Correction Attempted
- `architecture/06-runtime-view.md`, 6.4 Malformed Entry: Processing Continues

**Out of scope:** marking the entry ILL when a ? is present (VALIDATION-STORY-002, which this story's end-to-end scenario depends on), attempting correction of unreadable digits (REPORTING-STORY-002, REPORTING-STORY-003), reporting a clear error when the scan file is missing or unreadable (RECOGNITION-STORY-003).

### SCENARIO 1: Entry with one unreadable digit is marked with ? and processing continues

**Scenario ID**: RECOGNITION-STORY-002-S1

**GIVEN**
* A scan file with two entries
* The first entry has an all-spaces grid at digit position 1 (the leftmost position); its three lines of 27 characters are:

```
    _  _  _  _  _  _  _  _ 
   | || || || || || || || |
   |_||_||_||_||_||_||_||_|

```

* The second entry represents the account number 123456789

**WHEN**
* The Operator runs BankOCR with the scan file

**THEN**
* The result for the first entry is "?00000000 ILL"
* The result for the second entry is "123456789"
* Both entries appear in the result file; no entry is dropped

## FE

Not applicable. BankOCR is a CLI program with no graphical interface (ADR-001). The ? marker is written to the result file by Reporting & Correction (REPORTING-STORY-001, VALIDATION-STORY-002).

## BE

### RECOGNITION-BE-002.1: Replace an unrecognised 3-by-3 pattern with ?

When a 3-by-3 character grid within an entry does not match any of the ten known digit patterns, Recognition replaces that position with `?` and continues converting the remaining digit positions in the same entry.

**Architecture references:**
- `architecture/05-building-block-view.md`, 5.3 Recognition component
- `architecture/05-building-block-view.md`, 5.4 Important Interfaces
- `architecture/08-cross-cutting-concepts.md`, 8.1 Error Handling
- `architecture/01-introduction-and-goals.md`, 1.2 F1 Read scan file
- `architecture/11-risks-and-technical-debts.md`, R1

#### SCENARIO 1: Single unrecognised digit in an entry is replaced with ?

**Scenario ID**: RECOGNITION-BE-002.1-S1

**GIVEN**
* An entry with an all-spaces grid at digit position 1 (the leftmost position) and eight `0` patterns at positions 2 through 9; its three lines of 27 characters are:

```
    _  _  _  _  _  _  _  _ 
   | || || || || || || || |
   |_||_||_||_||_||_||_||_|

```

(The unreadable grid is not drawn in the kata description or the architecture; it is defined here as nine spaces, a 3-by-3 grid of spaces, which does not match any of the ten known patterns in `architecture/05-building-block-view.md`, 5.3.)

**WHEN**
* Recognition converts the patterns of that entry to digits

**THEN**
* The output for that entry is "?00000000"
* No exception is raised; processing of that entry completes normally

#### SCENARIO 2: All nine digit positions unrecognised in one entry yields nine ? characters

**Scenario ID**: RECOGNITION-BE-002.1-S2

**GIVEN**
* An entry where all nine 3-by-3 grids are the all-spaces pattern (nine spaces each); its three lines of 27 characters are:

```
                           
                           
                           

```

**WHEN**
* Recognition converts the patterns of that entry to digits

**THEN**
* The output for that entry is "?????????"
* No exception is raised

### RECOGNITION-BE-002.2: Continue to the next entry after an unreadable digit

When an entry contains one or more `?` positions, Recognition passes the partial result (with `?` in the unrecognised positions) to the CLI Entry Point and moves on to process the next entry in the scan file.

**Architecture references:**
- `architecture/05-building-block-view.md`, 5.3 Recognition component
- `architecture/05-building-block-view.md`, 5.4 Important Interfaces
- `architecture/08-cross-cutting-concepts.md`, 8.1 Error Handling
- `architecture/01-introduction-and-goals.md`, 1.3 Robustness quality goal
- `architecture/06-runtime-view.md`, 6.4 Malformed Entry: Processing Continues

#### SCENARIO 1: Entry with unreadable digit is passed on and next entry is processed

**Scenario ID**: RECOGNITION-BE-002.2-S1

**GIVEN**
* A scan file with two entries
* The first entry has an all-spaces grid at digit position 1 and eight `0` patterns at positions 2 through 9 (the same entry as RECOGNITION-BE-002.1-S1)
* The second entry represents the account number 123456789

**WHEN**
* Recognition processes the scan file

**THEN**
* Recognition returns two results in order
* The first result is "?00000000"
* The second result is "123456789"

## INFRA

### RECOGNITION-INFRA-002.1: Deployment

See RECOGNITION-INFRA-001.1. No additional deployment configuration is needed for the ? marking behaviour; it is part of the same Recognition module and Docker image.

**Architecture references:** `architecture/09-architecture-decisions.md`, ADR-001, ADR-002, ADR-004; `architecture/07-deployment-view.md`

#### SCENARIO 1: BankOCR processes a scan file with an unreadable digit inside the container

**Scenario ID**: RECOGNITION-INFRA-002.1-S1

**GIVEN**
* The BankOCR image has been built with `docker build -t bankocr .`
* A `data` folder on the local machine contains a `scan.txt` with two entries: the first has an all-spaces grid at digit position 1 and eight `0` patterns at positions 2 through 9 (the same entry as RECOGNITION-BE-002.1-S1), the second represents 123456789

**WHEN**
* The Operator runs `docker run --rm -v "$(pwd)/data":/data bankocr`

**THEN**
* `data/result.txt` on the local machine contains two lines
* The first line is "?00000000 ILL"
* The second line is "123456789"
* The container exits with code 0

### Data store

See RECOGNITION-INFRA-001.2. There is no database; the scan file and result file are plain text files in the mounted data folder. No change is needed for this story.

### Event handling

Not applicable. The CLI Entry Point runs the modules in a fixed order, without events (`architecture/04-solution-strategy.md`, 4.2).

### Monitoring

See RECOGNITION-INFRA-001.3. A ? marker is a normal result, not an error. Recognition writes nothing to standard error when it marks a digit as ?. An entry later marked ILL by Validation is also a normal result (`architecture/08-cross-cutting-concepts.md`, 8.1, 8.3).

### Test environment

See RECOGNITION-INFRA-001.4.

## Implementation Order

1. RECOGNITION-BE-002.1: Replace an unrecognised 3-by-3 pattern with ?
2. RECOGNITION-BE-002.2: Continue to the next entry after an unreadable digit
3. RECOGNITION-STORY-002-S1: end-to-end check of the whole story, implemented after VALIDATION-STORY-002, because Validation must handle ? to produce the ILL marker that makes the end-to-end result observable
4. RECOGNITION-INFRA-002.1-S1: end-to-end container check, implemented after VALIDATION-STORY-002, same reason

## Traceability

| Scenario ID | Architecture | Parent story | Testable assertion (THEN) |
|-------------|--------------|--------------|---------------------------|
| RECOGNITION-STORY-002-S1 | 5.3 Recognition; 1.2 F1; 1.3 Robustness; 8.1; 6.2; 6.4 | RECOGNITION-STORY-002 | First result is "?00000000 ILL", second result is "123456789", both entries appear in the result file |
| RECOGNITION-BE-002.1-S1 | 5.3 Recognition; 5.4; 8.1; 1.2 F1; 11 R1 | RECOGNITION-BE-002.1 | Output for the entry is "?00000000"; no exception raised |
| RECOGNITION-BE-002.1-S2 | 5.3 Recognition; 5.4; 8.1; 1.2 F1; 11 R1 | RECOGNITION-BE-002.1 | Output for the entry is "?????????"; no exception raised |
| RECOGNITION-BE-002.2-S1 | 5.3 Recognition; 5.4; 8.1; 1.3 Robustness; 6.4 | RECOGNITION-BE-002.2 | Two results in order: "?00000000" then "123456789" |
| RECOGNITION-INFRA-002.1-S1 | 9 ADR-001, ADR-002, ADR-004; 7 Deployment View | RECOGNITION-INFRA-002.1 | data/result.txt has two lines: "?00000000 ILL" and "123456789"; container exits with code 0 |
