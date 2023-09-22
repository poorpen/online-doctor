from typing import List
from dataclasses import dataclass, field

from src.common.domain.models.entity import Entity
from src.common.domain.value_objects.identifiers import UUIDVO

from src.domain.med_card.value_objects.anamnesis_vitae_point import CategoryID, AnswerID, PointUUID


@dataclass
class AnamnesisPointAnswer(Entity):
    point_id: PointUUID
    answer_id: AnswerID


@dataclass
class AnamnesisVitaePoint(Entity):
    uuid: UUIDVO
    med_card_uuid: UUIDVO
    category_id: CategoryID
    answers_ids: List[AnamnesisPointAnswer] = field(default_factory=list)

    def update_answers(self, answers_ids: List[AnswerID]) -> None:
        new_answers = []
        for index, answer in enumerate(answers_ids):
            if answer not in answers_ids[:index]:
                new_answers.append(
                    AnamnesisPointAnswer(point_id=PointUUID(self.uuid.get_value()), answer_id=answer)
                )
        self.answers_ids = sorted(new_answers, key=lambda x: x.answer_id.get_value())

    @property
    def anamnesis_category_id(self) -> CategoryID:
        return self.category_id
