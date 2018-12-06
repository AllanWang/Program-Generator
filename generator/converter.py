# -*- coding: utf-8 -*-

sentence = "create even list from 10 to 100 that is bigger than 5"
#parsed = 'program(even(bigger(5,list(R(10,100)))))'

from generator.ccg import parse
from nltk.ccg import chart, lexicon, CCGLexicon
from nltk.tree import Tree
import re

derivation = []

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def myCCGTree(lwidth, tree):
    rwidth = lwidth
    
    # Is a leaf (word).
    # Increment the span by the space occupied by the leaf.
    if not isinstance(tree, Tree):
        return 2 + lwidth + len(tree)

    # Find the width of the current derivation step
    for child in tree:
        rwidth = max(rwidth, myCCGTree(rwidth, child))

    # Is a leaf node.
    # Don't print anything, but account for the space occupied.
    if not isinstance(tree.label(), tuple):
        return max(
            rwidth, 2 + lwidth + len("%s" % tree.label()), 2 + lwidth + len(tree[0])
        )

    (token, op) = tree.label()
    #print(token.semantics())
    if op == 'Leaf':
        return rwidth

    # Pad to the left with spaces, followed by a sequence of '-'
    # and the derivation rule.
    #print(lwidth * ' ' + (rwidth - lwidth) * '-' + "%s" % op)
    # Print the resulting category on a new line.
    #str_res = "%s" % (token.categ())
    str_res = ""
    if token.semantics() is not None:
        str_res += " {" + str(token.semantics()) + "}"
    respadlen = (rwidth - lwidth - len(str_res)) // 2 + lwidth
    if "\\" not in str_res: 
        #print(str_res)
        clean = re.sub(r'\s+','',str_res.replace("{","").replace("}",""))
        if not is_number(clean):
            derivation.append(re.sub(r'\s+','',str_res.replace("{","").replace("}","")))
        
    return rwidth

def process():
    
    range_str = derivation[0]
    lb = range_str.find('(')
    rb = range_str.find(')')
    operator = range_str[0:lb] + '()'
    arg1, arg2 = range_str[lb + 1: rb].split(',')
    stack_execution = [(operator, arg1, arg2)]
    
    for i in range(len(derivation) - 1):
        new = derivation[i + 1].replace(derivation[i], '').replace(',', '')
        
        lb = new.find('(')
        rb = new.find(')')
    
        if rb - lb > 1:
            operator = new[0:lb] + '()'
            arg = new[lb + 1: rb]
            stack_execution.append((operator, arg))
            continue
        
        stack_execution.append(new)
        
    return stack_execution
    
def generate_python(stack_execution):
    
    declare = ''
    creation = ''
    condition = ''
    for i in range(len(stack_execution)): 
        
        elem = stack_execution[i]
        
        if type(elem) == tuple:
            
            op = elem[0]
            args = list(elem[1:])
            
            if op == 'R()':
                declare = 'min_var, max_var = ' + args[0] + ', ' + args[1] + '\n'
            elif op == 'bigger()':
                if not condition:
                    condition = condition + ' x > ' + args[0]
                else:
                    condition = condition + ' and x > ' + args[0]
            
        else:
            if elem == 'list()':
                creation = '[x for x in range(min_var, max_var)]'
            elif elem == 'even()':
                if not condition:
                    condition = condition + ' x % 2 == 0'  
                else:
                    condition = condition + ' and x % 2 == 0'  
    
    if not condition:
        return declare + creation
    else:
        return declare + '[for x in ' + creation + ' if ' + condition + ']'
    
result = parse(sentence)
myCCGTree(0, result)
ccg_input = derivation[-1]
del derivation[-1]
stack_execution = process()
print('Execution stack: ' + str(stack_execution))
print('generated code............................')
print(generate_python(stack_execution))