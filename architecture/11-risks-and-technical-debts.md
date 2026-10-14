# 11. Risks and Technical Debts

## 11.1 Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|------------|--------|------------|
| R1 | A digit pattern is misrecognised, causing a wrong number to pass the checksum and be reported as valid. | Low | High | The digit patterns are defined explicitly and tested with all ten digits. Correction only accepts a candidate that passes the checksum. |
| R2 | The Scanner Operator changes the scan file format (line length or characters), so Recognition can no longer read the entries. | Low | High | The format rules are only in Recognition, so only that module needs to change. |
| R3 | The Operator mounts the wrong folder or passes wrong file paths to the container, so the CLI cannot find the scan file or writes the result file to the wrong place. | Medium | Medium | The CLI reports a clear error message to the Operator when the input file does not exist or cannot be read. |
| R4 | The checksum is implemented with the digit order reversed (d1 must be the rightmost digit), so valid numbers are marked ERR and wrong numbers could pass. | Medium | High | Test Validation with known valid and invalid account numbers. |

## 11.2 Technical Debts

| ID | Debt | Reason | Plan |
|-----|------|--------|------|
| D1 | No history of past runs is kept. Each run processes one file and produces one result file, then nothing is stored. | ADR-001 decided against a database because nothing needs to be kept between runs. | If the bank later needs reports over time, a data store can be added in a new ADR. |
| D2 | The Operator has only a command line, without a graphical interface. | ADR-001 decided on a CLI built with the standard library only. | A GUI or web interface could be added later, but would require external dependencies and a new ADR. |
| D3 | The exact Docker command and image name are not decided yet. | The architecture focuses on the structure and constraints, not the specific Docker configuration. | The Dockerfile and run command will be defined during implementation and documented in a new ADR if needed. |
