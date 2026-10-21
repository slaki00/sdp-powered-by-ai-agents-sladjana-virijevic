# Reporting

Domain: REPORTING. Bounded context: Reporting & Correction (`architecture/05-building-block-view.md`, 5.3).

## REPORTING-STORY-001: Write the result file, one number per line with its marker

AS AN Operator I WANT BankOCR to write a result file with one account number per line and a marker for each flagged entry SO THAT I can review only the flagged numbers instead of transcribing all entries

**Priority:** Core

**Architecture references:**
- `architecture/05-building-block-view.md`, 5.3 Reporting & Correction component
- `architecture/01-introduction-and-goals.md`, 1.2 F3 Write result file
- `architecture/06-runtime-view.md`, 6.1 Happy Path: All Digits Recognised and Checksum Passes
- `architecture/08-cross-cutting-concepts.md`, 8.2 Status Marking
- `architecture/08-cross-cutting-concepts.md`, 8.4 File I/O Conventions
- `architecture/10-quality-requirements.md`, 10.2 Scenario 4

**Out of scope:** correction and the AMB marker (REPORTING-STORY-002, REPORTING-STORY-003), the ILL marker for numbers with unreadable digits (VALIDATION-STORY-002), unreadable digits and the ? marker (RECOGNITION-STORY-002), errors when the scan file is missing or unreadable (RECOGNITION-STORY-003).

### SCENARIO 1: Valid and ERR entries written to the result file in order

**Scenario ID**: REPORTING-STORY-001-S1

**GIVEN**
* A scan file with three entries: 345882865, 664371495 and 123456789

**WHEN**
* The Operator runs BankOCR with the scan file

**THEN**
* The result file has three lines
* Line 1 is "345882865" with no marker
* Line 2 is "664371495 ERR"
* Line 3 is "123456789" with no marker

## FE

Not applicable. BankOCR is a CLI program with no graphical interface (ADR-001). The Operator reviews the result file directly as plain text.

## BE

### REPORTING-BE-001.1: Format each entry as a result line

Given an account number and its validation status, produce one output line. A valid number has no marker. A number with a failed checksum is followed by " ERR".

**Architecture references:** `architecture/01-introduction-and-goals.md`, 1.2 F3; `architecture/08-cross-cutting-concepts.md`, 8.2 Status Marking

#### SCENARIO 1: Valid number has no marker

**Scenario ID**: REPORTING-BE-001.1-S1

**GIVEN**
* A recognised account number 345882865 with status valid

**WHEN**
* The result line is formatted

**THEN**
* The line is "345882865"

#### SCENARIO 2: ERR number is followed by ERR

**Scenario ID**: REPORTING-BE-001.1-S2

**GIVEN**
* A recognised account number 664371495 with status ERR

**WHEN**
* The result line is formatted

**THEN**
* The line is "664371495 ERR"

### REPORTING-BE-001.2: Write all result lines to the result file

Given the output file path from the CLI Entry Point, write one formatted line per entry to the result file. The file is written once after all entries are processed.

**Architecture references:** `architecture/05-building-block-view.md`, 5.3 Reporting & Correction and 5.4 Important Interfaces; `architecture/08-cross-cutting-concepts.md`, 8.4 File I/O Conventions

#### SCENARIO 1: Two entries produce a two-line result file

**Scenario ID**: REPORTING-BE-001.2-S1

**GIVEN**
* Two formatted lines: "345882865" and "664371495 ERR"

**WHEN**
* The lines are written to the result file

**THEN**
* The result file contains two lines
* Line 1 is "345882865"
* Line 2 is "664371495 ERR"

## INFRA

### REPORTING-INFRA-001.1: Package Reporting & Correction in the BankOCR Docker image

The Reporting & Correction module is part of the BankOCR Docker image and runs as one CLI process. The program uses the Python 3.12 standard library only; pytest in the image is used only for the tests (ADR-003).

**Architecture references:** `architecture/09-architecture-decisions.md`, ADR-001, ADR-002 and ADR-004; `architecture/07-deployment-view.md`

#### SCENARIO 1: Reporting runs inside the container

**Scenario ID**: REPORTING-INFRA-001.1-S1

**GIVEN**
* The BankOCR image has been built with `docker build -t bankocr .`
* A `data` folder on the local machine contains a `scan.txt` with two entries representing 345882865 and 664371495

**WHEN**
* The Operator runs `docker run --rm -v "$(pwd)/data":/data bankocr`

