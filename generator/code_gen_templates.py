from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from generator.ccg import parse_to_node
from generator.code_gen import *

_code_gen_base_templates = [
    CodeTemplate(key='neg', template=negation_template)
]

_code_gen_python_base_templates = _code_gen_base_templates + [
    CodeTemplate(key='list', template=python_range_template),
    CodeTemplate(key='even', template=condition_template('x % 2 == 0')),
    CodeTemplate(key='odd', template=condition_template('x % 2 == 1')),
    CodeTemplate(key='bigger', template=condition_template('x > {0}', 1)),
]

code_gen_python_inline_templates = _code_gen_python_base_templates + [
    CodeTemplate(key='program', template=python_inline_program_template)
]

code_gen_python_functional_templates = _code_gen_python_base_templates + [
    CodeTemplate(key='program', template=python_functional_program_template)
]

code_gen_java_templates = _code_gen_base_templates + [
    CodeTemplate(key='list', template=java_range_template,
                 imports={'import java.util.stream.Collectors;', 'import java.util.stream.IntStream;',
                          'import java.util.List;'}),
    CodeTemplate(key='even', template=condition_template('x % 2 == 0')),
    CodeTemplate(key='odd', template=condition_template('x % 2 == 1')),
    CodeTemplate(key='bigger', template=condition_template('x > {0}', 1)),
    CodeTemplate(key='program', template=java_program_template),
]

code_gen_kotlin_templates = _code_gen_base_templates + [
    CodeTemplate(key='list', template=kotlin_range_template),
    CodeTemplate(key='even', template=condition_template('it % 2 == 0')),
    CodeTemplate(key='odd', template=condition_template('it % 2 == 1')),
    CodeTemplate(key='bigger', template=condition_template('it > {0}', 1)),
    CodeTemplate(key='program', template=kotlin_program_template),
]

code_gen_elm_templates = _code_gen_base_templates + [
    CodeTemplate(key='list', template=elm_range_template),
    CodeTemplate(key='even', template=condition_template('modBy x 2 == 0')),
    CodeTemplate(key='odd', template=condition_template('modBy x 2 == 1')),
    CodeTemplate(key='bigger', template=condition_template('x > {0}', 1)),
    CodeTemplate(key='program', template=elm_program_template),
]


def test(templates: [CodeTemplate], sentence: str):
    generator = CodeGenLanguage.from_templates('test', templates)
    node = parse_to_node(sentence)
    code = generator.generate_from_node(node)
    print(code)

# test(code_gen_python_inline_templates, "create even list from 0 to 100 bigger 5")
