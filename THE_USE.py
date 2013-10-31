'''
Created on Jul 16, 2011

@author: Sam
'''

from SAM_CODE_FuncContaining_Class import *

SAM_CODE = Machine(10)


whitespace = '((" ")*)'
digitList = '"0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"'
alphabetList = ''.join(['"'+char+'"'+'|' for char in 'abcdefghijklmnopqrstuvwxyz']) [:-1] ## without last char, because last char is '|'
print alphabetList
identifier = '($(~("if"|"print"|"del")))((""<alphabetList>)+)@'
variable = '(""<identifier>""<useVar>)'
#digit = '(""<digitList>""<pushDigit>)'
digit = '""<digitList>""<pushDigit>'
digits = '(($(""<digitList>)""<digit>)+)(""<numToStack>)'
#$(""<digitList>)
#number = '""<digits>((".")<digits>)?'
list = '"["<initList>(""<expression>""<appendToList>)*"]"<reveal>'
unit = '(("+"|"-"<negate>)?)(("("<expression>")")|(($(""<digitList>)""<digits>)|(""<list>)|($(""<alphabetList>)""<variable>)))""<whitespace>'
listOperatedFactor = '""<unit>((("["<expression>"]"<getElement>))?)'
mulopThenFactor = '("*"<whitespace>""<listOperatedFactor>""<mulOp>)|("/"<whitespace>""<listOperatedFactor>""<divOp>)'
term = '""<listOperatedFactor>($("*"|"/")""<mulopThenFactor>)*'
addopThenTerm = '("+"<whitespace>""<term>""<addOp>)|("-"<whitespace>""<term>""<subOp>)'
arithExp = '""<term>($("+"|"-")""<addopThenTerm>)*'
relThenArithExp = '("=="<whitespace>""<arithExp>""<eqsOp>)|("!="<whitespace>""<arithExp>""<neqOp>)'
relationship = '""<arithExp>($("=="|"!=")""<relThenArithExp>)*'
andThenRelationship = '"and"<whitespace>""<relationship>""<andOp>'
andExp = '""<relationship>($("and")""<andThenRelationship>)*'
orThenAndExp = '"or"<whitespace>""<andExp>""<orOp>'
orExp = '""<andExp>($("or")""<orThenAndExp>)*'
expression = '""<orExp>'
printStatement = '"print "<whitespace>""<expression>""<out>'
assignmentStatement = '""<identifier>""<whitespace>"="<whitespace>(""<expression>)""<assign>' #""<reveal>'
delStatement = '"del "<whitespace>""<identifier>""<delete>'
revealStatement = '"!reveal!"<reveal>'
ifStatementBegin = '"if"<whitespace>"("<expression>")"'
statement = '(""<assignmentStatement>|""<delStatement>|""<expression>|""<printStatement>|""<revealStatement>)""<endOfStatement>'

##statement = '(""<expression>|""<assignmentStatement>|""<printStatement>|""<block>"")'
#### insert/define functions to execute!!!!!
#ifStatement = '"if "<whitespace>""<expression>""<whitespace>""<statement>(("elif "<expression>""<whitespace>""<statement>("else "<statement>)?)?)'
##
##block = '"<"<whitespace>(""<statement>)*">"'

SAMcompile(whitespace, SAM_CODE, 'whitespace')
SAMcompile(digitList, SAM_CODE, 'digitList')
SAMcompile(digit, SAM_CODE, 'digit')
SAMcompile(digits, SAM_CODE, 'digits')
SAMcompile(alphabetList, SAM_CODE, 'alphabetList')
SAMcompile(identifier, SAM_CODE, 'identifier')
SAMcompile(variable, SAM_CODE, 'variable')
#SAMcompile(number, SAM_CODE, 'number')
SAMcompile(list, SAM_CODE, 'list')
SAMcompile(listOperatedFactor, SAM_CODE, 'listOperatedFactor')
SAMcompile(unit, SAM_CODE, 'unit')
SAMcompile(mulopThenFactor, SAM_CODE, 'mulopThenFactor')
SAMcompile(term, SAM_CODE, 'term')
SAMcompile(addopThenTerm, SAM_CODE, 'addopThenTerm')
SAMcompile(arithExp, SAM_CODE, 'arithExp')
SAMcompile(relThenArithExp, SAM_CODE, 'relThenArithExp')
SAMcompile(relationship, SAM_CODE, 'relationship')
SAMcompile(andThenRelationship, SAM_CODE, 'andThenRelationship')
SAMcompile(andExp, SAM_CODE, 'andExp')
SAMcompile(orThenAndExp, SAM_CODE, 'orThenAndExp')
SAMcompile(orExp, SAM_CODE, 'orExp')
SAMcompile(expression, SAM_CODE, 'expression')
SAMcompile(printStatement, SAM_CODE, 'printStatement')
SAMcompile(assignmentStatement, SAM_CODE, 'assignmentStatement')
SAMcompile(delStatement, SAM_CODE, 'delStatement')
SAMcompile(revealStatement, SAM_CODE, 'revealStatement')
SAMcompile(ifStatementBegin, SAM_CODE, 'ifStatementBegin')
SAMcompile(statement, SAM_CODE, 'statement')

#SAMcompile(block, SAM_CODE, 'block')
#SAMcompile(ifStatement, SAM_CODE, 'ifStatement')
 

def withIfStatement(self):
    def rtrn(string):
        success = True
        success = success and self.ifStatementBegin(string)
        if success:
            condition = bool(self.stackPop())
            if condition:
                success = success and self.statement(string)
            else:
                print "else"
        else:
            success = success and self.statement(string)
        return success
    return rtrn
    

setattr(SAM_CODE, 'withIfStatement', withIfStatement(SAM_CODE))


while True:
    print 'please enter an expression'
    #error = SAM_CODE.withIfStatement(raw_input()) == False
    error = SAM_CODE.statement(raw_input()) == False
    if error:
        print
        print '~?~'
        print
    print


print 'OK!'
