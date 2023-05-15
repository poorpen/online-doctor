from dataclasses import dataclass

from src.domain.common.value_objects.base import BaseValueObject


@dataclass(frozen=True)
class Text(BaseValueObject[str]):
    max_len: int

    @classmethod
    def _validate(cls, v: str) -> None:
        if len(v) > cls.max_len:
            raise ValueError(f'text lenght exceeds the allowed threshold of {cls.max_len} characters')


@dataclass(frozen=True)
class NonEmptyText(Text):
    max_len: int = 500

    @classmethod
    def _validate_non_empty(cls, v: str) -> None:
        if not v or v.isspace():
            raise ValueError()

    @classmethod
    def _validate(cls, v: str) -> None:
        cls._validate_non_empty(v)
        super()._validate(v)


@dataclass(frozen=True)
class OptionalText(Text):
    max_len: int = 500
