from uuid import UUID

from src.common.application.exceptions.base import ApplicationException


class MedCardNotFound(ApplicationException):
    value: UUID


class CurrentPatientAlreadyHaveMedCard(ApplicationException):
    value: UUID


class PatientNotFound(ApplicationException):
    value: UUID


class DoctorNotFound(ApplicationException):
    value: UUID


class CategoryIDNotFound(ApplicationException):
    value: int


class AnswerIDNotFound(ApplicationException):
    value: int


class AnswersForCurrentCategoryNotFound(ApplicationException):
    value: int


class DoctorNotesNotFound(ApplicationException):
    value: int
