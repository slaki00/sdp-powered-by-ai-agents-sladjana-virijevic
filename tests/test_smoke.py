def test_package_can_be_imported():
    # GIVEN the bankocr package is in the image
    # WHEN it is imported
    import bankocr

    # THEN the import succeeds
    assert bankocr is not None
