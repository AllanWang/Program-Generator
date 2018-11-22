from enum import Enum, unique
from typing import Optional


class Condition:

    def __init__(self, description):
        self.description = description


class OneArgCondition(Condition):

    def __init__(self, description, value: int):
        super().__init__(description)
        self.value = value


class GT(OneArgCondition):

    def __init__(self, description, value: int):
        super().__init__(description, value)


@unique
class ConditionFactory(Enum):
    GT = "greater than"
    LT = "less than"

    @property
    def get_condition(self) -> Optional[Condition]:
        pass
