from sly import Parser

from cisco.assignment.lexer import MyLexer


class MyParser(Parser):
    # Get the token list from the lexer
    tokens = MyLexer.tokens

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
#         | assignments SCRPTARG #
#         | DATE format   #
# format : PLUS PERCENT WORD #
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
        print('call 1 \n')
        return p[0]
    @_('statements statement')
    def statements(self, p):
        print('call 2 \n')
        return (p[0],p[1])

    @_('statement')
    def statements(self, p):
        print('call 3 \n')
        return (p[0])

    @_('command')
    def statement(self, p):
        print('call 4 \n')
        return (p[0])

    @_('conditional')
    def statement(self, p):
        print('call 4.1 \n')
        return (p[0])

    @_('IF statement THEN statements FI')
    def statement(self, p):
        print('call 5 \n')
        return ('check',p[1],'then execute',p[3])

    @_('assignments')
    def statement(self, p):
        print('call 6 \n')
        return (p[0])

    @_('ECHO DQUOTE words DQUOTE')
    def command(self, p):
        print('call 7 \n')
        return ('print',p[2])

    @_('ECHO words')
    def command(self, p):
        print('call 8 \n')
        return ('print', p[1])

    @_('assignments SCRPTARG')
    def command(self, p):
        print('call 9 \n')
        return ('set values before execute',p[0], 'execute with args', p[1])

    @_('DATE format')
    def command(self, p):
        print('call 10 \n')
        return ('execution time', p[0])

    @_('WORD')
    def words(self, p):
        print('call 11 \n')
        return (p[0])

    @_('words WORD')
    def words(self, p):
        print('call 12 \n')
        return (p[0] , p[1])

    @_('words SCRPTARG')
    def words(self, p):
        print('call 13 \n')
        return (p[0] , p[1])

    @_('words COLON')
    def words(self, p):
        print('call 14 \n')
        return (p[0] , p[1])

    @_('words VALUEOF LCURLY WORD RCURLY')
    def words(self, p):
        print('call 15 \n')
        return (p[0] , p[3])

    @_('assignments assignment')
    def assignments(self, p):
        print('call 16 \n')
        return (p[0] , p[1])

    @_('assignment')
    def assignments(self, p):
        print('call 17 \n')
        return (p[0])

    @_('WORD ASSIGN NUMBER')
    def assignment(self, p):
        print('call 18 \n')
        return ('assign', p[0] , p[2])

    @_('WORD ASSIGN BTICK command BTICK')
    def assignment(self, p):
        print('call 19 \n')
        return ('assign', p[0], p[2])

    @_('WORD ASSIGN VALUEOF QMARK')
    def assignment(self, p):
        print('call 20 \n')
        return ('assign', p[0], 'execution code')

    @_('assignment SCOLON')
    def assignment(self, p):
        print('call 21 \n')
        return (p[0])

    @_('LET WORD ASSIGN NUMBER SCOLON')
    def assignment(self, p):
        print('call 22 \n')
        return ('assign',p[1],p[3])

    @_('LSQUARE LSQUARE comparison AND comparison RSQUARE RSQUARE SCOLON')
    def conditional(self, p):
        print('call 23 \n')
        return ('and',p[2],p[4])

    @_('DQUOTE WORD DQUOTE')
    def quoted(self, p):
        print('call 24 \n')
        return (p[1])

    @_('LPAREN quoted COMPARE quoted RPAREN')
    def comparison(self,p):
        print('call 25 \n')
        return ('is equal to',p[1],p[3])

    @_('PLUS PERCENT WORD')
    def format(self,p):
        print('call 26 \n')
        if p[2] == 's':
            return ('in seconds since 1970-01-01 00:00:00 UTC')

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
    print(result or 'Nothing to print')