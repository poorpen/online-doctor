from dataclasses import dataclass
from uuid import uuid4

from src.common.domain.models.aggregate import AggregateRoot
from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.user.value_objects.user import FirstName, LastName, MiddleName, Phone, Password, DateTimeOfBirth
from src.domain.user.models.user_events import UserCreated
from src.domain.user.enum.role import Role


@dataclass
class User(AggregateRoot):
    uuid: UUIDVO
    first_name: FirstName
    last_name: LastName
    middle_name: MiddleName
    date_time_of_birth: DateTimeOfBirth
    password: Password
    phone: Phone
    role: Role

    @classmethod
    def create(cls, first_name: FirstName, last_name: LastName, middle_name: MiddleName, password: Password,
               role: Role, phone: Phone, date_time_of_birth: DateTimeOfBirth) -> "User":
        user = cls(uuid=UUIDVO(uuid4()), first_name=first_name, last_name=last_name, middle_name=middle_name,
                   password=password, role=role,
                   date_time_of_birth=date_time_of_birth, phone=phone)
        user.record_event(
            UserCreated(
                user_uuid=user.uuid.get_value(),
                date_time_of_birth=user.date_time_of_birth.get_value()
            )

        )
        return user

    def change_password(self, new_password: Password):
        self.password = new_password

    def change_phone(self, new_phone_number: Phone):
        self.phone = new_phone_number
