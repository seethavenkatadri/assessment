from sly import Parser
import pprint
from cisco.assignment.lexer import MyLexer


class MyParser(Parser):
    # Get the token list from the lexer
    tokens = MyLexer.tokens
    debugfile = 'parser.out'


# program : statements
# statements : statements statement
#		    | statement
# statement : ECHOLINE
#	        | IF conditionals THEN statements FI
#           | IF conditionals THEN statements ELSE statements FI
#	        | assignments
#	        | LET statement
#           | DATE format
#           | assignments SCRPTARG
# assignments:assignment
#           | assignments assignment
# assignment: assignment NUMBER
#		    | WORD assign
#		    | assignment BTICK statement BTICK
#		    | assignment VALUEOF QMARK
#		    | assignment SCOLON
# conditional : LSQUARE LSQUARE comparison AND comparison RSQUARE RSQUARE SCOLON
# comparison: LPAREN STRING COMPARE STRING RPAREN
# format : PLUS PERCENT NUMBER WORD







    @_('statements')
    def program(self,p):
        print('1..')
        return dict(operation='start',stlist=p[0])

    @_('statements statement')
    def statements(self, p):
        print('2..')
        templist=[]
        if isinstance(p[0],dict) and isinstance(p[1],dict):
            templist.append(p[0].copy())
            templist.append(p[1].copy())
            return templist
        elif isinstance(p[0],list) and isinstance(p[1],dict):
            templist=p[0]
            templist.append(p[1].copy())
            return templist
        elif isinstance(p[0],type(None)) and isinstance(p[1],dict):
            return p[1]
        elif isinstance(p[0],dict) and isinstance(p[1],type(None)):
            return p[0]

    @_('statement')
    def statements(self, p):
        print('3..')
        return p[0]

    @_('ECHOLINE')
    def statement(self, p):
        print('5..')
        return dict(operation='print',args=p[0])

    @_('IF conditional THEN statements FI')
    def statement(self, p):
        print('6..')
        return dict(operation='IF',condition=p[1],stlist=p[3])

    @_('IF conditional THEN statements ELSE statements FI')
    def statement(self, p):
        print('6.1..')
        return dict(operation='IF', condition=p[1], ifstlist=p[3],elsestlist=p[5])

    @_('assignments')
    def statement(self, p):
        print('7..')
        return p[0]

    @_('LET statement')
    def statement(self, p):
        print('8..')
        return p[1]

    @_('DATE format')
    def statement(self, p):
        print('9..')
        return dict(operation=p[0], format=p[1])

    @_('assignments SCRPTARG')
    def statement(self, p):
        print('10..')
        return dict(operation='exec',script=p[1])

    @_('assignment')
    def assignments(self, p):
        print('11..')
        return p[0]

    @_('assignments assignment')
    def assignments(self, p):
        print('11.1..')
        templist = []
        if isinstance(p[0], dict) and isinstance(p[1], dict):
            templist.append(p[0].copy())
            templist.append(p[1].copy())
            return templist
        elif isinstance(p[0], list) and isinstance(p[1], dict):
            templist = p[0]
            templist.append(p[1].copy())
            return templist
        elif isinstance(p[0], type(None)) and isinstance(p[1], dict):
            return p[1]
        elif isinstance(p[0], dict) and isinstance(p[1], type(None)):
            return p[0]

    @_('assignment NUMBER')
    def assignment(self, p):
        print('12..')
        p[0]['operands']['rhs'] = p[1]
        return p[0]

    @_('WORD ASSIGN')
    def assignment(self, p):
        print('13..')
        temp=dict(lhs=p[0],rhs='')
        return dict(operation='assign',operands=temp)

    @_('assignment BTICK statement BTICK')
    def assignment(self, p):
        print('14..')
        p[0]['operands']['rhs'] = p[2]
        return p[0]

    @_('assignment VALUEOF QMARK')
    def assignment(self, p):
        print('15..')
        p[0]['operands']['rhs'] = p[1]+ p[2]
        return p[0]

    @_('assignment SCOLON')
    def assignment(self, p):
        print('16..')
        return p[0]

    @_('LSQUARE LSQUARE comparison AND comparison RSQUARE RSQUARE SCOLON')
    def conditional(self, p):
        print('17..')
        return dict(operation='AND',operands=[p[2],p[4]])

    @_('LPAREN STRING COMPARE STRING RPAREN')
    def comparison(self,p):
        print('20..')
        temp=dict(lhs=p[1], rhs=p[3])
        return dict(operation='isequalto',operands=temp)

    @_('PLUS PERCENT NUMBER WORD')
    def format(self,p):
        print('21..')
        if p[3] == 's':
            return ('in seconds')

    def error(self, p):
        print("Syntax error at token", p.value , " at line:", p.lineno, "(type=", p.type, "), omitting statement..")


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
              if [[ ( "here" == "am" ) && ( "hello" == "hello" ) ]]; then
              Y=2
              fi
              I_E_T=`date +%25s`
              fi
              if [[ ( "ha" == "magic" ) && ( "is" == "here" ) ]]; then
              X=89
              else
              k=3
              fi
              h=90"""
    lexer = MyLexer()
    parser = MyParser()

    result = parser.parse(lexer.tokenize(data))
    pprint.pprint(result)