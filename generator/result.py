from dataclasses import dataclass

from generator.condition import Condition


@dataclass
class Result:
    tokens: [str]
    formatted_tokens: []
    fully_parsed: bool
    conditions: [Condition]
