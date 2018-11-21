from typing import Optional

from .nodes import *
from .result import Result


def generate(query: Optional[str]) -> Result:
    return Result("Blank", "Blank", Blank())
