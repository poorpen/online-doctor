from typing import Any, TypeVar

T = TypeVar("T")


class Specification:

    def is_satisfied_by(self, candidates: T) -> bool:
        raise NotImplemented

    def __and__(self, other: "Specification") -> "MultiSpecification":
        return And(self, other)

    def __or__(self, other: "Specification") -> "MultiSpecification":
        return Or(self, other)


class MultiSpecification(Specification):

    def __init__(self, *specifications):
        self.specifications = specifications


class And(MultiSpecification):

    def __and__(self, other: Specification):
        if isinstance(other, And):
            self.specifications += other.specifications
        else:
            self.specifications += (other,)
        return self

    def is_satisfied_by(self, candidate: Any) -> bool:
        return all(
            [
                specification.is_satisfied_by(candidate)
                for specification in self.specifications
            ]
        )


class Or(MultiSpecification):

    def __or__(self, other):
        if isinstance(other, Or):
            self.specifications += other.specifications
        else:
            self.specifications += (other,)
        return self

    def is_satisfied_by(self, candidate) -> bool:
        return any(
            [
                specification.is_satisfied_by(candidate)
                for specification in self.specifications
            ]
        )


