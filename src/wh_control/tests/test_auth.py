from warehouse_service.application.auth import PasswordHasher, AuthCryptoSettings


def test_pwd_hash():
    password_hasher = PasswordHasher(AuthCryptoSettings())
    password = "asdf"
    pwd_hash_and_salt = password_hasher.hash_password(password)
    assert password_hasher.verify_password_hash(
        hashed_password_and_salt=pwd_hash_and_salt,
        password=password,
    ) is True


def test_pwd_hash_check_fails_different_pwd():
    password_hasher = PasswordHasher(AuthCryptoSettings())
    password = "asdf"
    different_password = "asdfg"
    pwd_hash_and_salt = password_hasher.hash_password(password)
    assert password_hasher.verify_password_hash(
        hashed_password_and_salt=pwd_hash_and_salt,
        password=different_password,
    ) is False