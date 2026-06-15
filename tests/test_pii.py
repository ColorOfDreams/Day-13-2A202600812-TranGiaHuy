from app.pii import scrub_text


def test_scrub_email() -> None:
    out = scrub_text("Email me at student@vinuni.edu.vn")
    assert "student@" not in out
    assert "REDACTED_EMAIL" in out


def test_scrub_vietnamese_phone() -> None:
    out = scrub_text("Call me at 090 123 4567 or +84.912.345.678")
    assert "090 123 4567" not in out
    assert "+84.912.345.678" not in out
    assert out.count("REDACTED_PHONE_VN") == 2


def test_scrub_cccd() -> None:
    out = scrub_text("My CCCD is 012345678901")
    assert "012345678901" not in out
    assert "REDACTED_CCCD" in out


def test_scrub_credit_card() -> None:
    out = scrub_text("Use card 4111 1111 1111 1111")
    assert "4111" not in out
    assert "REDACTED_CREDIT_CARD" in out


def test_scrub_passport() -> None:
    out = scrub_text("Passport B12345678 belongs to me")
    assert "B12345678" not in out
    assert "REDACTED_PASSPORT" in out


def test_scrub_vietnamese_address() -> None:
    out = scrub_text("Ship to 123 đường Nguyễn Huệ, phường Bến Nghé, quận 1")
    assert "Nguyễn Huệ" not in out
    assert "quận 1" not in out
    assert "REDACTED_VN_ADDRESS" in out
