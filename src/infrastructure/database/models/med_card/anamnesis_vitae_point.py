from sqlalchemy import ForeignKey, Table, Column, Integer, UUID, String
from sqlalchemy.orm import composite, relationship

from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.med_card.value_objects.anamnesis_vitae_point import CategoryID, AnswerID, PointUUID
from src.domain.med_card.models.anamesis_vitae_point import AnamnesisVitaePoint, AnamnesisPointAnswer
from src.common.infrastructure.database.models.base import metadata_obj, mapper_registry

anamnesis_category = Table(
    'anamnesis_categories',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String(60), nullable=False)

)

answer_for_category = Table(
    'answers_for_anamnesis_categories',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String(60), nullable=False),
    Column('category_id', Integer, ForeignKey('anamnesis_categories.id'))
)

anamnesis_vitae_point = Table(
    'anamnesis_vitae_points',
    metadata_obj,
    Column('uuid', UUID, primary_key=True),
    Column('med_card_uuid', UUID, ForeignKey('med_cards.uuid'), nullable=False),
    Column('category_id', Integer, ForeignKey('anamnesis_categories.id'), nullable=False)
)

answer_for_anamnesis_point = Table(
    'answers_for_anamnesis_point',
    metadata_obj,
    Column('point_uuid', UUID, ForeignKey('anamnesis_vitae_points.uuid'), primary_key=True),
    Column('answer_id', Integer, ForeignKey('answers.id'), primary_key=True)
)


def map_anamnesis_point() -> None:
    mapper_registry(
        AnamnesisPointAnswer,
        answer_for_anamnesis_point,
        properties={
            'point_id': composite(PointUUID, answer_for_anamnesis_point.c.point_uuid),
            'answer_id': composite(AnswerID, answer_for_anamnesis_point.c.answer_id)
        },
        column_prefix='_'

    )
    mapper_registry(
        AnamnesisVitaePoint,
        anamnesis_vitae_point,
        properties={
            'uuid': composite(UUIDVO, anamnesis_vitae_point.c.uuid),
            'med_card_uuid': composite(UUIDVO, anamnesis_vitae_point.c.med_card_uuid),
            'category_id': composite(CategoryID, anamnesis_vitae_point.c.med_card_uuid),
            'answers_ids': relationship(AnamnesisPointAnswer)
        },
        column_prefix='_'
    )
