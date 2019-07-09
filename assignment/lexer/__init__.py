from sly import Lexer

class MyLexer(Lexer):
    # Set of token names
    tokens = { WORD, NUMBER,                            ## words
               ASSIGN, COMPARE, AND, PLUS, PERCENT,     ## operators
               LET, IF, THEN, FI,                       ## reserved words
               ECHO, DATE, SCRPTARG,                    ## commands
               DQUOTE, VALUEOF,  QMARK, COLON, SCOLON,  ## literals
               LPAREN, RPAREN, LCURLY, RCURLY, LSQUARE, RSQUARE, BTICK}

    # String containing ignored characters between tokens
    ignore = ' \t'  # spaces

    # Ignore comments but track line number
    @_(r'\#.*')
    def ignore_comment(self, t):
        self.lineno += t.value.count('\n')

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    @_(r'\\\n+')
    def ignore_bslashnewline(self, t):
        self.lineno += t.value.count('\n')
    # Regular expression rules for tokens
    WORD = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Special cases
    WORD['if'] = IF
    WORD['then'] = THEN
    WORD['fi'] = FI
    WORD['echo'] = ECHO
    WORD['date'] = DATE
    WORD['let'] = LET
    NUMBER  = r'\d+'

    COMPARE = r'=='
    ASSIGN  = r'='
    AND = r'&&'

    DQUOTE = r'"'
   # BSLASH = r'\\'
    LPAREN = r'\('
    RPAREN = r'\)'
    LCURLY = r'{'
    RCURLY = r'}'
    LSQUARE = r'\['
    RSQUARE = r'\]'
    COLON = r':'
    SCOLON = r';'
    VALUEOF = r'\$'
    QMARK = r'\?'
    BTICK = r'`'
    PLUS = r'\+'
    PERCENT = r'%'

    SCRPTARG= r'\.\./(.)+'




if __name__ == '__main__':

    lexer = MyLexer()