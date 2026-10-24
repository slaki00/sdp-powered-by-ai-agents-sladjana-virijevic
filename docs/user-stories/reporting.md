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
* A scan file with three entries: 345882865, 222222222 and 123456789

**WHEN**
* The Operator runs BankOCR with the scan file

**THEN**
* The result file has three lines
* Line 1 is "345882865" with no marker
* Line 2 is "222222222 ERR"
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
* A `data` folder on the local machine contains a `scan.txt` with two entries representing 345882865 and 222222222

**WHEN**
* The Operator runs `docker run --rm -v "$(pwd)/data":/data bankocr`

**THEN**
* The container reads `/data/scan.txt` and writes `/data/result.txt`
* `data/result.txt` on the local machine contains "345882865" on line 1 and "222222222 ERR" on line 2
* The container exits with code 0

### REPORTING-INFRA-001.2: File storage in the mounted data folder

The scan file and the result file are plain text files in a data folder on the local machine, mounted into the container as a volume. There is no database.

**Architecture references:** `architecture/09-architecture-decisions.md`, ADR-001, ADR-004; `architecture/07-deployment-view.md`, 7.1 Infrastructure (Data Folder)

#### SCENARIO 1: Result file is written to the mounted data folder

**Scenario ID**: REPORTING-INFRA-001.2-S1

**GIVEN**
* A `data` folder on the local machine contains `scan.txt` with two entries representing 345882865 and 222222222
* No `result.txt` exists in the `data` folder

**WHEN**
* The Operator runs `docker run --rm -v "$(pwd)/data":/data bankocr`

**THEN**
* `data/result.txt` is created on the local machine
* `data/result.txt` contains "345882865" on line 1 and "222222222 ERR" on line 2

### REPORTING-INFRA-001.3: Monitoring through standard error

BankOCR writes no log files. Diagnostic messages go to standard error. An ERR entry is a normal result, not an error, so it produces no diagnostic message.

**Architecture references:** `architecture/08-cross-cutting-concepts.md`, 8.1 Error Handling and 8.3 Logging

#### SCENARIO 1: ERR entries produce no diagnostic messages

**Scenario ID**: REPORTING-INFRA-001.3-S1

**GIVEN**
* A scan file containing 345882865 and 222222222

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
| REPORTING-STORY-001-S1 | 5.3 Reporting & Correction; 1.2 F3; 6.1 Happy Path; 8.2 Status Marking; 8.4 File I/O; 10.2 Scenario 4 | REPORTING-STORY-001 | Result file has three lines: "345882865", "222222222 ERR", "123456789" |
| REPORTING-BE-001.1-S1 | 1.2 F3; 8.2 Status Marking | REPORTING-BE-001.1 | Line is "345882865" |
| REPORTING-BE-001.1-S2 | 1.2 F3; 8.2 Status Marking | REPORTING-BE-001.1 | Line is "664371495 ERR" |
| REPORTING-BE-001.2-S1 | 5.3 Reporting & Correction; 5.4; 8.4 File I/O | REPORTING-BE-001.2 | Result file contains two lines: "345882865" and "664371495 ERR" |
| REPORTING-INFRA-001.1-S1 | 9 ADR-001, ADR-002, ADR-004; 7 Deployment View | REPORTING-INFRA-001.1 | data/result.txt contains "345882865" on line 1 and "222222222 ERR" on line 2; container exits with code 0 |
| REPORTING-INFRA-001.2-S1 | 9 ADR-001, ADR-004; 7.1 Infrastructure (Data Folder) | REPORTING-INFRA-001.2 | data/result.txt is created and contains "345882865" on line 1 and "222222222 ERR" on line 2 |
| REPORTING-INFRA-001.3-S1 | 8.1 Error Handling; 8.3 Logging | REPORTING-INFRA-001.3 | Nothing on standard error; data/result.txt is the only file written to the data folder |

---

## REPORTING-STORY-002: Correct an ERR or ILL entry when exactly one alternative passes

AS AN Operator I WANT BankOCR to replace an ERR or ILL entry with the corrected account number when exactly one alternative interpretation passes the checksum SO THAT I do not have to manually correct entries that the program can resolve automatically

**Priority:** Supporting

