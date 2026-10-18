# Validation

Domain: VALIDATION. Bounded context: Validation (`architecture/05-building-block-view.md`, 5.3).

## VALIDATION-STORY-001: Validate account numbers with the checksum

AS AN Operator I WANT BankOCR to validate every recognised account number with the checksum SO THAT I only need to manually review the numbers marked ERR, instead of all 500 entries

**Priority:** Core

**Architecture references:**
- `architecture/05-building-block-view.md`, 5.3 Validation component
- `architecture/01-introduction-and-goals.md`, 1.2 F2 Validate checksum
- `architecture/01-introduction-and-goals.md`, 1.3 Quality goal Accuracy
- `architecture/10-quality-requirements.md`, 10.2 Scenario 1

**Out of scope:** numbers with unreadable digits and the ILL marker (VALIDATION-STORY-002), correction and the AMB marker (REPORTING-STORY-002, REPORTING-STORY-003).

### SCENARIO 1: Valid and invalid numbers in one file

**Scenario ID**: VALIDATION-STORY-001-S1

**GIVEN**
* A scan file with two entries: 345882865 and 664371495

**WHEN**
* The Operator runs BankOCR with the scan file

**THEN**
* The result file has two lines
* Line 1 is "345882865" with no marker
* Line 2 is "664371495 ERR"

## FE

Not applicable. Validation shows nothing to the Operator directly; the status it sets is written to the result file by Reporting & Correction (REPORTING-STORY-001).

## BE

### VALIDATION-BE-001.1: Calculate the checksum

Given 9 recognised digits, calculate (1*d1 + 2*d2 + ... + 9*d9) mod 11, where d1 is the rightmost digit and d9 the leftmost, and report whether the result is 0.

**Architecture references:** `architecture/01-introduction-and-goals.md`, 1.2 F2; `architecture/11-risks-and-technical-debts.md`, R4

#### SCENARIO 1: Checksum passes

**Scenario ID**: VALIDATION-BE-001.1-S1

**GIVEN**
* The recognised digits 345882865

**WHEN**
* The checksum is calculated

**THEN**
* The weighted sum is 231
* 231 mod 11 is 0, so the checksum passes

#### SCENARIO 2: Checksum fails

**Scenario ID**: VALIDATION-BE-001.1-S2

**GIVEN**
* The recognised digits 664371495

**WHEN**
* The checksum is calculated

**THEN**
* The weighted sum is 222
* 222 mod 11 is 2, so the checksum fails

### VALIDATION-BE-001.2: Assign the validation status

Given a recognised account number, use VALIDATION-BE-001.1 to mark it valid (no marker) when the checksum passes, or ERR when it fails.

**Architecture references:** `architecture/05-building-block-view.md`, 5.3 Validation; `architecture/08-cross-cutting-concepts.md`, 8.2 Status Marking

#### SCENARIO 1: Valid number has no marker

**Scenario ID**: VALIDATION-BE-001.2-S1

**GIVEN**
* A recognised account number 345882865

**WHEN**
* The validation status is assigned

**THEN**
* The number is valid and has no marker

#### SCENARIO 2: Failed checksum is marked ERR

**Scenario ID**: VALIDATION-BE-001.2-S2

**GIVEN**
* A recognised account number 664371495

**WHEN**
* The validation status is assigned

**THEN**
* The number is marked ERR

## INFRA

### VALIDATION-INFRA-001.1: Package Validation in the BankOCR Docker image

The Validation module is part of the BankOCR Docker image and runs with the Python 3.12 standard library only.

**Architecture references:** `architecture/09-architecture-decisions.md`, ADR-001 and ADR-002; `architecture/07-deployment-view.md`

#### SCENARIO 1: Validation runs inside the container

**Scenario ID**: VALIDATION-INFRA-001.1-S1

**GIVEN**
* The BankOCR Docker image
* A folder mounted as a volume with a scan file containing 345882865

