def format_result_line(account_number: str, status: str) -> str:
    """Format one result line from an account number and its validation status."""
    if status:
        return f"{account_number} {status}"
    return account_number


def write_result_file(lines: list[str], output_path: str) -> None:
    """Write formatted result lines to the result file, one line per entry."""
    with open(output_path, "w") as f:
        f.write("\n".join(lines) + "\n")
