from dataclasses import dataclass, field
from typing import Set, Dict, Union, Callable, List, Optional, Any

from generator.ccg import parse_to_node
from generator.node import Node

CallableTemplate = Callable[[List], Any]


@dataclass
class CodeTemplate:
    key: str
    template: Union[str, CallableTemplate]
    import_keys: Set[str] = field(default_factory=set)
    lib_keys: Set[str] = field(default_factory=set)


@dataclass
class CodeGenLanguage:
    name: str
    templates: Dict[str, CodeTemplate] = field(default_factory=dict)

    @classmethod
    def from_templates(cls, name: str, templates: [CodeTemplate]) -> 'CodeGenLanguage':
        code_gen = CodeGenLanguage(name)
        for t in templates:
            code_gen.add_template(t)
        return code_gen

    def add_template(self, template: CodeTemplate):
        self.templates[template.key] = template

    def get_template(self, key: str) -> CodeTemplate:
        if key.isdigit():
            return CodeTemplate(key=key, template=key)
        return self.templates[key]

    def contains_all_keys(self, words: Set[str]):
        return set(self.templates.keys()) == words

    @dataclass
    class CodeGenHelper:
        imports: Set[str] = field(default_factory=set)
        lib_keys: Set[str] = field(default_factory=set)

    def generate_from_text(self, text: str) -> Optional[str]:
        node = Node.parse(text)
        if not node:
            return None
        return self.generate_from_node(node)

    def generate_from_node(self, node: Node) -> str:
        container = self.CodeGenHelper()
        gen_code = self._generate_from_node(node, container)
        import_string = '\n'.join(self.get_template(s).template for s in container.imports)
        lib_string = '\n'.join(self.get_template(s).template for s in container.lib_keys)
        return '\n'.join(s for s in [import_string, lib_string, gen_code] if s)

    def _generate_from_node(self, node: Node, container: CodeGenHelper):
        code_template = self.get_template(node.value)
        container.lib_keys.update(code_template.lib_keys)
        child_templates = [self._generate_from_node(c, container) for c in node.children]
        if isinstance(code_template.template, str):
            return code_template.template.format(*child_templates)
        return code_template.template(child_templates)


def python_range_template(body: [str]) -> str:
    a = int(body[0])
    b = int(body[1])
    if a > b:
        return f"reversed(range({b}, {a}+1))"
    else:
        return f"range({a}, {b}+1)"


def python_inline_negate(body: [str]) -> str:
    pre, mid, post = body[0].rpartition('if')
    if mid is '':
        raise ValueError("Attempted to negate without an if condition")
    if post.startswith(' not'):
        return f"{pre}{mid}{post[4:]}"
    else:
        return f"{pre}{mid} not{post}"


@dataclass
class ConditionTemplate:
    template: str
    negate: bool = False


def condition_template(template: str, argc: int = 0) -> CallableTemplate:
    def callable(data: []) -> [Any]:
        cond = ConditionTemplate(template.format(*data[:argc]))
        base = data_to_list(data[argc])
        base.append(cond)
        return base

    return callable


def negation_template(data: []) -> []:
    cond = data[0][-1]
    if not isinstance(cond, ConditionTemplate):
        raise ValueError("Attempted to negate an element that wasn't a condition template")
    cond.negate = not cond.negate
    return data[0]


def data_to_list(data) -> [Any]:
    if isinstance(data, list):
        return data
    if isinstance(data, str):
        return [data]
    raise ValueError("Expected string or list")


def get_templates(negate_condition: Callable[[str], str]) -> CallableTemplate:
    def converter(template: Union[str, ConditionTemplate]) -> str:
        if isinstance(template, str):
            return template
        if isinstance(template, ConditionTemplate):
            if template.negate:
                return negate_condition(template.template)
            return template.template

    def callable(data) -> [str]:
        return [converter(d) for d in data_to_list(data[0])]

    return callable


# -------------------------------------------------------
# Python
# -------------------------------------------------------

get_python_templates = get_templates(lambda x: f"not {x}")


def python_inline_program_template(data: []) -> str:
    lines = get_python_templates(data)
    code = f"(x for x in {lines[0]})"
    for cond in lines[1:]:
        code = f"(x for x in {code} if {cond})"
    return f"def code():\n\treturn list({code})"


def python_functional_program_template(data: []) -> str:
    lines = get_python_templates(data)
    code = [f"stream = {lines[0]}"]
    for cond in lines[1:]:
        code.append(f"stream = filter(lambda x: {cond}, stream)")
    body = '\n\t'.join(code)
    return f"def code():\n\t{body}\n\treturn list(stream)"


# -------------------------------------------------------
# Kotlin
# -------------------------------------------------------

get_kotlin_templates = get_templates(lambda x: f"!({x})")


def kotlin_range_template(body: [str]) -> str:
    a = int(body[0])
    b = int(body[1])
    if a > b:
        return f"({a} downTo {b})"
    else:
        return f"({a}..{b})"


def kotlin_program_template(data: []) -> str:
    lines = get_kotlin_templates(data)
    if len(lines) == 1:
        return f"{lines[0]}.toList()"
    code = [f"{lines[0]}.asSequence()"]
    for cond in lines[1:]:
        code.append(f"\t.filter {{ {cond} }}")
    body = '\n\t'.join(code)
    return f"fun code() =\n\t{body}\n\t\t.toList()"


# -------------------------------------------------------
# Elm
# -------------------------------------------------------

get_elm_templates = get_templates(lambda x: f"not <| {x}")


def elm_range_template(body: [str]) -> str:
    a = int(body[0])
    b = int(body[1])
    return f"List.range {a} {b}"


def elm_program_template(data: []) -> str:
    lines = get_elm_templates(data)
    code = [lines[0]]
    for cond in lines[1:]:
        code.append(f"\t|> List.filter (\\x -> {cond})")
    body = '\n\t'.join(code)
    return f"code : List Int\ncode = {body}"
