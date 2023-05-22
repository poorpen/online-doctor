from dataclasses import dataclass

from src.common.domain.models.aggregate import AggregateRoot
from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.user.value_objects.user import FirstName, LastName, MiddleName, Phone, Password
from src.domain.user.enum.role import Role


@dataclass
class User(AggregateRoot):
    uuid: UUIDVO
    first_name: FirstName
    last_name: LastName
    middle_name: MiddleName
    password: Password
    phone: Phone
    role: Role

    def change_password(self, new_password: Password):
        self.password = new_password

    def change_phone(self, new_phone_number: Phone):
        self.phone = new_phone_number
