from typing import List, Union
from dataclasses import dataclass


@dataclass
class Terminal:
    value: str

    def print(self):
        return f'`{self.value}`'

    def __str__(self):
        return f'"{self.value}"'


@dataclass
class NonTerminal:
    value: str

    def print(self):
        return f'[{self.value}]'

    def __str__(self):
        return f'${self.value}$'


@dataclass
class Empty:

    def print(self):
        return 'EPS'

    def __str__(self):
        return 'EPS'


Term = Union[Terminal, NonTerminal, Empty]


@dataclass
class Rule:
    name: NonTerminal
    values: List[Term]

    def print(self):
        result = f'{self.name.print()} ='
        for term in self.values:
            result += ' ' + term.print()
        return result + ";\n"

    def __str__(self):
        result = f'{str(self.name)} = {{ '
        for term in self.values:
            result += str(term) + ' '
        return result + "}\n"


@dataclass
class Grammar:
    terminals: List[Terminal]
    non_terminals: List[NonTerminal]
    start: NonTerminal
    rules: List[Rule]

    def print(self):
        result = f"start={self.start.print()}\n"
        for rule in self.rules:
            result += rule.print()
        return result

    def __str__(self):
        result = f"STARTING_NON_TERMINAL={str(self.start)}\n"
        for rule in self.rules:
            result += str(rule)
        return result


def create_grammar(start: NonTerminal, rules: List[Rule]) -> Grammar:
    terminals, non_terminals = set(), set()
    for rule in rules:
        for term in rule.values:
            if isinstance(term, Terminal):
                terminals.add(str(term))
            if isinstance(term, NonTerminal) and term != start:
                non_terminals.add(str(term))

    terminals_list, non_terminals_list = [], []
    for term in terminals:
        terminals_list += [Terminal(term[1:-1])]
    for term in non_terminals:
        non_terminals_list += [NonTerminal(term[1:-1])]

    non_terminals_list = [start] + non_terminals_list

    return Grammar(terminals_list, non_terminals_list, start, rules)
