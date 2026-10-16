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

The Recognition module is part of the BankOCR Docker image and runs with the Python 3.12 standard library only.

**Architecture references:** `architecture/09-architecture-decisions.md`, ADR-001 and ADR-002; `architecture/07-deployment-view.md`

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

## Implementation Order

1. RECOGNITION-INFRA-001.1: Package Recognition in the BankOCR Docker image
2. RECOGNITION-INFRA-001.2: File storage in the mounted data folder
3. RECOGNITION-INFRA-001.3: Monitoring through standard error
4. RECOGNITION-BE-001.1: Read the scan file and split it into 4-line entries
5. RECOGNITION-BE-001.2: Convert ASCII digit patterns to numeric digits
6. RECOGNITION-STORY-001-S1: end-to-end check of the whole story

## Traceability

| Scenario ID | Architecture | Parent story | Testable assertion (THEN) |
|-------------|--------------|--------------|---------------------------|
| RECOGNITION-STORY-001-S1 | 5.3 Recognition; 1.2 F1; 4.2; 6.1 Happy Path | RECOGNITION-STORY-001 | Result file has two lines: "123456789" and "345882865", both with no marker |
| RECOGNITION-BE-001.1-S1 | 5.3 Recognition; 5.4; 8.4 File I/O Conventions | RECOGNITION-BE-001.1 | Two entries identified, each with 3 lines of 27 characters |
| RECOGNITION-BE-001.2-S1 | 5.3 Recognition; 1.2 F1; 11 R1 | RECOGNITION-BE-001.2 | Recognised account number is 123456789 |
| RECOGNITION-BE-001.2-S2 | 5.3 Recognition; 1.2 F1; 11 R1 | RECOGNITION-BE-001.2 | Recognised account number is 490867715 |
| RECOGNITION-INFRA-001.1-S1 | 9 ADR-001, ADR-002; 7 Deployment View | RECOGNITION-INFRA-001.1 | Result file contains "123456789" with no marker; container exits with code 0 |
| RECOGNITION-INFRA-001.2-S1 | 9 ADR-001; 7.1 Infrastructure (Data Folder) | RECOGNITION-INFRA-001.2 | Result file created in data folder, contains "345882865" with no marker |
| RECOGNITION-INFRA-001.3-S1 | 8.1 Error Handling; 8.3 Logging | RECOGNITION-INFRA-001.3 | Nothing on standard error; result file is the only file written |
