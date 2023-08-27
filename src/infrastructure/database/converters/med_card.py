from sqlalchemy.engine.row import Row

from typing import List, Tuple, Sequence

from src.domain.med_card.models.anamesis_vitae_point import AnamnesisVitaePoint
from src.domain.med_card.models.med_card import MedCard

from src.application.med_card.models.dto import MedCardDTO, MedCardPreviewDTO, AnamnesisVitaePointDTO, DoctorNotesDTO, \
    AnswersForCategory, AnswerDTO, DoctorNoteDTO

from src.infrastructure.database.models.med_card.category import AnamnesisCategoryDB
from src.infrastructure.database.models.med_card.answer import AnswerForAnamnesisDB
from src.infrastructure.database.models.med_card.anamnesis_vitae_point import AnamnesisVitaePointDB
from src.infrastructure.database.models.med_card.doctor_note import DoctorNoteDB
from src.infrastructure.database.models.med_card.med_card import MedCardDB


def aggregate_to_db_model(data: MedCard) -> MedCardDB:
    anamnesis_vitae = [
        AnamnesisVitaePointDB(
            med_card_uuid=point.medcard_uuid,
            category_id=point.category_id,
            answer_id=answer
        )
        for point in data.anamnesis_vitae for answer in point.answers_ids
    ]
    doctor_notes = [
        DoctorNoteDB(
            uuid=note.uuid,
            med_card_uuid=note.med_card_uuid,
            doctor_uuid=note.doctor_uuid,
            anamnesis_morbi=note.anamnesis_morbi,
            diagnosis=note.diagnosis,
            treatment_plan=note.treatment_plan
        )
        for note in data.doctor_notes
    ]
    return MedCardDB(
        uuid=data.uuid,
        patient_uuid=data.patient_uuid,
        first_name=data.first_name,
        last_name=data.last_name,
        middle_name=data.middle_name,
        datetime_of_birth=data.datetime_of_birth,
        gender=data.gender,
        height=data.height,
        weight=data.weight,
        deleted=data.deleted,
        anamnesis_vitae=anamnesis_vitae,
        doctor_notes=doctor_notes
    )


def db_model_to_aggregate(data: MedCardDB) -> MedCard:
    anamnesis_vitae = {}
    for db_point in data.anamnesis_vitae:

        if db_point.category_id not in anamnesis_vitae:
            anamnesis_vitae[db_point.category_id] = AnamnesisVitaePoint(
                medcard_uuid=db_point.med_card_uuid,
                category_id=db_point.category_id,
                answers_ids=[]
            )

        domain_point = anamnesis_vitae[db_point.category_id]
        domain_point.answers_ids.append(db_point.answer_id)

    return MedCard(
        uuid=data.uuid,
        patient_uuid=data.patient_uuid,
        first_name=data.first_name,
        last_name=data.last_name,
        middle_name=data.middle_name,
        datetime_of_birth=data.datetime_of_birth,
        gender=data.gender,
        height=data.height,
        weight=data.weight,
        deleted=data.deleted,
        anamnesis_vitae=list(anamnesis_vitae.values()),
        doctor_notes=data.doctor_notes
    )


def db_model_to_dto_preview(data: MedCardDB) -> MedCardPreviewDTO:
    return MedCardPreviewDTO(
        uuid=data.uuid,
        patient_uuid=data.patient_uuid,
        first_name=data.first_name,
        last_name=data.last_name,
        middle_name=data.middle_name,
        date_of_birth=data.datetime_of_birth,
        gender=data.gender
    )


def db_models_to_dto_previews(data: List[MedCardDB]) -> List[MedCardPreviewDTO]:
    return [db_model_to_dto_preview(model) for model in data]


def db_model_to_dto(data: MedCardDB) -> MedCardDTO:
    anamnesis_vitae = {}
    for db_point in data.anamnesis_vitae:

        if db_point.category_id not in anamnesis_vitae:
            anamnesis_vitae[db_point.category_id] = AnamnesisVitaePointDTO(
                category_id=db_point.category_id,
                category_name=db_point.category.name,
                answers_names=[]
            )

        domain_point = anamnesis_vitae[db_point.category_id]
        domain_point.answers_names.append(db_point.answer.name)

    return MedCardDTO(
        uuid=data.uuid,
        first_name=data.first_name,
        last_name=data.last_name,
        middle_name=data.middle_name,
        date_of_birth=data.datetime_of_birth,
        gender=data.gender,
        patient_uuid=data.patient_uuid,
        height=data.height,
        weight=data.weight,
        anamnesis_vitae=list(anamnesis_vitae.values())
    )


def db_answers_model_to_dto(data: Sequence[Row[Tuple[AnamnesisCategoryDB, AnswerForAnamnesisDB]]]) -> AnswersForCategory:
    return AnswersForCategory(
        category_name=data[0][0].name,
        category_id=data[0][0].id,
        answers=[AnswerDTO(answer_id=answer.id, answer_name=answer.name) for _, answer in data]
    )


def db_doctors_notes_to_dto(data: Sequence[DoctorNoteDB]) -> List[DoctorNotesDTO]:
    dto_notes = {}
    for note in data:
        if note.doctor_uuid not in dto_notes:
            dto_notes[note.doctor_uuid] = DoctorNotesDTO(
                doctor_uuid=note.doctor_uuid,
                doctor_first_name=note.doctor.first_name,
                doctor_last_name=note.doctor.last_name,
                doctor_middle_name=note.doctor.middle_name,
                notes=[]
            )

        dto_note = dto_notes[note.doctor_uuid]
        dto_note.notes.append(DoctorNoteDTO(anamnesis_morbi=note.anamnesis_morbi, diagnosis=note.diagnosis,
                                            treatment_plan=note.treatment_plan, note_uuid=note.uuid))

    return list(dto_notes.values())
