import pytest
from uuid import uuid4
from datetime import datetime

from sqlalchemy import insert

from tests.integration.test_infrastructure.test_database.conftest import session

from src.infrastructure.database.models.med_card.doctor_note import doctor_note
from src.infrastructure.database.models.med_card.med_card import med_card
from src.infrastructure.database.models.med_card.anamnesis_vitae_point import (
    anamnesis_category, answer_for_category, anamnesis_vitae_point, answer_for_anamnesis_point)


@pytest.fixture(scope="session")
def med_card_uuid():
    return uuid4()


@pytest.fixture
def data(med_card_uuid):
    first_point_uuid = uuid4()
    second_point_uuid = uuid4()
    return {
        "med_card": {
            "uuid": med_card_uuid,
            "patient_uuid": None,
            "first_name": "Ryan",
            "middle_name": "Thomas",
            "last_name": "Gosling",
            "date_of_birth": datetime(day=12, month=11, year=1980),
            "gender": "MALE",
            "height": 185,
            "weight": 80,
            "deleted": False
        },
        "doctor_note": [{
            "uuid": uuid4(),
            "med_card_uuid": med_card_uuid,
            "doctor_uuid": None,
            "doctor_first_name": "some_doctor_first_name",
            "doctor_middle_name": "some_doctor_middle_name",
            "doctor_last_name": "some_doctor_last_name",
            "diagnosis": "Ass cancer",
            "anamnesis_morbi": "Попа боль, когда много сидеть. Не нраица",
            "treatment_plan": "Свечи в помощь"
        },
            {
                "uuid": uuid4(),
                "med_card_uuid": med_card_uuid,
                "doctor_uuid": None,
                "doctor_first_name": "some_doctor_first_name",
                "doctor_middle_name": "some_doctor_middle_name",
                "doctor_last_name": "some_doctor_last_name",
                "diagnosis": "Отказ пизды",
                "anamnesis_morbi": "Все симптомы",
                "treatment_plan": "Небоходимое лечение"
            }
        ],
        "answer_for_category": [
            {
                "id": 1,
                "name": "На головном мозге",
                "category_id": 1
            },
            {
                "id": 2,
                "name": "На ногах",
                "category_id": 1
            },
            {
                "id": 3,
                "name": "Небыло",
                "category_id": 1
            },
            {
                "id": 4,
                "name": "Нет",
                "category_id": 2
            },
            {
                "id": 5,
                "name": "Пыль",
                "category_id": 2
            },
            {
                "id": 6,
                "name": "Солнце",
                "category_id": 2
            },
            {
                "id": 7,
                "name": "Перелом позвоночника",
                "category_id": 3
            },
            {
                "id": 8,
                "name": "Ушиб колена",
                "category_id": 3
            },
            {
                "id": 9,
                "name": "Отсутствуют",
                "category_id": 3
            },
        ],
        "anamnesis_category": [
            {
                "id": 1,
                "name": "Операции"
            },
            {
                "id": 2,
                "name": "Аллергии"
            },
            {
                "id": 3,
                "name": "Травмы"
            }
        ],
        "anamnesis_vitae_point": [
            {
                "uuid": first_point_uuid,
                "category_id": 1,
                "med_card_uuid": med_card_uuid
            },
            {
                "uuid": second_point_uuid,
                "category_id": 2,
                "med_card_uuid": med_card_uuid
            }
        ],
        "answer_for_anamnesis_point": [
            {
                "point_uuid": first_point_uuid,
                "answer_id": 3
            },
            {
                "point_uuid": second_point_uuid,
                "answer_id": 5
            },
            {
                "point_uuid": second_point_uuid,
                "answer_id": 6
            }
        ],

    }


@pytest.fixture(scope='session', autouse=True)
def data_prepare(session, data):
    tables = {
        "med_card": med_card,
        "doctor_note": doctor_note,
        "answer_for_anamnesis_point": answer_for_anamnesis_point,
        "answer_for_category": answer_for_category,
        "anamnesis_category": anamnesis_category,
        "anamnesis_vitae_point": anamnesis_vitae_point,
    }
    for table_name, table_data in data.items():
        session.execute(
            insert(tables[table_name]).values(table_data)
        )
    session.commit()
