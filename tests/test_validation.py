from bankocr.validation import checksum_passes, weighted_sum


def test_validation_be_001_1_s1_checksum_passes():
    # GIVEN the recognised digits 345882865
    digits = "345882865"

    # WHEN the checksum is calculated
    total = weighted_sum(digits)
    passes = checksum_passes(digits)

    # THEN the weighted sum is 231
    assert total == 231
    # AND 231 mod 11 is 0, so the checksum passes
    assert passes is True
