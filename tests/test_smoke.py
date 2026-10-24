def test_recognition_infra_001_4_s4_tests_can_import_bankocr_from_src():
    # GIVEN the project structure has source code in src/bankocr and tests in tests/
    # WHEN docker run --rm --entrypoint pytest bankocr is run
    import bankocr

    # THEN the tests can import the bankocr package from src/
    # because the image sets PYTHONPATH to /app/src
    assert bankocr is not None
