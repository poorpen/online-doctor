import uuid
import pytest
from datetime import datetime

from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.med_card.models.anamesis_vitae_point import AnamnesisVitaePoint
from src.domain.med_card.models.med_card import MedCard
from src.domain.med_card.value_objects.common import MedCardUUID
from src.domain.med_card.value_objects.anamnesis_vitae_point import CategoryID, AnswerID
from src.domain.med_card.value_objects.med_card import Height, Weight, PatientUUID, DateTimeOfBirth


@pytest.fixture()
def med_card():
    return MedCard(uuid=UUIDVO(uuid.uuid4()),
                   patient_uuid=PatientUUID(uuid.uuid4()),
                   height=Height(173),
                   weight=Weight(175),
                   date_of_birth=DateTimeOfBirth(datetime(year=1889, month=4, day=20)))


def test_add_answer(med_card):
    old_answers_ids = [AnswerID(1), AnswerID(3)]
    new_answers_ids = [AnswerID(1), AnswerID(3), AnswerID(5), AnswerID(10)]
    category_id = CategoryID(1)
    med_card.update_answers_in_anamnesis_vitae(answers_ids=old_answers_ids, category_id=category_id)
    med_card.update_answers_in_anamnesis_vitae(answers_ids=new_answers_ids, category_id=category_id)
    expected_anamnesis_vitae_point = AnamnesisVitaePoint(
        medcard_uuid=MedCardUUID(med_card.uuid.get_value()),
        answers_ids=[],
        category_id=category_id
    )
    expected_anamnesis_vitae_point.update_answers([*old_answers_ids, *new_answers_ids])
    assert expected_anamnesis_vitae_point in med_card.anamnesis_vitae and len(med_card.anamnesis_vitae) == 1


def test_delete_answer(med_card):
    old_answers_ids = [AnswerID(1), AnswerID(3), AnswerID(5), AnswerID(10)]
    new_answers_ids = [AnswerID(1), AnswerID(3)]
    category_id = CategoryID(1)
    med_card.update_answers_in_anamnesis_vitae(answers_ids=old_answers_ids, category_id=category_id)
    med_card.update_answers_in_anamnesis_vitae(answers_ids=new_answers_ids, category_id=category_id)
    expected_anamnesis_vitae_point = AnamnesisVitaePoint(
        medcard_uuid=MedCardUUID(med_card.uuid.get_value()),
        answers_ids=new_answers_ids,
        category_id=category_id
    )
    assert expected_anamnesis_vitae_point in med_card.anamnesis_vitae and len(med_card.anamnesis_vitae) == 1


def test_add_not_selected_answers(med_card):
    old_answers_ids = [AnswerID(1), AnswerID(3), AnswerID(5), AnswerID(10)]
    new_answers_ids = [AnswerID(15), AnswerID(33), AnswerID(25)]
    category_id = CategoryID(1)
    med_card.update_answers_in_anamnesis_vitae(answers_ids=old_answers_ids, category_id=category_id)
    med_card.update_answers_in_anamnesis_vitae(answers_ids=new_answers_ids, category_id=category_id)
    expected_anamnesis_vitae_point = AnamnesisVitaePoint(
        medcard_uuid=MedCardUUID(med_card.uuid.get_value()),
        answers_ids=sorted(new_answers_ids),
        category_id=category_id
    )
    assert expected_anamnesis_vitae_point in med_card.anamnesis_vitae and len(med_card.anamnesis_vitae) == 1


def test_add_with_dupl(med_card):
    answers_ids = [AnswerID(15), AnswerID(33), AnswerID(25), AnswerID(25)]
    category_id = CategoryID(1)
    med_card.update_answers_in_anamnesis_vitae(answers_ids=answers_ids, category_id=category_id)
    expected_anamnesis_vitae_point = AnamnesisVitaePoint(
        medcard_uuid=MedCardUUID(med_card.uuid.get_value()),
        answers_ids=[AnswerID(15), AnswerID(25), AnswerID(33)],
        category_id=category_id
    )
    assert expected_anamnesis_vitae_point in med_card.anamnesis_vitae and len(med_card.anamnesis_vitae) == 1
