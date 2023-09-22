import uuid

import pytest
from unittest.mock import patch, Mock
from datetime import datetime

from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.med_card.models.anamesis_vitae_point import AnamnesisVitaePoint, AnamnesisPointAnswer
from src.domain.med_card.models.med_card import MedCard
from src.domain.med_card.value_objects.common import FirstName, LastName, MiddleName
from src.domain.med_card.value_objects.anamnesis_vitae_point import CategoryID, AnswerID, PointUUID
from src.domain.med_card.value_objects.med_card import Height, Weight, PatientUUID, \
    DateTimeOfBirth
from src.domain.med_card.enum.gender import Gender


@pytest.fixture()
def med_card():
    return MedCard(uuid=UUIDVO(uuid.uuid4()),
                   first_name=FirstName('walter'),
                   last_name=LastName('hartwel'),
                   middle_name=MiddleName('white'),
                   patient_uuid=PatientUUID(uuid.uuid4()),
                   height=Height(173),
                   weight=Weight(175),
                   datetime_of_birth=DateTimeOfBirth(datetime(year=1889, month=4, day=20)),
                   gender=Gender('MALE'))


@pytest.fixture()
def anamnesis_params():
    return uuid.uuid4(), CategoryID(1)


@pytest.fixture
def expected_anamnesis_vitae_point(anamnesis_params, med_card):
    generated_uuid, category_id = anamnesis_params
    return AnamnesisVitaePoint(
        uuid=UUIDVO(generated_uuid),
        med_card_uuid=med_card.uuid,
        answers_ids=[],
        category_id=category_id
    )


@patch('src.domain.med_card.models.med_card.uuid4')
@pytest.mark.parametrize(
    'test_params', [
        ([AnswerID(1), AnswerID(3)], [AnswerID(1), AnswerID(3), AnswerID(5), AnswerID(10)]),
        ([], [AnswerID(1), AnswerID(3), AnswerID(5), AnswerID(10)]),
        ([AnswerID(10), AnswerID(32), AnswerID(3), AnswerID(12)], [AnswerID(1), AnswerID(3)])
    ]
)
def test_update_answers(mock_uuid, expected_anamnesis_vitae_point, med_card, anamnesis_params, test_params):
    generated_uuid, category_id = anamnesis_params
    old_answers_ids, new_answers_ids = test_params
    mock_uuid.return_value = generated_uuid
    med_card.update_answers_in_anamnesis_vitae(answers_ids=old_answers_ids, category_id=category_id)
    med_card.update_answers_in_anamnesis_vitae(answers_ids=new_answers_ids, category_id=category_id)
    expected_anamnesis_vitae_point.answers_ids = [
        AnamnesisPointAnswer(point_id=PointUUID(generated_uuid), answer_id=answer) for answer in
        new_answers_ids]
    assert expected_anamnesis_vitae_point in med_card.anamnesis_vitae and len(med_card.anamnesis_vitae) == 1


@patch('src.domain.med_card.models.med_card.uuid4')
@pytest.mark.parametrize(
    'answers_ids', [
        ([AnswerID(1), AnswerID(1), AnswerID(3), AnswerID(5), AnswerID(10), AnswerID(3)]),
        ([AnswerID(1), AnswerID(10), AnswerID(5), AnswerID(10)]),
        ([AnswerID(x) for _ in range(10) for x in [1, 5, 6, 7]]),
        ([AnswerID(3), AnswerID(3), AnswerID(3), AnswerID(3), AnswerID(3), AnswerID(3), AnswerID(3)])
    ]
)
def test_add_duplicates_answers(mock_uuid, expected_anamnesis_vitae_point, med_card, anamnesis_params, answers_ids):
    generated_uuid, category_id = anamnesis_params
    mock_uuid.return_value = generated_uuid
    med_card.update_answers_in_anamnesis_vitae(answers_ids=answers_ids, category_id=category_id)
    expected_anamnesis_vitae_point.answers_ids = sorted([
        AnamnesisPointAnswer(point_id=PointUUID(generated_uuid), answer_id=answer)
        for index, answer in enumerate(answers_ids)
        if answer not in answers_ids[:index]
    ], key=lambda x: x.answer_id)
    assert expected_anamnesis_vitae_point in med_card.anamnesis_vitae and len(med_card.anamnesis_vitae) == 1
