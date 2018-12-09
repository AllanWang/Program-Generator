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
        print(data, argc)
        base = _data_to_list(data[argc])
        base.append(cond)
        return base

    return callable


def negation_template(data: []) -> []:
    cond: ConditionTemplate = data[0][-1]
    cond.negate = not cond.negate
    return data[0]


def _data_to_list(data) -> [Any]:
    if isinstance(data, list):
        return data
    if isinstance(data, str):
        return [data]
    raise ValueError("Expected string or list")


def _get_templates(negate_condition: Callable[[str], str]) -> CallableTemplate:
    def converter(template: Union[str, ConditionTemplate]) -> str:
        if isinstance(template, str):
            return template
        if isinstance(template, ConditionTemplate):
            if template.negate:
                return negate_condition(template.template)
            return template.template

    def callable(data) -> [str]:
        return [converter(d) for d in _data_to_list(data[0])]

    return callable


_get_python_templates = _get_templates(lambda x: f"not {x}")


def python_inline_program_template(data: []) -> str:
    print(data)
    lines = _get_python_templates(data)
    code = f"(x for x in {lines[0]})"
    for cond in lines[1:]:
        code = f"(x for x in {code} if {cond})"
    return f"def code():\n\treturn list({code})"


def python_functional_program_template(data: []) -> str:
    lines = _get_python_templates(data)
    code = [f"stream = {lines[0]}"]
    for cond in lines[1:]:
        code.append(f"stream = filter(lambda x: {cond}, stream)")
    body = '\n\t'.join(code)
    return f"def code():\n\t{body}\n\treturn list(stream)"


code_gen_base_templates = [
    CodeTemplate(key='neg', template=negation_template)
]

code_gen_python_base_templates = code_gen_base_templates + [
    CodeTemplate(key='list', template=python_range_template),
    CodeTemplate(key='even', template=condition_template('x % 2 == 0')),
    CodeTemplate(key='odd', template=condition_template('x % 2 == 1')),
    CodeTemplate(key='bigger', template=condition_template('x > {0}', 1)),
]

code_gen_python_inline_templates = code_gen_python_base_templates + [
    CodeTemplate(key='program', template=python_inline_program_template)
]

code_gen_python_functional_templates = code_gen_python_base_templates + [
    CodeTemplate(key='program', template=python_functional_program_template)
]


def kotlin_range_wrap(wrapper: str) -> CallableTemplate:
    def wrapper_template(body: [str]):
        a = int(body[0])
        b = int(body[1])
        if a > b:
            return wrapper.format(f"({a} downTo {b})")
        else:
            return wrapper.format(f"({a}..{b})")

    return wrapper_template


def kotlin_wrap(body: [str]) -> str:
    code = '\n\t\t'.join(b for b in body[0].split('\n') if b)
    if code.endswith('.asSequence()'):
        code = code.rpartition('.asSequence()')[0]
    return f"fun code() =\n\t{code}.toList()"


code_gen_kotlin = CodeGenLanguage.from_templates('kotlin', [
    CodeTemplate(key='list', template=kotlin_range_wrap('{0}.asSequence()')),
    CodeTemplate(key='even', template='{0}\n.filter {{ it % 2 == 0 }}'),
    CodeTemplate(key='odd', template='{0}\n.filter {{ it % 2 == 1 }}'),
    CodeTemplate(key='bigger', template='{1}\n.filter {{ it > {0} }}'),
    CodeTemplate(key='program', template=kotlin_wrap),
])


def test(templates: [CodeTemplate], sentence: str):
    generator = CodeGenLanguage.from_templates('test', templates)
    node = parse_to_node(sentence)
    code = generator.generate_from_node(node)
    print(code)


test(code_gen_python_inline_templates, "create even list from 0 to 100 bigger 5")
