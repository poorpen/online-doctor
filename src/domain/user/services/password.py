from passlib.context import CryptContext

from src.domain.user.value_objects.user import Password
from src.domain.user.exceptions.user import PasswordMismatch


class PasswordService:

    def __init__(self, hasher: CryptContext):
        self._hasher = hasher

    def hash_password(self, password: Password) -> Password:
        hashed_password = self._hasher.hash(password.get_value())
        return Password(hashed_password)

    def verify_password(self, hashed_password: Password, password: Password) -> None:
        if not self._hasher.verify(password.get_value(), hashed_password.get_value()):
            raise PasswordMismatch(password)
