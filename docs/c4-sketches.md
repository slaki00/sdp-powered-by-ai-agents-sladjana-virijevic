## Level 1 - System Context

![Level 1](img/c4-level1.png)

BankOCR gets scan files from the scanner and the operator, and sends the results to the bank system. The operator also checks the numbers that are marked as ERR, ILL or AMB.

## Level 2 - Container

![Level 2](img/c4-level2.png)

BankOCR is a program that reads input files and writes result files. Recognition, Validation and Reporting are parts of that program, so they are not separate containers.
