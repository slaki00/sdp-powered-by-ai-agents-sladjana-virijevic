from bankocr.validation import assign_status, checksum_passes, weighted_sum


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


def test_validation_be_001_1_s2_checksum_fails():
    # GIVEN the recognised digits 664371495
    digits = "664371495"

    # WHEN the checksum is calculated
    total = weighted_sum(digits)
    passes = checksum_passes(digits)

    # THEN the weighted sum is 222
    assert total == 222
    # AND 222 mod 11 is 2, so the checksum fails
    assert passes is False


def test_validation_be_001_2_s1_valid_number_has_no_marker():
    # GIVEN a recognised account number 345882865
    digits = "345882865"

    # WHEN the validation status is assigned
    status = assign_status(digits)

    # THEN the number is valid and has no marker
    assert status == ""
