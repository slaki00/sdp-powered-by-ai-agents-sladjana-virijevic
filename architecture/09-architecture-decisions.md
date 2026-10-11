# 9. Architecture Decisions

## ADR-001: Technology decisions (Language, Framework, Data Storage)

**Status:** Accepted

**Context:**
We need to choose the programming language, the application framework and the
way data is stored. Input and output are text files with fixed formats, each
file has about 500 entries, and nothing needs to be kept between runs.
Accuracy and easy testing matter more than speed.

**Decision:**
- **Language:** Python 3.12.
- **Framework:** No application framework. A command-line program built with
  the Python standard library only.
- **Data storage:** Plain text files on the file system. No database.

**Rationale:**
- Python 3.12 is the language set for the repository (`pyproject.toml`), and it
  has strong built-in support for reading and processing text.
- The whole job is "file in, file out", so a web application or API would add
  code and setup without adding value.
- Using only the standard library means no external dependencies to install,
  update or secure.
- Every file is processed on its own and nothing needs to be remembered between
  runs, so a database would add complexity with no benefit.
- Plain text files match the formats already required by the scanner and the
  bank system.

**Consequences:**
- (+) Simple to run, test and understand; no infrastructure to maintain.
- (+) Recognition, validation and reporting can be tested separately with small
  text inputs.
- (−) There is no history of past runs. If the bank later needs reports over
  time, a data store has to be added in a new ADR.
- (−) The operator has only a command line, without a graphical interface.
- (−) Python is slower than compiled languages, but for files of this size the
  difference is not noticeable.