**Architecture references:**
- `architecture/05-building-block-view.md`, 5.3 Reporting & Correction component
- `architecture/01-introduction-and-goals.md`, 1.2 F4 Attempt correction
- `architecture/06-runtime-view.md`, 6.2 Unreadable Digit: ILL, Correction Attempted
- `architecture/06-runtime-view.md`, 6.3 Bad Checksum: ERR with Correction
- `architecture/08-cross-cutting-concepts.md`, 8.1 Error Handling
- `architecture/08-cross-cutting-concepts.md`, 8.2 Status Marking

**Correction rule (quoted from architecture):**

F4 (`architecture/01-introduction-and-goals.md`, 1.2): "For entries marked ERR or ILL, try alternative digit interpretations. If exactly one alternative passes the checksum, replace the number and clear the flag. If more than one passes, mark the entry AMB. If no alternative passes, the entry keeps its ERR or ILL status. An alternative changes one digit by adding or removing exactly one pipe or underscore."

For an ERR entry all nine digit positions are candidates for the single-segment change. For an ILL entry only the unrecognised (`?`) position is a candidate (`architecture/06-runtime-view.md`, 6.2: "tries alternative interpretations for the unreadable digit").

**Out of scope:** marking AMB when more than one alternative passes (REPORTING-STORY-003), writing the result file without correction (REPORTING-STORY-001), the ILL marker for numbers with unreadable digits (VALIDATION-STORY-002), the ERR marker for failed checksums (VALIDATION-STORY-001).

### SCENARIO 1: ERR entry with exactly one valid alternative is corrected

**Scenario ID**: REPORTING-STORY-002-S1

**GIVEN**
* A scan file with one entry whose three lines of 27 characters are (the same number 664371495 as in VALIDATION-STORY-001):

```
 _  _     _  _        _  _ 
|_ |_ |_| _|  |  ||_||_||_ 
|_||_|  | _|  |  |  | _| _|

```

* Recognition produces "664371495"; Validation marks it ERR
* 664371495 fails the checksum: weighted sum 1(5) + 2(9) + 3(4) + 4(1) + 5(7) + 6(3) + 7(4) + 8(6) + 9(6) = 5 + 18 + 12 + 4 + 35 + 18 + 28 + 48 + 54 = 222, 222 mod 11 = 2

**WHEN**
* The Operator runs BankOCR with the scan file

**THEN**
* Reporting & Correction finds exactly one alternative that passes the checksum: adding one pipe to digit position 8 (d2 = 9) turns 9 into 8, giving 664371485
* The result file contains one line: "664371485" with no marker
* 664371485 passes the checksum: weighted sum 1(5) + 2(8) + 3(4) + 4(1) + 5(7) + 6(3) + 7(4) + 8(6) + 9(6) = 5 + 16 + 12 + 4 + 35 + 18 + 28 + 48 + 54 = 220, 220 mod 11 = 0

### SCENARIO 2: ILL entry with exactly one valid alternative is corrected

**Scenario ID**: REPORTING-STORY-002-S2

**GIVEN**
* A scan file with one entry whose three lines of 27 characters are:

```
    _  _     _  _  _  _  _ 
  | _| _||_||_ |_   ||_||_|
   |_  _|  | _||_|  ||_| _|

```

* Digit position 9 (the leftmost position) is a 1 pattern missing its bottom pipe; Recognition cannot match it to any known digit and produces "?"; the remaining eight positions are recognised normally
* Recognition produces "?23456789"; Validation marks it ILL

**WHEN**
* The Operator runs BankOCR with the scan file

**THEN**
* Reporting & Correction tries alternatives for the unrecognised position; adding one pipe (the bottom pipe) to position 9 matches digit 1, giving 123456789
* 123456789 is the only alternative that passes the checksum
* The result file contains one line: "123456789" with no marker
* 123456789 passes the checksum: weighted sum 1(9) + 2(8) + 3(7) + 4(6) + 5(5) + 6(4) + 7(3) + 8(2) + 9(1) = 9 + 16 + 21 + 24 + 25 + 24 + 21 + 16 + 9 = 165, 165 mod 11 = 0

### SCENARIO 3: ILL entry with no valid alternative keeps ILL

**Scenario ID**: REPORTING-STORY-002-S3

**GIVEN**
* A scan file with one entry whose three lines of 27 characters are (the same entry as RECOGNITION-BE-002.1-S1):

