from uuid import UUID
from typing import List
from dataclasses import dataclass, field

from src.domain.common.models.entity import Entity

from src.domain.medcard.exceptions.anamnesis_vitae_point import AnswerAlreadySelected, AnswerNotSelected
from src.domain.medcard.value_objects.anamnesis_vitae_point import CategoryID, AnswerID


@dataclass
class AnamnesisVitaePoint(Entity):
    medcard_uuid: UUID
    category_id: CategoryID
    answers_ids: List[AnswerID] = field(default_factory=list)

    def add_answer(self, answers_ids: List[AnswerID]) -> None:
        set_add_answer_ids = set(answers_ids)
        set_answer_ids = set(self.answers_ids)
        existed = set_add_answer_ids.intersection(set_answer_ids)
        if existed:
            raise AnswerAlreadySelected(existed.pop())
        self.answers_ids = list(set_answer_ids.union(set_answer_ids))

    def delete_answer(self, answers_ids: List[AnswerID]) -> None:
        set_delete_answer_ids = set(answers_ids)
        set_answer_ids = set(self.answers_ids)
        unselected_answers = set_delete_answer_ids.difference(set_answer_ids)
        if unselected_answers:
            raise AnswerNotSelected(unselected_answers.pop())
        self.answers_ids = list(set_answer_ids - set_delete_answer_ids)
