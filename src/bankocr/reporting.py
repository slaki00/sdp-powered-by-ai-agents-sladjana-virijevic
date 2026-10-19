def format_result_line(account_number: str, status: str) -> str:
    """Format one result line from an account number and its validation status."""
    if status:
        return f"{account_number} {status}"
    return account_number