```
    _  _  _  _  _  _  _  _ 
   | || || || || || || || |
   |_||_||_||_||_||_||_||_|

```

* Digit position 9 (the leftmost position) is an all-spaces pattern; Recognition cannot match it to any known digit and produces "?"; the remaining eight positions are recognised as 0
* Recognition produces "?00000000"; Validation marks it ILL

**WHEN**
* The Operator runs BankOCR with the scan file

**THEN**
* Reporting & Correction tries alternatives for the unrecognised position; no single pipe or underscore added to or removed from an empty grid produces a pattern that matches any known digit
* Reporting & Correction finds no alternative that passes the checksum
* The result file contains one line: "?00000000 ILL"

## FE

Not applicable. BankOCR is a CLI program with no graphical interface (ADR-001). The Operator reviews the corrected result file directly as plain text.

## BE

### REPORTING-BE-002.1: Correct an ERR or ILL entry when exactly one valid alternative is found

Given an entry with status ERR or ILL and its three-line scan drawing, Reporting & Correction tries all alternatives produced by adding or removing exactly one pipe or underscore from each candidate digit position. For an ERR entry the candidates are all nine positions. For an ILL entry the candidates are only the unrecognised (`?`) positions. Each alternative that matches a known digit pattern is checked against the checksum. When exactly one candidate passes, the corrected number replaces the original entry and its status is cleared.

**Architecture references:** `architecture/01-introduction-and-goals.md`, 1.2 F4; `architecture/05-building-block-view.md`, 5.3 Reporting & Correction; `architecture/06-runtime-view.md`, 6.2, 6.3; `architecture/08-cross-cutting-concepts.md`, 8.2 Status Marking

#### SCENARIO 1: ERR entry is replaced by the single valid alternative

**Scenario ID**: REPORTING-BE-002.1-S1

**GIVEN**
* An entry whose three lines of 27 characters are:

```
 _  _     _  _        _  _ 
|_ |_ |_| _|  |  ||_||_||_ 
|_||_|  | _|  |  |  | _| _|

```

* Recognition produces "664371495" with status ERR
* 664371495 fails the checksum: weighted sum 222, 222 mod 11 = 2
* Reporting & Correction tries all single-segment alternatives across all nine positions and finds exactly one that passes the checksum: adding one pipe to position 8 (d2 = 9) turns 9 into 8, giving 664371485

**WHEN**
* The correction is applied

**THEN**
* The result for this entry is "664371485" with no marker
* 664371485 passes the checksum: weighted sum 220, 220 mod 11 = 0

#### SCENARIO 2: ILL entry is replaced by the single valid alternative

**Scenario ID**: REPORTING-BE-002.1-S2

**GIVEN**
* An entry whose three lines of 27 characters are:

```
    _  _     _  _  _  _  _ 
  | _| _||_||_ |_   ||_||_|
   |_  _|  | _||_|  ||_| _|

```

* Digit position 9 (the leftmost) is a 1 pattern missing its bottom pipe; Recognition produces "?23456789" with status ILL
* Reporting & Correction tries single-segment alternatives for position 9 only; adding the bottom pipe produces digit 1, giving 123456789 as the only candidate that passes the checksum

**WHEN**
* The correction is applied

**THEN**
* The result for this entry is "123456789" with no marker
* 123456789 passes the checksum: weighted sum 165, 165 mod 11 = 0

### REPORTING-BE-002.2: Keep the original status when no valid alternative is found

Given an entry with status ERR or ILL where no single-segment alternative produces a known digit that passes the checksum, Reporting & Correction leaves the entry unchanged and passes through the original number and status to the result file.

**Architecture references:** `architecture/01-introduction-and-goals.md`, 1.2 F4; `architecture/05-building-block-view.md`, 5.3 Reporting & Correction; `architecture/08-cross-cutting-concepts.md`, 8.1 Error Handling; `architecture/08-cross-cutting-concepts.md`, 8.2 Status Marking

#### SCENARIO 1: ILL entry with no valid alternative keeps ILL

**Scenario ID**: REPORTING-BE-002.2-S1

**GIVEN**
* An entry whose three lines of 27 characters are (the same entry as RECOGNITION-BE-002.1-S1):

```
    _  _  _  _  _  _  _  _ 
   | || || || || || || || |
   |_||_||_||_||_||_||_||_|

```

