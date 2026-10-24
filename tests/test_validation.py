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


def test_validation_be_001_2_s2_failed_checksum_marked_err():
    # GIVEN a recognised account number 664371495
    digits = "664371495"

    # WHEN the validation status is assigned
    status = assign_status(digits)

    # THEN the number is marked ERR
    assert status == "ERR"


def test_validation_be_002_1_s1_one_unreadable_digit_causes_ill():
    # GIVEN the Recognition output for an entry is "?00000000"
    digits = "?00000000"

    # WHEN Validation checks the entry
    status = assign_status(digits)

    # THEN the ILL status is assigned
    assert status == "ILL"
    # AND no checksum calculation is performed for this entry
    # (verified implicitly: assign_status returns "ILL" without raising ValueError)


def test_validation_be_002_1_s2_nine_unreadable_digits_cause_ill():
    # GIVEN the Recognition output for an entry is "?????????"
    digits = "?????????"

    # WHEN Validation checks the entry
    status = assign_status(digits)

    # THEN the ILL status is assigned
    assert status == "ILL"
    # AND no checksum calculation is performed for this entry
    # (verified implicitly: no ValueError raised)


def test_validation_be_002_2_s1_ill_entry_passed_on_next_validated_normally():
    # GIVEN Recognition has produced two results: "?00000000" and "345882865"
    entries = ["?00000000", "345882865"]

    # WHEN Validation processes both entries
    results = [assign_status(digits) for digits in entries]

    # THEN Validation returns two results in order
    assert len(results) == 2
    # AND the first result is "?00000000" with ILL status
    assert results[0] == "ILL"
    # AND the second result is "345882865" with no marker
    # (checksum passes: weighted sum is 231, 231 mod 11 is 0)
    assert results[1] == ""
