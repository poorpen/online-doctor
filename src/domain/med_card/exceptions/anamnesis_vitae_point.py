from src.common.domain.exceptions.domain import DomainException

from src.domain.med_card.value_objects.anamnesis_vitae_point import AnswerID, CategoryID


class AnswerAlreadySelected(DomainException):
    value: AnswerID


class AnswerNotSelected(DomainException):
    value: AnswerID


class AnamnesisVitaePointNotExist(DomainException):
    value: CategoryID
