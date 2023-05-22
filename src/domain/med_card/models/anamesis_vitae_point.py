from typing import List
from dataclasses import dataclass, field

from src.common.domain.models.entity import Entity

from src.domain.med_card.value_objects.common import MedCardUUID
from src.domain.med_card.exceptions.anamnesis_vitae_point import AnswerAlreadySelected, AnswerNotSelected
from src.domain.med_card.value_objects.anamnesis_vitae_point import CategoryID, AnswerID


@dataclass
class AnamnesisVitaePoint(Entity):
    medcard_uuid: MedCardUUID
    category_id: CategoryID
    answers_ids: List[AnswerID] = field(default_factory=list)

    def add_answer(self, answers_ids: List[AnswerID]) -> None:
        set_add_answer_ids = set(answers_ids)
        set_answer_ids = set(self.answers_ids)
        existed = set_add_answer_ids.intersection(set_answer_ids)
        if existed:
            raise AnswerAlreadySelected(existed.pop())
        self.answers_ids = sorted(list(set_answer_ids.union(set_add_answer_ids)))

    def delete_answer(self, answers_ids: List[AnswerID]) -> None:
        set_delete_answer_ids = set(answers_ids)
        set_answer_ids = set(self.answers_ids)
        unselected_answers = set_delete_answer_ids.difference(set_answer_ids)
        if unselected_answers:
            raise AnswerNotSelected(unselected_answers.pop())
        self.answers_ids = sorted(list(set_answer_ids - set_delete_answer_ids))

    @property
    def anamnesis_category_id(self) -> CategoryID:
        return self.category_id
