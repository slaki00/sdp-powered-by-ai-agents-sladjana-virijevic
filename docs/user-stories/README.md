# User Stories: BankOCR

Derived from the architecture in `architecture/`. Domains follow the bounded contexts in chapter 5.3.

## Domains

| Domain | Bounded context (5.3) | Requirements |
|--------|-----------------------|--------------|
| RECOGNITION | Recognition | F1 |
| VALIDATION | Validation | F2 |
| REPORTING | Reporting & Correction | F3, F4 |

The CLI Entry Point has no domain of its own: it is not a bounded context and has no business rules. Its stories belong to RECOGNITION, because Recognition reads the file the CLI passes on.

## Story Inventory

Stories are ordered by priority: a story is placed after the stories it depends on.

| # | Story ID | Story | Source | Priority | Status | Implementation |
|---|----------|-------|--------|----------|--------|----------------|
| 1 | RECOGNITION-STORY-001 | Read each entry as a 9-digit account number | F1 | Core | Done | Done (#5, #18) |
| 2 | VALIDATION-STORY-001 | Validate each number with the checksum, mark ERR when it fails | F2 | Core | Done | Done (#11) |
| 3 | REPORTING-STORY-001 | Write the result file, one number per line with its marker | F3 | Core | Done | Done (#13) |
| 4 | RECOGNITION-STORY-002 | Mark unreadable digits with ? and continue with the next entry | F1, Robustness | Supporting | Not started | Not started |
| 5 | VALIDATION-STORY-002 | Mark a number with an unreadable digit as ILL, without calculating the checksum | F2, F3 | Supporting | Not started | Not started |
| 6 | RECOGNITION-STORY-003 | Show a clear error when the scan file is missing or unreadable | 8.1, R3 | Supporting | Not started | Not started |
| 7 | REPORTING-STORY-002 | Correct an ERR or ILL entry when exactly one alternative passes | F4 | Supporting | Not started | Not started |
| 8 | REPORTING-STORY-003 | Mark AMB when more than one alternative passes | F4 | Supporting | Not started | Not started |

**Status** is the requirements work from Module 3: Done means the story bundle is written and approved. **Implementation** is the TDD work from Module 5: which scenarios have passing tests.

Total stories: 8. Core stories: 3.

## Pareto

The three core stories form the minimum usable product: the Operator gets every entry read, checked and written to the result file, and only needs to review the numbers marked ERR. They also block all other stories and together use every component.

Three of eight is more than 20% because the kata is small and the core is one chain of three steps.

## Progress

Pareto Progress: 3/3 core stories
