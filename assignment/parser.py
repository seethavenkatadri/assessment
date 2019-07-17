from sly import Parser
import pprint
from cisco.assignment.lexer import MyLexer


class MyParser(Parser):
    # Get the token list from the lexer
    tokens = MyLexer.tokens

# program : statements
# statements : statements statement
#		    | statement
# statement : ECHOLINE
#	        | IF conditions THEN statements FI
#           | IF conditions THEN statements ELSE statements FI
#	        | assignments
#	        | LET statement
#           | DATE FORMAT
#           | assignments SCRPTARG
# assignments:assignment
# assignment: assignment NUMBER
#		    | IDENTIFIER assign
#		    | assignment BTICK statement BTICK
#		    | assignment VALUEOF QMARK
#		    | assignment SCOLON
# conditions : LSQUARE LSQUARE comparison AND comparison RSQUARE RSQUARE SCOLON
# comparison: LPAREN STRING COMPARE STRING RPAREN


    @_('statements')
    def program(self,p):
        return dict(node='start',stlist=p[0])

    @_('statements statement')
    def statements(self, p):
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
        return p[0]

    @_('ECHOLINE')
    def statement(self, p):
        return dict(node='print',args=p[0])

    @_('IF conditions THEN statements FI')
    def statement(self, p):
        return dict(node='IF',condition=p[1],stlist=p[3])

    @_('IF conditions THEN statements ELSE statements FI')
    def statement(self, p):
        return dict(node='IF', condition=p[1], ifstlist=p[3],elsestlist=p[5])

    @_('assignments')
    def statement(self, p):
        return p[0]

    @_('LET statement')
    def statement(self, p):
        return p[1]

    @_('assignments SCRPTARG')
    def statement(self, p):
        return dict(node='exec',script=p[1])

    @_('assignment')
    def assignments(self, p):
        return p[0]

    @_('assignment NUMBER')
    def assignment(self, p):
        p[0]['operands']['rhs'] = p[1]
        return p[0]

    @_('IDENTIFIER ASSIGN')
    def assignment(self, p):
        temp=dict(lhs=p[0],rhs='')
        return dict(node='assign',operands=temp)

    @_('assignment BTICK command BTICK')
    def assignment(self, p):
        p[0]['operands']['rhs'] = p[2]
        return p[0]

    @_('assignment VALUEOF QMARK')
    def assignment(self, p):
        p[0]['operands']['rhs'] = p[1]+ p[2]
        return p[0]

    @_('assignment SCOLON')
    def assignment(self, p):
        return p[0]

    @_('LSQUARE LSQUARE comparison AND comparison RSQUARE RSQUARE SCOLON')
    def conditions(self, p):
        return dict(node='AND',operands=[p[2],p[4]])

    @_('LPAREN STRING COMPARE STRING RPAREN')
    def comparison(self,p):
        temp=dict(lhs=p[1], rhs=p[3])
        return dict(node='isequalto',operands=temp)

    @_('DATE FORMAT')
    def command(self,p):
        return dict(node=p[0], format=p[1])

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
              if [[ ( "here" == "magic" ) && ( "some" == "some" ) ]]; then
              I_E_T=`date +%25s`
              else
              Z=5
              fi
              fi
              Y=3
              """
    lexer = MyLexer()
    parser = MyParser()

    result = parser.parse(lexer.tokenize(data))
    pprint.pprint(result)