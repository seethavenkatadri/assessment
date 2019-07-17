from sly import Lexer
import re

class MyLexer(Lexer):
    # Set of token names
    tokens = { IDENTIFIER, NUMBER,                            ## words
               ASSIGN, COMPARE, AND,                    ## operators
               LET, IF, THEN, ELSE, FI,                       ## reserved words
               ECHOLINE, DATE, FORMAT, SCRPTARG,                    ## commands
               STRING , VALUEOF,  QMARK, SCOLON,  ## literals
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
    def ECHOLINE(self,t):
        t.value= re.sub('"','',re.sub('echo ','',t.value))
        return t

    # Regular expression rules for tokens
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Special cases
    IDENTIFIER['if'] = IF
    IDENTIFIER['then'] = THEN
    IDENTIFIER['else'] = ELSE
    IDENTIFIER['fi'] = FI

    IDENTIFIER['date'] = DATE
    IDENTIFIER['let'] = LET
    NUMBER  = r'\d+'

    COMPARE = r'=='
    ASSIGN  = r'='
    AND = r'&&'

    LPAREN = r'\('
    RPAREN = r'\)'
    LSQUARE = r'\['
    RSQUARE = r'\]'
    SCOLON = r';'
    VALUEOF = r'\$'
    QMARK = r'\?'
    BTICK = r'`'

    FORMAT = r'\+%[0-9][0-9][a-z]'
    STRING = r'[\'"][a-zA-Z_][a-zA-Z0-9_]*[\'"]'
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
                  fi
                  """
    lexer = MyLexer()
    for tok in lexer.tokenize(data):
        print(tok)