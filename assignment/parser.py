from sly import Parser
import pprint
from cisco.assignment.lexer import MyLexer


class MyParser(Parser):
    # Get the token list from the lexer
    tokens = MyLexer.tokens
    debugfile = 'parser.out'

# statements : statements statement #
#         | statement #
# statement : command #
#         | assignments #
#         | IF conditional THEN statements FI #
# words : words WORD #
#         | words SCRPTARG #
#         | words COLON  #
#         | words VALUEOF LCURLY WORD RCURLY  #
#         | WORD #
# command : ECHO DQUOTE words DQUOTE #
#         | ECHO words #
#         | ECHO command #
#         | assignments SCRPTARG  #
#         | DATE format   #
# format : PLUS PERCENT NUMBER WORD #
# assignment :  WORD ASSIGN NUMBER #
#         | assignment SCOLON #
#         | WORD ASSIGN BTICK command BTICK #
#         | WORD ASSIGN VALUEOF QMARK #
#         | LET assignment
# assignments : assignments assignment #
#         | assignment #
# conditional : LSQUARE LSQUARE comparison AND comparison RSQUARE RSQUARE SCOLON #
# quoted : DQUOTE WORD DQUOTE #
# comparison : LPAREN quoted COMPARE quoted RPAREN #

    @_('statements')
    def program(self,p):
        print('statements --> program')
        return dict(start=p[0])
    @_('statements statement')
    def statements(self, p):
        print('statements statement --> statements')
        return (p[0],p[1])

    @_('statement')
    def statements(self, p):
        print('statement --> statements')
        return (p[0])

    @_('command')
    def statement(self, p):
        print('command --> statement')
        return (p[0])

    @_('WORD')
    def words(self, p):
        print('WORD --> words')
        return (p[0])

    @_('PRINT')
    def statement(self, p):
        print('PRINT --> statement --',p[0])
        return dict(print=p[0])

    @_('IF conditional THEN statements FI')
    def statement(self, p):
        print('IF conditional THEN statements FI --> statement')
        return dict(checkif=p[1],execute=p[3])

    @_('assignment')
    def statement(self, p):
        print('assignment --> statement')
        return (p[0])

    @_('LET statement')
    def statement(self, p):
        print('LET statement --> statement')
        return (p[1])

    @_('DATE format')
    def command(self, p):
        print('DATE format --> command')
        return dict(etime=p[0],format=p[1])

    @_('assignments SCRPTARG')
    def command(self, p):
        print('assignments SCRPTARG --> command')
        return ('set values before execute', p[0], 'execute with args', p[1])

    @_('assignment')
    def assignments(self, p):
        print('assignment --> assignments')
        return (p[0])

    @_('assignment NUMBER')
    def assignment(self, p):
        print('assignment NUMBER --> assignment')
        return ('assign', p[0] , p[1])

    @_('WORD ASSIGN')
    def assignment(self, p):
        print('WORD ASSIGN --> assignment')
        return dict(assign=p[0])

    @_('assignment BTICK command BTICK')
    def assignment(self, p):
        print('assignment BTICK command BTICK --> assignment')
        return ('assign', p[0], p[2])

    @_('assignment VALUEOF QMARK')
    def assignment(self, p):
        print('assignment VALUEOF QMARK --> assignment')
        return ('assign', p[0], 'execution code')

    @_('assignment SCOLON')
    def assignment(self, p):
        print('assignment SCOLON --> assignment')
        return (p[0])

    @_('LSQUARE LSQUARE comparison AND comparison RSQUARE RSQUARE SCOLON')
    def conditional(self, p):
        print('LSQUARE LSQUARE comparison AND comparison RSQUARE RSQUARE SCOLON --> conditional')
        return ('and',p[2],p[4])

    @_('DQUOTE words DQUOTE')
    def quoted(self, p):
        print('DQUOTE words DQUOTE --> quoted')
        return str(p[1])

    @_('LPAREN quoted COMPARE quoted RPAREN')
    def comparison(self,p):
        print('LPAREN quoted COMPARE quoted RPAREN --> comparison')
        return dict(compare=(p[1],p[3]))

    @_('PLUS PERCENT NUMBER WORD')
    def format(self,p):
        print('PLUS PERCENT NUMBER WORD --> format')
        if p[3] == 's':
            return ('in seconds')

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
    parser = MyParser()

    result = parser.parse(lexer.tokenize(data))
    pprint.pprint(result,width=2)