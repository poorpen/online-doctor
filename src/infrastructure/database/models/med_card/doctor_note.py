from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.types import String, UUID
from sqlalchemy.orm import composite

from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.med_card.value_objects.common import FirstName, LastName, MiddleName
from src.domain.med_card.value_objects.doctor_note import AnamnesisMorbi, Diagnosis, TreatmentPlan, DoctorUUID
from src.domain.med_card.models.doctor_note import DoctorNote

from src.common.infrastructure.database.models.base import metadata_obj, mapper_registry

doctor_note = Table(
    'doctors_notes',
    metadata_obj,
    Column('uuid', UUID, nullable=False),
    Column('med_card_uuid', UUID, ForeignKey('med_cards.uuid'), nullable=False),
    Column('doctor_uuid', UUID, ForeignKey('users.uuid')),
    Column('doctor_first_name', String(60), nullable=False),
    Column('doctor_last_name', String(60), nullable=False),
    Column('doctor_middle_name', String(60), nullable=False),
    Column('diagnosis', String(350), nullable=False),
    Column('anamnesis_morbi', String(350), nullable=False),
    Column('treatment_plan', String(350), nullable=False),
)


def map_doctor_note() -> None:
    mapper_registry.map_imperatively(
        DoctorNote,
        doctor_note,
        properties={
            'uuid': composite(UUIDVO, doctor_note.c.uuid),
            'med_card_uuid': composite(UUIDVO, doctor_note.c.med_card_uuid),
            'doctor_uuid': composite(DoctorUUID, doctor_note.c.doctor_uuid),
            'diagnosis': composite(Diagnosis, doctor_note.c.diagnosis),
            'doctor_first_name': composite(FirstName, doctor_note.c.doctor_first_name),
            'doctor_last_name': composite(LastName, doctor_note.c.doctor_last_name),
            'doctor_middle_name': composite(MiddleName, doctor_note.c.doctor_middle_name),
            'anamnesis_morbi': composite(AnamnesisMorbi, doctor_note.c.anamnesis_morbi),
            'treatment_plan': composite(TreatmentPlan, doctor_note.c.treatment_plan)
        },
        column_prefix="_"
    )
