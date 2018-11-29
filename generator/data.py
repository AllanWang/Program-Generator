from typing import Callable, List
from dill.source import getsource
from dataclasses import dataclass
from pprintpp import pprint


@dataclass
class ConverterData:
    desc: [str]
    code: [str]

    def execute(self):
        exec('\n'.join(self.code))

def read_data():
    with open('../static/data.txt') as fp:
        data = []
        desc = []
        code = []
        flag = 'desc'
        for line in fp.readlines():
            line = line.strip()
            if line == '.':
                flag = 'code'
            elif line == '..':
                flag = 'desc'
                data.append(ConverterData(desc, code))
                desc = []
                code = []
            elif flag == 'desc':
                desc.append(line)
            elif flag == 'code':
                code.append(line)
        return data


pprint(read_data())

for d in read_data():
    print(d.execute())
