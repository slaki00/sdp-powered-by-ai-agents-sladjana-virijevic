# 7. Deployment View

## 7.1 Infrastructure

BankOCR runs on the Operator's local machine. The machine has Docker installed.
No server, cloud service or network connection is required.

| Element | Technology | Purpose |
|---------|-----------|---------|
| Local Machine | The Operator's computer | Hosts Docker, the data folder and the BankOCR container |
| Data Folder | Local file system | Contains the scan file and the result file; mounted into the container as a volume |
| Docker Engine | Docker | Runs the BankOCR container |
| BankOCR Container | Docker image with Python 3.12 | Runs the CLI process that processes the scan file |
| Scan File | Plain text file in the data folder | Input: 4-line entries with ASCII digits |
| Result File | Plain text file in the data folder | Output: one account number per line with status flags |

## 7.2 Deployment Diagram

![Deployment](diagrams/deployment-view.svg)

## 7.3 How It Runs

1. The Operator places the scan file in a folder on the local machine.
2. The Operator starts the BankOCR container with Docker, mounting that folder
   as a volume into the container.
3. Docker runs the container, which starts a single CLI process.
4. The CLI reads the scan file and writes the result file through the mounted
   volume. Python 3.12 is inside the Docker image, so no Python installation is
   needed on the local machine.
5. When the CLI finishes, the container exits.
6. The Operator reviews the result file in the same folder on the local
   machine.
