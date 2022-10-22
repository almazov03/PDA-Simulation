import grammar as gr

from lexer import tokens
import ply.yacc as yacc

from GNF import *

import sys


def p_Start(p):
    "Start : START Rules"
    p[0] = gr.create_grammar(gr.NonTerminal(p[1]), p[2])


def p_Rules(p):
    ''' Rules : Rule
              | Rule Rules
    '''
    p[0] = [p[1]] + (p[2] if len(p) == 3 else [])


def p_Rule(p):
    'Rule : NON_TERMINAL EQUAL LBR Expr RBR'
    p[0] = gr.Rule(gr.NonTerminal(p[1]), p[4])


def p_Expr(p):
    ''' Expr : Term
             | Term Expr
    '''
    p[0] = [p[1]] + (p[2] if len(p) == 3 else [])


def p_Term_terminal(p):
    'Term : TERMINAL'
    p[0] = gr.Terminal(p[1])


def p_Term_non_terminal(p):
    'Term : NON_TERMINAL'
    p[0] = gr.NonTerminal(p[1])


def p_Term_Empty(p):
    'Term : EMPTY'
    p[0] = gr.Empty()


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
        grammar = parser.parse(' '.join(cin.readlines()))

        make_GNF(grammar)

        print(grammar)


if __name__ == "__main__":
    main()
