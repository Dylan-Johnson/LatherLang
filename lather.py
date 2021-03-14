from sly import Lexer
from sly import Parser

################################################################################
#    LEXER
################################################################################
from sly import Lexer

class CalcLexer(Lexer):
    # Set of token names.   This is always required
    tokens = { STRING, NUMBER, CAT,
               PLUS, MINUS, TIMES, DIVIDE,
               EQ, LT, LE, GT, GE, NE, LATHER }


    literals = { '(', ')', '{', '}', ';' }

    # String containing ignored characters
    ignore = ' \t'

    # Regular expression rules for tokens
    CAT     = r'~'
    PLUS    = r'\+'
    MINUS   = r'--'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    EQ      = r'=='
    LE      = r'<='
    LT      = r'<'
    GE      = r'>='
    GT      = r'>'
    NE      = r'!='

    STRING = r'\".*?\"'
    #@_(r'\".*?\"')
    #def STRING(self, t):
    #    return (t.value)[1:-1]

    @_(r'[+-]?([0-9]*[.])?[0-9]+')
    def NUMBER(self, t):
        t.value = float(t.value)
        return t

    # Identifiers and keywords
    #ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    #ID['lather'] = LATHER
    LATHER = 'lather'

    ignore_comment = r'\#.*'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1
################################################################################
#    PARSER
################################################################################
from sly import Parser
#from calclex import CalcLexer

class CalcParser(Parser):
    # Get the token list from the lexer (required)
    tokens = CalcLexer.tokens

    #Split text and numbers between 'expr' and 'term'

    # Grammar rules and actions

    @_('str CAT string')
    def expr(self, p):
        return p.str + p.string

    @_('term PLUS factor')
    def term(self, p):
        return p.term + p.factor

    #[Works with no errors]
    @_('term MINUS factor')
    def term(self, p):
        return p.term - p.factor

    @_('term TIMES factor')
    def term(self, p):
        return p.term * p.factor

    @_('term DIVIDE factor')
    def term(self, p):
        return p.term / p.factor

    ###############################
    @_('term GE factor')
    def term(self, p):
        return p.term >= p.factor

    @_('term LE factor')
    def term(self, p):
        return p.term <= p.factor

    @_('term NE factor')
    def term(self, p):
        return p.term != p.factor

    @_('term GT factor')
    def term(self, p):
        return p.term > p.factor

    @_('term LT factor')
    def term(self, p):
        return p.term < p.factor

    @_('term EQ factor')
    def term(self, p):
        return p.term == p.factor

    ###############################

    @_('term')
    def expr(self, p):
        return p.term

    @_('factor')
    def term(self, p):
        return p.factor

    @_('NUMBER')
    def factor(self, p):
        return p.NUMBER

    @_('str')
    def expr(self,p):
        return p.str

    @_('string')
    def str(self, p):
        return p.string

    @_('STRING')
    def string(self, p):
        #Cuts the quotation marks from the initial string
        return (p.STRING)[1:-1]

    @_('line')
    def expr(self, p):
        return p.line

    @_('LATHER')
    def line(self, p):
        return ('          ___       ___  __  \n|     /\   |  |__| |__  |__) \n|___ /~~\  |  |  | |___ |  \ \n LAnguage THeory End Result \n\nDeveloped by Dylan Johnson, Richard Tran, and Tanner Tran')

    @_('')
    def line(self, p):
        pass

################################################################################
#    MAIN
################################################################################
if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()

    print("Lather Language: Development Version")

    while True:
        try:
            text = input('LatherLang > ')
            result = parser.parse(lexer.tokenize(text))
            print(result)
        except EOFError:
            break
