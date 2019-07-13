from sly import Parser
import pprint
from cisco.assignment.lexer import MyLexer


class MyParser(Parser):
    # Get the token list from the lexer
    tokens = MyLexer.tokens
    debugfile = 'parser.out'

    ## Starting conditions
    tree = dict(root=[])  ## one main tree for the AST
    currNode = {}   ## one temp node for every branch the execution takes
    currParent = ['root'] ## to remember the path that the program has taken
    branchCount = 0 ## count to differentiate multiple Ifs

    nodeChanged = False

    def addStatement(self,s):
        curr=self.currParent[-1]
        if curr == 'root':
            if self.nodeChanged:
                self.nodeChanged = False
            else:
                self.tree[curr].append(s)
        else:
            if self.nodeChanged:
                self.nodeChanged = False
            else:
                self.currNode[curr].append(s)

    def attachNode(self):
        self.tree[self.currParent[-1]].append(self.currNode)

# program : statements
# statements : statements statement
#		    | statement
# statement : command
#	        | ECHOLINE
#	        | IF conditionals THEN
#	        | FI
#	        | assignments
#	        | LET statement
# command : DATE format
#	        | assignments SCRPTARG
# assignments:assignment
# assignment: assignment NUMBER
#		    | WORD assign
#		    | assignment BTICK command BTICK
#		    | assignment VALUEOF QMARK
#		    | assignment SCOLON
# conditional : LSQUARE LSQUARE comparison AND comparison RSQUARE RSQUARE SCOLON
# words : WORD
# quoted: DQUOTE words DQUOTE
# comparison: LPAREN quoted COMPARE quoted RPAREN
# format : PLUS PERCENT NUMBER WORD







    @_('statements')
    def program(self,p):
        return self.tree

    @_('statements statement')
    def statements(self, p):
        self.addStatement(p[1])

    @_('statement')
    def statements(self, p):
        self.addStatement(p[0])

    @_('command')
    def statement(self, p):
        return p[0]

    @_('ECHOLINE')
    def statement(self, p):
        return dict(print=p[0])

    @_('IF conditional THEN')
    def statement(self, p):
        ### Start a new branch
        self.branchCount += 1
        key='IF'+str(self.branchCount)
        temp={}
        temp[key]=[]
        temp['condition']=p[1]
        self.currNode=temp
        self.currParent.append(key)
        self.nodeChanged=True
        return temp

    @_('FI')
    def statement(self, p):
        ## Finish processing a IF branch
        ## and move back to the main branch
        self.currParent.pop()
        self.attachNode()
        self.nodeChanged = True

    @_('assignments')
    def statement(self, p):
        return p[0]

    @_('LET statement')
    def statement(self, p):
        return p[1]

    @_('DATE format')
    def command(self, p):
        return dict(command=p[0], format=p[1])

    @_('assignments SCRPTARG')
    def command(self, p):
        return dict(exec=p[1])

    @_('assignment')
    def assignments(self, p):
        return p[0]

    @_('assignment NUMBER')
    def assignment(self, p):
        key=[x for x in p[0]['assign'].keys()]
        p[0]['assign'][key[0]] = p[1]
        return p[0]

    @_('WORD ASSIGN')
    def assignment(self, p):
        temp={}
        temp[p[0]]=''
        return dict(assign=temp)

    @_('assignment BTICK command BTICK')
    def assignment(self, p):
        key = [x for x in p[0]['assign'].keys()]
        p[0]['assign'][key[0]] = p[2]
        return p[0]

    @_('assignment VALUEOF QMARK')
    def assignment(self, p):
        key = [x for x in p[0]['assign'].keys()]
        p[0]['assign'][key[0]] = p[1]+ p[2]
        return p[0]

    @_('assignment SCOLON')
    def assignment(self, p):
        return p[0]

    @_('LSQUARE LSQUARE comparison AND comparison RSQUARE RSQUARE SCOLON')
    def conditional(self, p):
        return dict(AND=[p[2],p[4]])

    @_('WORD')
    def words(self, p):
        return p[0]

    @_('DQUOTE words DQUOTE')
    def quoted(self, p):
        return p[1]

    @_('LPAREN quoted COMPARE quoted RPAREN')
    def comparison(self,p):
        return dict(lhs=p[1],rhs=p[3])

    @_('PLUS PERCENT NUMBER WORD')
    def format(self,p):
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
              I_E_T=`date +%25s`
              fi
            """
    lexer = MyLexer()
    parser = MyParser()

    result = parser.parse(lexer.tokenize(data))
    pprint.pprint(result)