from sly import Parser
import pprint
from cisco.assignment.lexer import MyLexer


class MyParser(Parser):
    # Get the token list from the lexer
    tokens = MyLexer.tokens
    debugfile = 'parser.out'
    tree = dict(root=[])
    currNode = {}
    currParent = ['root']
    nodeChanged = False
    branchCount=0

    def addStatement(self,s):
        print('currParent:',self.currParent)
        curr=self.currParent[-1]
        print('curr:',curr)
        if curr == 'root':
            print('self.tree:', self.tree)
            print('statement:', s)
            print('before append self.tree[curr]:',self.tree[curr])
            self.tree[curr].append(s)
            print('after append self.tree[curr]:', self.tree[curr])
        else:
            if not self.nodeChanged:
                print('self.currNode[curr]:', self.currNode[curr])
                print('statement:', s)
                print('currNode:', self.currNode)
                print('before append self.currNode[curr]:', self.currNode[curr])
                self.currNode[curr].append(s)
                print('after append self.currNode[curr]:', self.currNode[curr])
            else:
                self.nodeChanged=False

    def attachNode(self):
        print('attaching Node')
        curr = self.currParent[-1]
        print('curr:', curr)
        print('tree:',self.tree)
        self.tree[self.currParent[-1]].append(self.currNode)

#TODO - grammar needs update
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
        return self.tree

    @_('statements statement')
    def statements(self, p):
        print('statements statement --> statements')
        self.addStatement(p[1])

    @_('statement')
    def statements(self, p):
        print('statement --> statements')
        self.addStatement(p[0])

    @_('command')
    def statement(self, p):
        print('command --> statement')
        return p[0]

    @_('WORD')
    def words(self, p):
        print('WORD --> words')
        return p[0]

    @_('PRINT')
    def statement(self, p):
        print('PRINT --> statement --',p[0])
        tempNode=dict(print=p[0])
        return tempNode

    @_('IF conditional THEN')
    def statement(self, p):
        print('IF conditional--> statement')
        self.branchCount += 1
        key='IF'+str(self.branchCount)
        temp={}
        temp[key]=[]
        temp['condition']=p[1]
        self.currNode= temp
        self.currParent.append(key)
        self.nodeChanged=True
        return temp

    @_('FI')
    def statement(self, p):
        print('FI --> statement')
        self.currParent.pop()
        self.attachNode()

    @_('assignments')
    def statement(self, p):
        print('assignment --> statement')
        return p[0]

    @_('LET statement')
    def statement(self, p):
        print('LET statement --> statement')
        return p[1]

    @_('DATE format')
    def command(self, p):
        print('DATE format --> command')
        return dict(etime=p[0],format=p[1])

    @_('assignments SCRPTARG')
    def command(self, p):
        print('assignments SCRPTARG --> command')
        tempNode=dict(exec=p[1])
        return tempNode

    @_('assignment')
    def assignments(self, p):
        print('assignment --> assignments')
        return p[0]

    @_('assignment NUMBER')
    def assignment(self, p):
        print('assignment NUMBER --> assignment')
        temp={}
        temp[p[0]]=p[1]
        return dict(assign=temp)

    @_('WORD ASSIGN')
    def assignment(self, p):
        print('WORD ASSIGN --> assignment')
        return p[0]

    @_('assignment BTICK command BTICK')
    def assignment(self, p):
        print('assignment BTICK command BTICK --> assignment')
        temp = {}
        temp[p[0]] = p[2]
        return dict(assign=temp)

    @_('assignment VALUEOF QMARK')
    def assignment(self, p):
        print('assignment VALUEOF QMARK --> assignment')
        temp={}
        temp[p[0]] = p[1]+ p[2]
        return dict(assign=temp)

    @_('assignment SCOLON')
    def assignment(self, p):
        print('assignment SCOLON --> assignment')
        return p[0]

    @_('LSQUARE LSQUARE comparison AND comparison RSQUARE RSQUARE SCOLON')
    def conditional(self, p):
        print('LSQUARE LSQUARE comparison AND comparison RSQUARE RSQUARE SCOLON --> conditional')
        temp = dict(AND=[])
        temp['AND'].append(p[2])
        temp['AND'].append(p[4])
        return temp

    @_('DQUOTE words DQUOTE')
    def quoted(self, p):
        print('DQUOTE words DQUOTE --> quoted')
        return p[1]

    @_('LPAREN quoted COMPARE quoted RPAREN')
    def comparison(self,p):
        print('LPAREN quoted COMPARE quoted RPAREN --> comparison')
        return dict(lhs=p[1],rhs=p[3])

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
              fi
            if [[ ("thing" == "are") && ( "some" == "some" ) ]];then
            Y=2
            fi"""
    lexer = MyLexer()
    parser = MyParser()

    result = parser.parse(lexer.tokenize(data))
    pprint.pprint(result)