from src.domain.common.value_objects.integer import IntegerInRange


class Height(IntegerInRange):
    min_value: int = 10
    max_value: int = 200


class Weight(IntegerInRange):
    min_value: int = 30
    max_value: int = 220
