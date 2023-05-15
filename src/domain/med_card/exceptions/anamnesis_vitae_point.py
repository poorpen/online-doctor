from dataclasses import dataclass

from src.domain.med_card.value_objects.anamnesis_vitae_point import AnswerID, CategoryID

@dataclass(frozen=True)
class AnswerAlreadySelected(Exception):
    answer_id: AnswerID


@dataclass(frozen=True)
class AnswerNotSelected(Exception):
    answer_id: AnswerID


@dataclass(frozen=True)
class AnamnesisVitaePointNotExist(Exception):
    category_id: CategoryID