**WHEN**
* The Operator starts the container

**THEN**
* The result file in the mounted folder contains "345882865" with no marker
* The container exits with code 0

### VALIDATION-INFRA-001.2: File storage in the mounted data folder

The scan file and the result file are plain text files in a data folder on the local machine, mounted into the container as a volume. There is no database.

**Architecture references:** `architecture/09-architecture-decisions.md`, ADR-001; `architecture/07-deployment-view.md`, 7.1 Infrastructure (Data Folder)

#### SCENARIO 1: Result with ERR is stored in the data folder

**Scenario ID**: VALIDATION-INFRA-001.2-S1

**GIVEN**
* A data folder on the local machine with a scan file containing 664371495
* The data folder is mounted into the container

**WHEN**
* The Operator starts the container

**THEN**
* A result file is created in the same data folder on the local machine
* The result file contains "664371495 ERR"

### VALIDATION-INFRA-001.3: Monitoring through standard error

BankOCR writes no log files. Diagnostic messages go to standard error. An ERR entry is a normal result, not an error, so it produces no diagnostic message.

**Architecture references:** `architecture/08-cross-cutting-concepts.md`, 8.1 Error Handling and 8.3 Logging

#### SCENARIO 1: ERR entries produce no diagnostic messages

**Scenario ID**: VALIDATION-INFRA-001.3-S1

**GIVEN**
* A scan file containing 345882865 and 664371495

**WHEN**
* The Operator runs BankOCR

**THEN**
* Nothing is written to standard error
* The result file is the only file written to the data folder

### Event handling

Not applicable. The CLI Entry Point runs the modules in a fixed order, without events (`architecture/04-solution-strategy.md`, 4.2).

## Implementation Order

1. VALIDATION-INFRA-001.1: Package Validation in the BankOCR Docker image
2. VALIDATION-INFRA-001.2: File storage in the mounted data folder
3. VALIDATION-INFRA-001.3: Monitoring through standard error
4. VALIDATION-BE-001.1: Calculate the checksum
5. VALIDATION-BE-001.2: Assign the validation status
6. VALIDATION-STORY-001-S1: end-to-end check of the whole story

## Traceability

| Scenario ID | Architecture | Parent story | Testable assertion (THEN) |
|-------------|--------------|--------------|---------------------------|
| VALIDATION-STORY-001-S1 | 5.3 Validation; 1.2 F2; 1.3 Accuracy; 10.2 Scenario 1 | VALIDATION-STORY-001 | Result file has two lines: "345882865" with no marker, "664371495 ERR" |
| VALIDATION-BE-001.1-S1 | 1.2 F2; 11 R4 | VALIDATION-BE-001.1 | Weighted sum is 231, 231 mod 11 is 0 |
| VALIDATION-BE-001.1-S2 | 1.2 F2; 11 R4 | VALIDATION-BE-001.1 | Weighted sum is 222, 222 mod 11 is 2 |
| VALIDATION-BE-001.2-S1 | 5.3 Validation; 8.2 Status Marking | VALIDATION-BE-001.2 | Number has no marker |
| VALIDATION-BE-001.2-S2 | 5.3 Validation; 8.2 Status Marking | VALIDATION-BE-001.2 | Number is marked ERR |
| VALIDATION-INFRA-001.1-S1 | 9 ADR-001, ADR-002; 7 Deployment View | VALIDATION-INFRA-001.1 | Result file contains "345882865" with no marker; container exits with code 0 |
| VALIDATION-INFRA-001.2-S1 | 9 ADR-001; 7.1 Infrastructure (Data Folder) | VALIDATION-INFRA-001.2 | Result file is created in the data folder and contains "664371495 ERR" |
| VALIDATION-INFRA-001.3-S1 | 8.1 Error Handling; 8.3 Logging | VALIDATION-INFRA-001.3 | Nothing on standard error; result file is the only file written |

Every scenario traces back to an architecture section, a parent story and a testable THEN clause.
