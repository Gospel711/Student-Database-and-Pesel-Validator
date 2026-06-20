def validate_pesel(pesel: str) -> bool:
    """
    Validate PESEL using official checksum algorithm.
    Returns True if valid, False otherwise.
    """

    # PESEL must be exactly 11 digits
    if len(pesel) != 11 or not pesel.isdigit():
        return False

    # Official PESEL weights
    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]

    # Multiply digits by weights and sum
    total = sum(int(d) * w for d, w in zip(pesel[:10], weights))

    # Compute checksum digit
    checksum = (10 - (total % 10)) % 10

    # Compare with last digit
    return checksum == int(pesel[10])