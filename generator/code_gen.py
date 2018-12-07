from dataclasses import dataclass, field
from typing import Set, Dict, Union, Callable, List, Optional

from generator.node import Node

CallableTemplate = Callable[[List[str]], str]


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

    def _generate_from_node(self, node: Node, container: CodeGenHelper) -> str:
        code_template = self.get_template(node.value)
        container.lib_keys.update(code_template.lib_keys)
        child_templates = [self._generate_from_node(c, container) for c in node.children]
        if isinstance(code_template.template, str):
            return code_template.template.format(*child_templates)
        return code_template.template(child_templates)


def python_range_wrap(wrapper: str) -> CallableTemplate:
    def wrapper_template(body: [str]):
        a = int(body[0])
        b = int(body[1])
        if a > b:
            return wrapper.format(f"reversed(range({b}, {a}))")
        else:
            return wrapper.format(f"range({a}, {b})")

    return wrapper_template


code_gen_python_inline = CodeGenLanguage.from_templates('python_inline', [
    CodeTemplate(key='list', template=python_range_wrap('(x for x in {0})')),
    CodeTemplate(key='even', template='(x for x in {0} if x % 2 == 0)'),
    CodeTemplate(key='odd', template='(x for x in {0} if x % 2 == 1)'),
    CodeTemplate(key='bigger', template='(x for x in {1} if x > {0})'),
    CodeTemplate(key='program', template='def code():\n\treturn list{0}'),
])


def python_functional_wrap(body: [str]):
    code = '\n\t'.join(b for b in body[0].split('\n') if b)
    return f"def code():\n\t{code}\n\treturn list(stream)"


code_gen_python_functional = CodeGenLanguage.from_templates('python_functional', [
    CodeTemplate(key='list', template=python_range_wrap('stream = (x for x in {0})')),
    CodeTemplate(key='even', template='{0}\nstream = filter(lambda x: x % 2 == 0, stream)'),
    CodeTemplate(key='odd', template='{0}\nstream = filter(lambda x: x % 2 == 1, stream)'),
    CodeTemplate(key='bigger', template='{1}\nstream = filter(lambda x: x > {0}, stream)'),
    CodeTemplate(key='program', template=python_functional_wrap),
])
