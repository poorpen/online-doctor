from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.types import String, DateTime, Enum, Boolean, UUID, Integer
from sqlalchemy.orm import composite, relationship

from src.common.domain.value_objects.identifiers import UUIDVO
from src.common.infrastructure.database.models.base import metadata_obj, mapper_registry

from src.domain.med_card.models.med_card import MedCard
from src.domain.med_card.models.anamesis_vitae_point import AnamnesisVitaePoint
from src.domain.med_card.models.doctor_note import DoctorNote
from src.domain.med_card.value_objects.common import FirstName, LastName, MiddleName
from src.domain.med_card.value_objects.med_card import PatientUUID, DateTimeOfBirth, Height, Weight
from src.domain.med_card.enum.gender import Gender

med_card = Table(
    "med_cards",
    metadata_obj,
    Column('uuid', UUID, primary_key=True),
    Column('patient_uuid', UUID, ForeignKey('users.uuid')),
    Column('first_name', String(60), nullable=False),
    Column('last_name', String(60), nullable=False),
    Column('middle_name', String(60), nullable=False),
    Column('date_of_birth', DateTime(True), nullable=False),
    Column('gender', Enum(Gender), nullable=False),
    Column('height', Integer, nullable=False),
    Column('weight', Integer, nullable=False),
    Column('deleted', Boolean, nullable=False),
)


def map_med_card() -> None:
    mapper_registry(
        MedCard,
        med_card,
        properties={
            'uuid': composite(UUID, med_card.c.uuid),
            'patient_uuid': composite(PatientUUID, med_card.c.patient_uuid),
            'first_name': composite(FirstName, med_card.c.first_name),
            'last_name': composite(LastName, med_card.c.last_name),
            'middle_name': composite(MiddleName, med_card.c.middle_name),
            'datetime_of_birth': composite(DateTimeOfBirth, med_card.c.datetime_of_birth),
            'height': composite(Height, med_card.c.height),
            'weight': composite(Weight, med_card.c.weight),
            'anamnesis_vitae': relationship(AnamnesisVitaePoint, lazy=None),
            'doctor_note': relationship(DoctorNote, lazy=None)
        },
        column_prefix="_"
    )
