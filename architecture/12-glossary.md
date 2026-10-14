# 12. Glossary

| Term | Definition |
|------|-----------|
| **?** | Marker for an unreadable digit in an entry. |
| **Account number** | A 9-digit number that identifies a bank account. |
| **AMB** | Status marker for an entry where more than one correction passes the checksum. |
| **ASCII digit** | A digit drawn with underscores (`_`), pipes (`\|`) and spaces in a 3-line by 3-character grid. |
| **Bank System** | The downstream system that uses the validated account numbers to process payments. |
| **Checksum** | A formula that verifies an account number: `(1·d₁ + 2·d₂ + … + 9·d₉) mod 11 = 0`, where d₁ is the rightmost digit and d₉ is the leftmost digit. |
| **CLI** | Command-line interface. The program is run from the terminal with arguments. |
| **CLI Entry Point** | The component that parses command-line arguments and runs the three modules in a fixed order. |
| **Docker container** | A running instance of the Docker image that executes the CLI process. |
| **Docker image** | The packaged artefact containing Python 3.12 and the BankOCR program, built for local execution. |
| **Entry** | A block of 4 lines in the scan file: 3 lines of 27 characters and one blank line, representing one account number. |
| **ERR** | Status marker for an entry where all digits are recognised but the checksum fails. |
| **ILL** | Status marker for an entry where one or more digits could not be recognised. |
| **Operator** | The bank clerk who submits the scan file to BankOCR and reviews the result file. |
| **Recognition** | The module that reads the scan file and converts ASCII digits to numeric digits. |
| **Reporting & Correction** | The module that attempts corrections, applies AMB markers, and writes the result file. |
| **Result file** | The output text file with one account number per line, optionally followed by a status marker. |
| **Scan file** | The input text file produced by the scanner, containing entries with ASCII digits. |
| **Scanner** | The machine that digitises paper documents into the scan file. |
| **Scanner Operator** | The technician who configures and runs the scanning machine. |
| **Validation** | The module that checks each account number with the checksum formula. |
| **Volume (mounted folder)** | A folder on the local machine that is mounted into the Docker container so the CLI can read the scan file and write the result file. |
