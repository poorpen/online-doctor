import pytest
from passlib.context import CryptContext

from src.domain.user.services.password import PasswordService
from src.domain.user.value_objects.user import Password
from src.domain.user.exceptions.user import PasswordMismatch


@pytest.fixture()
def password_service():
    return PasswordService(
        CryptContext(schemes=['bcrypt'], deprecated="auto")
    )


def test_invalid_verify_password(password_service):
    password = Password('69420228')
    hashed_password = password_service.hash_password(password + 's')
    with pytest.raises(PasswordMismatch):
        password_service.verify_password(hashed_password, password)


def test_verify_password(password_service):
    password = Password('69420228')
    hashed_password = password_service.hash_password(password)
    assert password_service.verify_password(hashed_password, password) is None
