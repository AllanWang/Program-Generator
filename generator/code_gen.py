from dataclasses import dataclass
from typing import List, Set


@dataclass
class CodeGen:
    imports: Set[str]
    lib_keys: Set[str]
    gen_code: List[str]
