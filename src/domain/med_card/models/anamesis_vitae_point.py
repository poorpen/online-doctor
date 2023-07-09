from typing import List
from dataclasses import dataclass, field

from src.common.domain.models.entity import Entity

from src.domain.med_card.value_objects.common import MedCardUUID
from src.domain.med_card.value_objects.anamnesis_vitae_point import CategoryID, AnswerID


@dataclass
class AnamnesisVitaePoint(Entity):
    medcard_uuid: MedCardUUID
    category_id: CategoryID
    answers_ids: List[AnswerID] = field(default_factory=list)

    def update_answers(self, answers_ids: List[AnswerID]) -> None:
        set_new_answers = set(answers_ids)
        self.answers_ids = sorted(list(set_new_answers))

    @property
    def anamnesis_category_id(self) -> CategoryID:
        return self.category_id
