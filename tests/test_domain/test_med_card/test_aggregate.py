import uuid
import pytest
from datetime import datetime

from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.med_card.models.anamesis_vitae_point import AnamnesisVitaePoint
from src.domain.med_card.models.med_card import MedCard
from src.domain.med_card.value_objects.common import MedCardUUID
from src.domain.med_card.value_objects.anamnesis_vitae_point import CategoryID, AnswerID
from src.domain.med_card.value_objects.med_card import Height, Weight, PatientUUID, DateTimeOfBirth
from src.domain.med_card.exceptions.anamnesis_vitae_point import AnamnesisVitaePointNotExist, AnswerNotSelected, \
    AnswerAlreadySelected


@pytest.fixture()
def med_card():
    return MedCard(uuid=UUIDVO(uuid.uuid4()),
                   patient_uuid=PatientUUID(uuid.uuid4()),
                   height=Height(173),
                   weight=Weight(175),
                   date_of_birth=DateTimeOfBirth(datetime(year=1889, month=4, day=20)))


def test_add_answer_when_answer_exist(med_card):
    answers_ids = [AnswerID(10), AnswerID(4)]
    category_id = CategoryID(1)
    med_card.add_answers_in_anamnesis_vitae(answers_ids=answers_ids, category_id=category_id)
    with pytest.raises(AnswerAlreadySelected):
        med_card.add_answers_in_anamnesis_vitae(answers_ids=[answers_ids[-1]], category_id=category_id)


def test_add_answer_when_point_not_exist(med_card):
    answers_ids = [AnswerID(1), AnswerID(3)]
    category_id = CategoryID(1)
    med_card.add_answers_in_anamnesis_vitae(answers_ids=answers_ids,
                                            category_id=category_id)
    expected_anamnesis_vitae_point = AnamnesisVitaePoint(
        medcard_uuid=MedCardUUID(med_card.uuid.get_value()),
        answers_ids=answers_ids,
        category_id=category_id
    )
    assert expected_anamnesis_vitae_point in med_card.anamnesis_vitae


def test_add_answer_when_point_exist(med_card):
    old_answers_ids = [AnswerID(1), AnswerID(3)]
    new_answers_ids = [AnswerID(5), AnswerID(10)]
    category_id = CategoryID(1)
    med_card.add_answers_in_anamnesis_vitae(answers_ids=old_answers_ids, category_id=category_id)
    med_card.add_answers_in_anamnesis_vitae(answers_ids=new_answers_ids, category_id=category_id)
    expected_anamnesis_vitae_point = AnamnesisVitaePoint(
        medcard_uuid=MedCardUUID(med_card.uuid.get_value()),
        answers_ids=[*old_answers_ids, *new_answers_ids],
        category_id=category_id
    )
    assert expected_anamnesis_vitae_point in med_card.anamnesis_vitae and len(med_card.anamnesis_vitae) == 1


def test_delete_answer_when_point_not_exist(med_card):
    answers_ids = [AnswerID(10), AnswerID(7)]
    category_id = CategoryID(1)
    with pytest.raises(AnamnesisVitaePointNotExist):
        med_card.delete_answers_in_anamnesis_vitae(
            answers_ids=answers_ids, category_id=category_id
        )


def test_delete_answer_when_answer_not_exist(med_card):
    answers_ids = [AnswerID(10)]
    category_id = CategoryID(1)
    med_card.add_answers_in_anamnesis_vitae(answers_ids=answers_ids, category_id=category_id)
    with pytest.raises(AnswerNotSelected):
        med_card.delete_answers_in_anamnesis_vitae(answers_ids=[*answers_ids, AnswerID(1)], category_id=category_id)