**THEN**
* The container reads `/data/scan.txt` and writes `/data/result.txt`
* `data/result.txt` on the local machine contains "345882865" on line 1 and "664371495 ERR" on line 2
* The container exits with code 0

### REPORTING-INFRA-001.2: File storage in the mounted data folder

The scan file and the result file are plain text files in a data folder on the local machine, mounted into the container as a volume. There is no database.

**Architecture references:** `architecture/09-architecture-decisions.md`, ADR-001, ADR-004; `architecture/07-deployment-view.md`, 7.1 Infrastructure (Data Folder)

#### SCENARIO 1: Result file is written to the mounted data folder

**Scenario ID**: REPORTING-INFRA-001.2-S1

**GIVEN**
* A `data` folder on the local machine contains `scan.txt` with two entries representing 345882865 and 664371495
* No `result.txt` exists in the `data` folder

**WHEN**
* The Operator runs `docker run --rm -v "$(pwd)/data":/data bankocr`

**THEN**
* `data/result.txt` is created on the local machine
* `data/result.txt` contains "345882865" on line 1 and "664371495 ERR" on line 2

### REPORTING-INFRA-001.3: Monitoring through standard error

BankOCR writes no log files. Diagnostic messages go to standard error. An ERR entry is a normal result, not an error, so it produces no diagnostic message.

**Architecture references:** `architecture/08-cross-cutting-concepts.md`, 8.1 Error Handling and 8.3 Logging

#### SCENARIO 1: ERR entries produce no diagnostic messages

**Scenario ID**: REPORTING-INFRA-001.3-S1

**GIVEN**
* A scan file containing 345882865 and 664371495

**WHEN**
* The Operator runs `docker run --rm -v "$(pwd)/data":/data bankocr`

**THEN**
* Nothing is written to standard error
* `data/result.txt` is the only file written to the data folder

### Event handling

Not applicable. The CLI Entry Point runs the modules in a fixed order, without events (`architecture/04-solution-strategy.md`, 4.2).

### Test environment

See RECOGNITION-INFRA-001.4: Test environment. The test environment is shared by all stories and is described once in the Recognition bundle.

## Implementation Order

1. REPORTING-INFRA-001.1: Package Reporting & Correction in the BankOCR Docker image
2. REPORTING-INFRA-001.2: File storage in the mounted data folder
3. REPORTING-INFRA-001.3: Monitoring through standard error
4. Test environment (see RECOGNITION-INFRA-001.4)
5. REPORTING-BE-001.1: Format each entry as a result line
6. REPORTING-BE-001.2: Write all result lines to the result file
7. REPORTING-STORY-001-S1: end-to-end check of the whole story

## Traceability

| Scenario ID | Architecture | Parent story | Testable assertion (THEN) |
|-------------|--------------|--------------|---------------------------|
| REPORTING-STORY-001-S1 | 5.3 Reporting & Correction; 1.2 F3; 6.1 Happy Path; 8.2 Status Marking; 8.4 File I/O; 10.2 Scenario 4 | REPORTING-STORY-001 | Result file has three lines: "345882865", "664371495 ERR", "123456789" |
| REPORTING-BE-001.1-S1 | 1.2 F3; 8.2 Status Marking | REPORTING-BE-001.1 | Line is "345882865" |
| REPORTING-BE-001.1-S2 | 1.2 F3; 8.2 Status Marking | REPORTING-BE-001.1 | Line is "664371495 ERR" |
| REPORTING-BE-001.2-S1 | 5.3 Reporting & Correction; 5.4; 8.4 File I/O | REPORTING-BE-001.2 | Result file contains two lines: "345882865" and "664371495 ERR" |
| REPORTING-INFRA-001.1-S1 | 9 ADR-001, ADR-002, ADR-004; 7 Deployment View | REPORTING-INFRA-001.1 | data/result.txt contains "345882865" on line 1 and "664371495 ERR" on line 2; container exits with code 0 |
| REPORTING-INFRA-001.2-S1 | 9 ADR-001, ADR-004; 7.1 Infrastructure (Data Folder) | REPORTING-INFRA-001.2 | data/result.txt is created and contains "345882865" on line 1 and "664371495 ERR" on line 2 |
| REPORTING-INFRA-001.3-S1 | 8.1 Error Handling; 8.3 Logging | REPORTING-INFRA-001.3 | Nothing on standard error; data/result.txt is the only file written to the data folder |
