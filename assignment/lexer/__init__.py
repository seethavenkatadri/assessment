from sly import Lexer
import re

class MyLexer(Lexer):
    # Set of token names
    tokens = { WORD, NUMBER,                            ## words
               ASSIGN, COMPARE, AND, PLUS, PERCENT,     ## operators
               LET, IF, THEN, FI,                       ## reserved words
               PRINT, DATE, SCRPTARG,                    ## commands
               DQUOTE, VALUEOF,  QMARK, SCOLON,  ## literals
               LPAREN, RPAREN, LSQUARE, RSQUARE, BTICK}

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

    @_(r'echo(.)+')
    def PRINT(self,t):
        t.value= re.sub('"','',re.sub('echo ','',t.value))
        return t

    # Regular expression rules for tokens
    WORD = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Special cases
    WORD['if'] = IF
    WORD['then'] = THEN
    WORD['fi'] = FI

    #WORD['echo'] = ECHO
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
    #LCURLY = r'{'
    #RCURLY = r'}'
    LSQUARE = r'\['
    RSQUARE = r'\]'
    #COLON = r':'
    SCOLON = r';'
    VALUEOF = r'\$'
    QMARK = r'\?'
    BTICK = r'`'
    PLUS = r'\+'
    PERCENT = r'%'

    SCRPTARG= r'\.\./(.)+'







if __name__ == '__main__':
    data = """# comment
               let \
             \
                \
            X=1 ; if [[ ( "some" == "imaging" ) && ( "some" == "some" ) ]]; then
            # comment
                  I_S_T=`date +%25s`
                  echo "FOR I_S_T is ${I_S_T}"
                  echo Executing Imaging script: I_V_P=1 I_D_T= O_B=1 ../build/c.f/gi i/f/f_t_c.d
                  I_V_P=1 I_D_T= F_P_V=1 O_B=1 ../build/c.f/gi i/f/f_t_c.d
                  RET_VAL=$?
                  I_E_T=`date +%25s`
                  fi"""

    lexer = MyLexer()

    for tok in lexer.tokenize(data):
        print(tok)