# -----------------------------------------------------------------------------
# calc.py
# -----------------------------------------------------------------------------

from sly import Lexer, Parser
import sys

class CalcLexer(Lexer):
    tokens = { ID, NUMBER, STRING }
    ignore = ' \t'
    literals = { '=', '+', '-', '*', '/', '(', ')', '~' }

    # Tokens
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    @_(r'\".*?\"')
    def STRING(self, t):
        return t

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
        )

    def __init__(self):
        self.names = { }

    @_('ID "=" expr')
    def statement(self, p):
        self.names[p.ID] = p.expr

    @_('expr "~" expr')
    def expr(self, p):
        return str(p.expr0) + str(p.expr1)

    @_('expr "+" expr')
    def expr(self, p):
        try:
            return p.expr0 + p.expr1
        except TypeError:
            print("Error: Type mismatch between",p.expr0,"and",p.expr1)
            return 0

    @_('expr "-" expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr "*" expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr "/" expr')
    def expr(self, p):
        try:
            return p.expr0 / p.expr1
        except TypeError:
            print("Error: Type mismatch between", p.expr0, "and", p.expr1)
            return 0

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

    @_('ID')
    def expr(self, p):
        try:
            return self.names[p.ID]
        except LookupError:
            print("Undefined name '%s'" % p.ID)
            return 0

    ##############################################
    @_('STRING')
    def expr(self, p):
        return p.STRING[1:-1]


if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    if (len(sys.argv) > 1):
        with open(sys.argv[1]) as topo_file:
            for line in topo_file:
                parser.parse(lexer.tokenize(line))
    else:
        print("  __      __   ____  _   _  ____  ____ ")
        print(" (  )    /__\ (_  _)( )_( )( ___)(  _ \ ")
        print("  )(__  /(__)\  )(   ) _ (  )__)  )   /")
        print(" (____)(__)(__)(__) (_) (_)(____)(_)\_)")
        print("      'LAnguage THeory End Result'      ")
        print("Dylan Johnson, Tanner Tran, Richard Tran")
        while True:
           try:
               text = input('calc > ')
           except EOFError:
               break
           if text:
               parser.parse(lexer.tokenize(text))