* Digit position 9 (the leftmost) is an all-spaces pattern; Recognition produces "?00000000" with status ILL
* Reporting & Correction tries single-segment alternatives for position 9; no single pipe or underscore added to or removed from an empty grid produces a pattern that matches any known digit

**WHEN**
* The correction attempt completes

**THEN**
* The result for this entry is "?00000000 ILL"

## INFRA

### REPORTING-INFRA-002.1: Deployment

See REPORTING-INFRA-001.1. No additional deployment configuration is needed for correction; it is part of the same Reporting & Correction module and Docker image.

**Architecture references:** `architecture/09-architecture-decisions.md`, ADR-001, ADR-002, ADR-004; `architecture/07-deployment-view.md`

#### SCENARIO 1: BankOCR corrects an ERR entry inside the container

**Scenario ID**: REPORTING-INFRA-002.1-S1

**GIVEN**
* The BankOCR image has been built with `docker build -t bankocr .`
* A `data` folder on the local machine contains a `scan.txt` with one entry representing 664371495 (the same three-line drawing as REPORTING-STORY-002-S1)

**WHEN**
* The Operator runs `docker run --rm -v "$(pwd)/data":/data bankocr`

**THEN**
* `data/result.txt` on the local machine contains one line: "664371485" with no marker
* The container exits with code 0

### Data store

See REPORTING-INFRA-001.2. There is no database; the scan file and result file are plain text files in the mounted data folder. No change is needed for this story.

### Event handling

Not applicable. The CLI Entry Point runs the modules in a fixed order, without events (`architecture/04-solution-strategy.md`, 4.2).

### Monitoring

See REPORTING-INFRA-001.3. A corrected entry is a normal result, not an error. Reporting & Correction writes nothing to standard error when it replaces an ERR or ILL entry. An entry that keeps its ERR or ILL status because no alternative was found is also a normal result (`architecture/08-cross-cutting-concepts.md`, 8.1, 8.3).

### Test environment

See RECOGNITION-INFRA-001.4: Test environment. The test environment is shared by all stories and is described once in the Recognition bundle.

## Implementation Order

1. REPORTING-BE-002.1: Correct an ERR or ILL entry when exactly one valid alternative is found
2. REPORTING-BE-002.2: Keep the original status when no valid alternative is found
3. REPORTING-INFRA-002.1-S1: end-to-end container check; no infrastructure change is needed (the image from REPORTING-INFRA-001.1 is reused)
4. REPORTING-STORY-002-S1: end-to-end check of ERR correction
5. REPORTING-STORY-002-S2: end-to-end check of ILL correction
6. REPORTING-STORY-002-S3: end-to-end check of ILL with no correction

## Traceability

| Scenario ID | Architecture | Parent story | Testable assertion (THEN) |
|---|---|---|---|
| REPORTING-STORY-002-S1 | 5.3 Reporting & Correction; 1.2 F4; 6.3; 8.2 | REPORTING-STORY-002 | Result file contains "664371485" with no marker; 664371485 passes checksum (sum 220, 220 mod 11 = 0) |
| REPORTING-STORY-002-S2 | 5.3 Reporting & Correction; 1.2 F4; 6.2; 8.2 | REPORTING-STORY-002 | Result file contains "123456789" with no marker; 123456789 passes checksum (sum 165, 165 mod 11 = 0) |
| REPORTING-STORY-002-S3 | 5.3 Reporting & Correction; 1.2 F4; 8.1; 8.2 | REPORTING-STORY-002 | Result file contains "?00000000 ILL" |
| REPORTING-BE-002.1-S1 | 1.2 F4; 5.3; 6.3; 8.2 | REPORTING-BE-002.1 | Result is "664371485" with no marker; sum 220, 220 mod 11 = 0 |
| REPORTING-BE-002.1-S2 | 1.2 F4; 5.3; 6.2; 8.2 | REPORTING-BE-002.1 | Result is "123456789" with no marker; sum 165, 165 mod 11 = 0 |
| REPORTING-BE-002.2-S1 | 1.2 F4; 5.3; 8.1; 8.2 | REPORTING-BE-002.2 | Result is "?00000000 ILL" |
| REPORTING-INFRA-002.1-S1 | 9 ADR-001, ADR-002, ADR-004; 7 Deployment View | REPORTING-INFRA-002.1 | data/result.txt contains "664371485" with no marker; container exits with code 0 |
