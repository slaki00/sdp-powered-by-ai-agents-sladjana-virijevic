# 1. Introduction and Goals

## 1.1 Introduction

A bank receives large quantities of paper documents, such as letters and
payment slips, each bearing a 9-digit account number. A scanning machine
digitises the documents and produces a text file in which every digit is
"drawn" with underscores (`_`), pipes (`|`) and spaces. Bank clerks currently
transcribe these numbers by hand, which is slow and error-prone.

**BankOCR** is a command-line program that automates this workflow. It reads
the scan file, recognises each 9-digit account number, validates it with a
checksum, attempts to correct wrong or unreadable entries, and writes a
result file that clerks can review. The program runs locally in a Docker
container; no server, database or network connection is required.

## 1.2 Requirements Overview

| ID  | Requirement | Description |
|-----|-------------|-------------|
| F1  | Read scan file | Read a text file produced by the scanner and convert each 4-line entry (3 lines of 27 characters + 1 blank line) into a 9-digit account number. |
| F2  | Validate checksum | For each recognised number, verify the checksum: `(1·d₁ + 2·d₂ + … + 9·d₉) mod 11 = 0`, where d₁ is the rightmost digit and d₉ is the leftmost digit. |
| F3  | Write result file | Produce an output file with one account number per line. Append `ERR` when the checksum fails, `ILL` when a digit could not be recognised, and `AMB` when more than one correction is possible. |
| F4  | Attempt correction | For entries marked `ERR` or `ILL`, try alternative digit interpretations. If exactly one alternative passes the checksum, replace the number and clear the flag. If more than one passes, mark the entry `AMB`. If no alternative passes, the entry keeps its `ERR` or `ILL` status. |

## 1.3 Quality Goals

Three quality goals drive the architecture. They are listed in priority order;
when two goals conflict, the higher-priority goal wins.

1. **Accuracy:** A wrong account number must never be reported as valid. Every
   number with an unreadable digit, a failed checksum, or an ambiguous
   correction must be flagged (`ILL`, `ERR`, or `AMB`). This is the top priority
   because an incorrect number could misdirect a payment.

2. **Robustness:** A single bad entry must not stop the file. If an entry is
   unreadable or invalid, it is marked and processing continues with the next
   entry. The program always produces a result for every entry in the file.

3. **Maintainability:** The recognition rules, the checksum formula and the
   correction logic live in separate modules. Each module can be tested on its
   own with small text inputs and changed without risking the others.

> Performance is not a quality goal. The scan file is small, so speed is not a
> concern.

## 1.4 Stakeholders

| Stakeholder | Role | Expectations |
|-------------|------|--------------|
| **Operator** | Bank clerk who submits the scan file and reviews the result file. | Suspicious numbers are clearly flagged (`ERR`, `ILL`, `AMB`) so that only those need manual checking. Valid numbers are listed without extra notation. |
| **Scanner Operator** | Technician who configures and runs the scanning machine. | The system correctly reads the file format the scanner produces: entries of 4 lines, each with 3 lines of 27 characters and a blank separator line. |
| **Development Team** | Developers who build, test and maintain the program. | Clear separation into modules (recognition, validation, reporting & correction), each independently testable with plain text input. |
| **Bank System** | Downstream system that uses the validated account numbers to process payments. | Never receives an incorrect number marked as valid. Every number it receives is either valid or explicitly flagged for review. |
