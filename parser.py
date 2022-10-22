from typing import List, Set, Union
from dataclasses import dataclass

from lexer import tokens
import ply.yacc as yacc

import sys


@dataclass
class Terminal:
    value: str

    def __str__(self):
        return f'"{self.value}"'

@dataclass
class NonTerminal:
    value: str

    def __str__(self):
        return f'${self.value}$'


@dataclass
class Empty:
    def __str__(self):
        return 'EPS'


Term = Union[Terminal, NonTerminal, Empty]


@dataclass
class Expr:
    values: List[Term]

    def __str__(self):
        result = ""
        for term in self.values:
            result += ' ' + str(term)
        return result


@dataclass
class Rule:
    name: str
    expr: Expr

    def __str__(self):
        return f'${self.name}$ = {{{str(self.expr)} }}\n'


@dataclass
class Grammar:
    terminals: Set[str]
    non_terminals: Set[str]
    start: str
    rules: List[Rule]

    def __str__(self):
        result = f"STARTING_NON_TERMINAL=${self.start}$\n"
        for rule in self.rules:
            result += str(rule)
        return result


def create_grammar(start: str, rules: List[Rule]) -> Grammar:
    terminals, non_terminals = set(), set()
    for rule in rules:
        for term in rule.expr.values:
            if isinstance(term, Terminal):
                terminals.add(str(term))
            else:
                non_terminals.add(str(term))

    return Grammar(terminals, non_terminals, start, rules)


def p_Start(p):
    "Start : START Rules"
    p[0] = create_grammar(p[1], p[2])


def p_Rules(p):
    ''' Rules : Rule
              | Rule Rules
    '''
    p[0] = [p[1]] + (p[2] if len(p) == 3 else [])


def p_Rule(p):
    'Rule : NON_TERMINAL EQUAL LBR Expr RBR'
    p[0] = Rule(p[1], p[4])


def p_Expr(p):
    ''' Expr : Term
             | Term Expr
    '''
    p[0] = Expr([p[1]] + (p[2].values if len(p) == 3 else []))


def p_Term_terminal(p):
    'Term : TERMINAL'
    p[0] = Terminal(p[1])


def p_Term_non_terminal(p):
    'Term : NON_TERMINAL'
    p[0] = NonTerminal(p[1])


def p_Term_Empty(p):
    'Term : EMPTY'
    p[0] = Empty()


def p_error(p):
    if p is None:
        token = "end of file"
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"

    print(f"Syntax error: Unexpected {token}")


parser = yacc.yacc()


def main():
    if len(sys.argv) != 2:
        print(f"Error. Expected 1, received {len(sys.argv) - 1}")
        exit(1)

    file_name = sys.argv[1]
    sys.stdout = open(file_name + '.parser.out', 'w')

    with open(file_name, 'r') as cin:
        result = parser.parse(' '.join(cin.readlines()))
        print(result)


if __name__ == "__main__":
    main()
