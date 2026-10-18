# 8. Cross-cutting Concepts

This chapter describes rules and patterns that apply across all modules of
BankOCR.

## 8.1 Error Handling

BankOCR does not raise exceptions for bad entries. Instead, every entry gets a
status, and processing continues with the next entry.

- **Unreadable digit**: Recognition marks the digit as `?`. Validation marks
  the entry `ILL`.
- **Bad checksum**: Validation marks the entry `ERR`.
- **Ambiguous correction**: Reporting & Correction marks the entry `AMB`.
- **No correction found**: The entry keeps its `ERR` or `ILL` status.

The CLI Entry Point passes the result of each module to the next one. If a
module cannot process an entry, the entry is marked and passed along; it is
never dropped.

Errors that are not entry-specific (for example, the input file does not exist
or cannot be read) are reported to the Operator on the command line and the
program exits with a non-zero status.

## 8.2 Status Marking

Status markers are consistent across all modules:

| Marker | Meaning | Applied by |
|--------|---------|------------|
| (none) | Number is valid | Validation, or Reporting & Correction after a successful correction |
| `ERR` | Checksum failed | Validation |
| `ILL` | One or more digits could not be recognised | Validation |
| `AMB` | More than one correction passes the checksum | Reporting & Correction |

A marker set by an earlier module can be cleared by Reporting & Correction
when a single valid correction is found. An `AMB` marker always replaces the
previous `ERR` or `ILL` marker.

## 8.3 Logging

BankOCR is a CLI program. It does not write log files. Diagnostic messages go
to standard error. The result file is the only output written to disk.

## 8.4 File I/O Conventions

- Input and output are plain text files.
- The input contains only underscores, pipes, spaces and line breaks.
- The output contains digits, `?` for unreadable digits, and status markers.
- The input file is read once by Recognition.
- The result file is written once by Reporting & Correction.
- No file is kept open between modules.

## 8.5 Testing

Each module can be tested on its own with plain text input:

- **Recognition**: provide a string with 4-line entries, check the recognised
  digits.
- **Validation**: provide recognised digits, check the checksum result.
- **Reporting & Correction**: provide entries with status, check the
  corrections and the written output.

Tests do not require Docker or the other modules. Tests are run with pytest
(ADR-003).
