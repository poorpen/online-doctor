from typing import Sequence, List

from sqlalchemy import RowMapping

from src.application.med_card.models.dto import MedCardDTO, AnamnesisVitaePointDTO, DoctorNotesDTO, \
    AnswersForCategory, AnswerDTO, DoctorNoteDTO


def to_med_card_dto(data: Sequence[RowMapping]) -> MedCardDTO:
    anamnesis_points = {}
    for row in data:
        if row['anamnesis_uuid'] not in anamnesis_points:
            anamnesis_points[row['anamnesis_uuid']] = AnamnesisVitaePointDTO(
                category_id=row['category_id'],
                category_name=row['category_name'],
                answers_names=[]
            )

        point = anamnesis_points['anamnesis_uuid']
        point.answers_names.append(row['answer_name'])
    first_row = data[0]
    return MedCardDTO(
        uuid=first_row['med_card_uuid'],
        first_name=first_row['first_name'],
        last_name=first_row['last_name'],
        middle_name=first_row['middle_name'],
        date_of_birth=first_row['date_of_birth'],
        gender=first_row['gender'],
        height=first_row['height'],
        weight=first_row['weight'],
        anamnesis_vitae=list(anamnesis_points.values())

    )


def to_answer_for_category_dto(data: Sequence[RowMapping]) -> AnswersForCategory:
    answers = []
    for row in data:
        answers.append(
            AnswerDTO(
                answer_id=row['answer_id'],
                answer_name=row['answer_name']
            )
        )
    first_row = data[0]
    return AnswersForCategory(
        category_id=first_row['category_id'],
        category_name=first_row['category_name'],
        answers=answers
    )


def to_doctor_notes_dto(data: Sequence[RowMapping]) -> List[DoctorNotesDTO]:
    doctors = {}
    for row in data:
        if row['doctor_uuid'] not in doctors:
            doctors[row['doctor_uuid']] = DoctorNotesDTO(
                doctor_uuid=row['doctor_uuid'],
                doctor_first_name=row['doctor_first_name'],
                doctor_last_name=row['doctor_last_name'],
                doctor_middle_name=row['doctor_middle_name'],
                notes=[]
            )
        doctor = doctors[row['doctor_uuid']]
        doctor.notes.append(
            DoctorNoteDTO(
                note_uuid=row['uuid'],
                anamnesis_morbi=row['anamnesis_morbi'],
                diagnosis=row['diagnosis'],
                treatment_plan=row['treatment_plan']
            )
        )
    return list(doctors.values())