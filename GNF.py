from grammar import *


def make_unique_rules(grammar):
    unique_rules = set()
    new_rules = []
    for rule in grammar.rules:
        if str(rule) in unique_rules:
            continue
        unique_rules.add(str(rule))
        new_rules += [rule]

    grammar.rules = new_rules


def is_eps_rule(rule):
    f = True
    for term in rule.values:
        if not isinstance(term, Empty):
            f = False
            break
    return f


def get_eps_non_terminals(grammar):
    eps_non_terminals = set()
    for rule in grammar.rules:
        if is_eps_rule(rule):
            eps_non_terminals.add(str(rule.name))

    f = True
    while f:
        f = False
        for rule in grammar.rules:
            if str(rule.name) in eps_non_terminals:
                continue
            for term in rule.values:
                if str(term) in eps_non_terminals:
                    eps_non_terminals.add(str(rule.name))
                    f = True
                    break
    return eps_non_terminals


def add_new_rules_without_eps(eps_non_terminals, rule: Rule, i, n, res: List[Term], new_rules: List[Rule]):
    if i == n:
        new_rule = Rule(rule.name, res)
        if not is_eps_rule(new_rule):
            new_rules += [new_rule]
        return

    if isinstance(rule.values[i], Empty):
        add_new_rules_without_eps(eps_non_terminals, rule, i + 1, n, res, new_rules)
        return

    if str(rule.values[i]) in eps_non_terminals:
        add_new_rules_without_eps(eps_non_terminals, rule, i + 1, n, res, new_rules)
    add_new_rules_without_eps(eps_non_terminals, rule, i + 1, n, res + [rule.values[i]], new_rules)


def remove_eps_rules(grammar):
    eps_non_terminals = get_eps_non_terminals(grammar)
    new_rules = []
    for rule in grammar.rules:
        add_new_rules_without_eps(eps_non_terminals, rule, 0, len(rule.values), [], new_rules)

    grammar.rules = new_rules
    if len(eps_non_terminals) > 0:
        last_start = grammar.start
        grammar.start = NonTerminal("START")

        grammar.rules = [Rule(grammar.start, [Empty()])] + grammar.rules
        grammar.rules = [Rule(grammar.start, [last_start])] + grammar.rules

        grammar.non_terminals = [grammar.start] + grammar.non_terminals


def remove_immediate_left_recursion(grammar, ind):
    non_term = grammar.non_terminals[ind]
    alpha, beta = [], []
    i = 0
    while i < len(grammar.rules):
        rule = grammar.rules[i]
        if rule.name != non_term:
            i += 1
            continue

        if rule.values[0] == non_term:
            alpha += [rule.values[1:]]
            grammar.rules.remove(rule)
            i -= 1
        else:
            beta += [rule.values]
        i += 1

    if len(alpha) == 0:
        return

    new_non_term = NonTerminal(str(non_term)[1:-1] + "'")

    for term in beta:
        grammar.rules += [Rule(non_term, term + [new_non_term])]

    grammar.non_terminals += [new_non_term]
    for term in alpha:
        grammar.rules += [Rule(new_non_term, term + [new_non_term])]
        grammar.rules += [Rule(new_non_term, term)]


def remove_left_recursion(grammar):
    n = len(grammar.non_terminals)
    for i in range(n):
        for j in range(i):
            ind = 0
            while ind < len(grammar.rules):
                rule = grammar.rules[ind]
                if rule.name != grammar.non_terminals[i] or rule.values[0] != grammar.non_terminals[j]:
                    ind += 1
                    continue

                ost = rule.values[1:]
                grammar.rules.remove(rule)

                for rule2 in grammar.rules:
                    if rule2.name != grammar.non_terminals[j]:
                        continue
                    grammar.rules += [Rule(grammar.non_terminals[i], rule2.values + ost)]

        remove_immediate_left_recursion(grammar, i)

    for i in range(len(grammar.non_terminals)):
        if str(grammar.non_terminals[i]).count("'"):
            tmp1 = grammar.non_terminals[i:]
            tmp2 = grammar.non_terminals[:i]
            grammar.non_terminals = tmp1 + tmp2
            break


def remove_all_terminal_in_right_part(grammar):
    n = len(grammar.rules)
    for j in range(n):
        rule = grammar.rules[j]
        new_rule = [rule.values[0]]
        for i in range(1, len(rule.values)):
            term = rule.values[i]
            if isinstance(term, Terminal):
                new_non_term = NonTerminal(str(term)[1:-1] + "'")
                grammar.rules += [Rule(new_non_term, [term])]
                new_rule += [new_non_term]
            else:
                new_rule += [term]
        grammar.rules[j] = Rule(rule.name, new_rule)


def make_GNF(grammar: Grammar):
    remove_eps_rules(grammar)
    remove_left_recursion(grammar)
    make_unique_rules(grammar)

    f = True
    while f:
        f = 0
        for i in range(len(grammar.non_terminals)):
            for j in range(i + 1, len(grammar.non_terminals)):

                rules_j = []
                for rule in grammar.rules:
                    if rule.name == grammar.non_terminals[j]:
                        rules_j += [rule.values]

                if len(rules_j) == 0:
                    continue

                ind = 0
                while ind < len(grammar.rules):
                    rule = grammar.rules[ind]
                    if rule.name != grammar.non_terminals[i] or rule.values[0] != grammar.non_terminals[j]:
                        ind += 1
                        continue

                    f = True
                    ost = rule.values[1:]
                    grammar.rules.remove(rule)

                    for rule2 in rules_j:
                        grammar.rules += [Rule(grammar.non_terminals[i], rule2 + ost)]
    remove_all_terminal_in_right_part(grammar)
    make_unique_rules(grammar)
