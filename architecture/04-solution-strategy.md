# 4. Solution Strategy

## 4.1 Technology Decisions

The technology decisions are recorded in ADR-001 and ADR-002:

- **Python 3.12** with the standard library only (ADR-001).
- **Plain text files** for input and output, no database (ADR-001).
- **Docker** for packaging and local execution (ADR-002).

## 4.2 System Decomposition

The program is a single CLI process with three modules, each handling one
bounded context:

1. **Recognition**: reads the scan file, splits it into 4-line entries, and
   converts the ASCII patterns of each entry into a 9-digit account number.
   Digits that cannot be recognised are marked as unreadable.

2. **Validation**: checks each recognised account number with the checksum
   formula. Numbers that fail are marked as `ERR`. Numbers with unreadable
   digits are marked as `ILL`.

3. **Reporting & Correction**: attempts to correct entries marked `ERR` or
   `ILL` by trying alternative digit interpretations. If exactly one
   alternative passes the checksum, the number is replaced. If more than one
   passes, the entry is marked `AMB`. If no alternative passes, the entry
   keeps its status. The module then writes the result file with one account
   number per line.

The CLI entry point runs the three modules in a fixed order: Recognition
reads the file, Validation checks the numbers, Reporting & Correction applies
fixes and writes the output. The modules do not call each other, so each
module stays independent.

## 4.3 Achieving the Quality Goals

### Accuracy

- The checksum is applied to every recognised number (F2).
- A number with any unreadable digit is marked `ILL` and never reported as
  valid.
- Correction only accepts a candidate if it passes the checksum. If multiple
  candidates pass, the entry is marked `AMB` rather than guessing.
- If no candidate passes, the original `ERR` or `ILL` status is kept.

### Robustness

- Each entry is processed independently. A malformed or unreadable entry is
  marked and processing continues with the next entry.
- The program always produces a result line for every entry in the input file.

### Maintainability

- Each module has one responsibility and can be tested on its own with small
  text inputs.
- The digit patterns, checksum formula and correction logic are isolated in
  their respective modules, so a change to one does not affect the others.
- No external dependencies means the only thing to install on the local
  machine is Docker, because Python 3.12 is inside the Docker image.
