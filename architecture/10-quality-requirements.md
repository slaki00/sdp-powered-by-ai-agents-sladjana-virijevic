# 10. Quality Requirements

## 10.1 Quality Tree

```
BankOCR
├── Accuracy
│   ├── Correct checksum validation
│   ├── Unreadable digits never reported as valid
│   └── Ambiguous corrections marked AMB
├── Robustness
│   └── One bad entry does not stop the file
└── Maintainability
    ├── Modules independently testable
    └── No external dependencies
```

## 10.2 Quality Scenarios

### Scenario 1: Correct checksum validation (Accuracy)

| Field | Value |
|-------|-------|
| Context | A scan file contains a valid 9-digit account number that passes the checksum. |
| Event | The Operator runs BankOCR on the file. |
| Expected result | The number appears in the result file with no status marker. |

### Scenario 2: Unreadable digit (Accuracy)

| Field | Value |
|-------|-------|
| Context | A scan file contains an entry where one digit does not match any known pattern, and no alternative digit interpretation passes the checksum. |
| Event | The Operator runs BankOCR on the file. |
| Expected result | The entry appears in the result file marked `ILL`. It is not reported as valid. |

### Scenario 3: Ambiguous correction (Accuracy)

| Field | Value |
|-------|-------|
| Context | A scan file contains an entry with a bad checksum where two different corrections both pass the checksum. |
| Event | The Operator runs BankOCR on the file. |
| Expected result | The entry appears in the result file marked `AMB`. Neither correction is chosen over the other. |

### Scenario 4: One bad entry does not stop the file (Robustness)

| Field | Value |
|-------|-------|
| Context | A scan file contains 500 entries. Entry 250 is unreadable. |
| Event | The Operator runs BankOCR on the file. |
| Expected result | The result file contains 500 lines. Entry 250 is marked `ILL`. Entries 1 to 249 and 251 to 500 are processed normally. |

### Scenario 5: Modules independently testable (Maintainability)

| Field | Value |
|-------|-------|
| Context | A developer changes the correction logic in Reporting & Correction. |
| Event | The developer runs the tests for Reporting & Correction only. |
| Expected result | The tests pass without running Recognition or Validation. No other module is affected. |

### Scenario 6: No external dependencies (Maintainability)

| Field | Value |
|-------|-------|
| Context | The Operator's machine has only Docker installed. |
| Event | The Operator starts the container. |
| Expected result | The program runs. No Python installation or external package install is needed on the local machine. |
