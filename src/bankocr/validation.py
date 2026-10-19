def weighted_sum(digits: str) -> int:
    """Calculate the checksum weighted sum for a 9-digit account number.

    d1 is the rightmost digit (weight 1), d9 is the leftmost digit (weight 9).
    Returns (1*d1 + 2*d2 + ... + 9*d9).
    """
    total = 0
    for weight, digit in enumerate(reversed(digits), start=1):
        total += weight * int(digit)
    return total


def checksum_passes(digits: str) -> bool:
    """Return True when the weighted sum mod 11 equals 0."""
    return weighted_sum(digits) % 11 == 0
