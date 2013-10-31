'''
Created on Jun 27, 2011

@author: Sam
'''

""" CHANGES: recursion is now possible! (not tested yet)
this is because of funcs to execute being wrapped in a class. modified RegexCompilerClass, too.

in CompilerClass:
        * changed rtrn of RegexCompiler to force string to type Text (if not already of type Text)
        * IMporTANT!: stringTogether now returns a non-success the moment (as opposed to at the end) one of the \
            functions it's stringing together returns a non-success!!
"""


import SettingsHeader

from RegexTokenizerClass import RegexTokenizer, e, Text
from RegexCompilerClass import RegexCompiler

####
e.level = SettingsHeader.ALL_THE_TIME
####


def SAMcompile(funcRegex, classInstanceContainingFuncs, name = None):
    myTokenizer = RegexTokenizer(funcRegex)
    t = myTokenizer.tokenizeRegex()
    
    e.pause(SettingsHeader.ALMOST_ALL_THE_TIME, 'tokenizedRegex=', t)

    myCompiler = RegexCompiler(classInstanceContainingFuncs)
    rtrn = myCompiler.compile(t)
    def rtrnWithStringTransporter(string):
        classInstanceContainingFuncs.__string__ = string
        return rtrn(string)
    
    if name:
        setattr(classInstanceContainingFuncs, name, rtrn)
    
    return rtrn


def match(funcRegex, string, classInstanceContainingFuncs, name = None):
    if type(funcRegex) == type(''):
        funcRegex = SAMcompile(funcRegex, classInstanceContainingFuncs, name)
        
    e.pause(SettingsHeader.HIGH_LEVEL, 'about to apply compiled funcRegex')
    
    return funcRegex(string)


pass ## this `pass' is just to separate the code / comments below from the class defined above.


##class recordTest:
##    recordStack = []
##    def out(self):
##        print self.recordStack.pop()
##
##instance = recordTest()
##
##SAMcompile('("a"|"b")*@""<out>', instance, 'test')
##
##i = raw_input()
##while i:
##    e.bark(SettingsHeader.TO_USER, \
##       instance.test(i))
##    i = raw_input()

#class calculator:
#    stack = [0]
#    op = ''
#    def primeStack(self):
#        self.stack.append(0)
#    def calcError(self):
#        print 'error'
#        self.stack = [0]
#    def useOperator(self):
#        if len(self.stack) > 1:
#            if self.op == '+':
#                self.stack.append(self.stack.pop() + self.stack.pop())
#            elif self.op == '-':
#                self.stack.append(-(self.stack.pop()-self.stack.pop()))
#            else:
#                self.calcError()
#        self.op = ''
#    def push0ToStack(self):
#        self.stack.append(0)
#        self.useOperator()
#    def push1ToStack(self):
#        self.stack.append(1)
#        self.useOperator()
#    def push2ToStack(self):
#        self.stack.append(2)
#        self.useOperator()
#    def plus(self):
#        self.op = '+'
#    def minus(self):
#        self.op = '-'
#    def printValOfStack(self):
#        if len(self.stack) == 1:
#            print self.stack[0]
#        else:
#            self.calcError() 
#
#myCalc = calculator()    
#
#num = '("0"<push0ToStack>|"1"<push1ToStack>|"2"<push2ToStack>)'
#term = num + '|("("<factor>")")' 
#compiledTermRegex = compile(term, myCalc, name = 'term')
#addOperator = '(("+"<plus>""<term>)|("-"<minus>""<term>))'
#
#factor = '((' + addOperator + ')' + '*)'
#compiledFactorRegex = compile(factor, myCalc, name = 'factor')
#
#printedExpression = '""<factor>""<printValOfStack>'
#
##expression = '((' + mulOperator + '""<digit>' + ')' + '*)' 
#
## ## testing whitespace-skipping capabilities
## expression = '("mommy" <ILoveYou>|"mama"<ILoveYouVeryMuch>)*'
#
#e.bark(Settings.SettingsHeader.ALMOST_ALL_THE_TIME, 'factor = ', factor)
#
##simple = '(("hi"<hiho>)|("bye"<hoho>))*'
##
##def hiho():
##    print "hijk"
##def hoho():
##    print "byebye"
#
#e.bark(Settings.SettingsHeader.TO_USER, '\n__start__\n')
#
#compiledRegex = compile(printedExpression, myCalc, name = 'printedExpression')
#i = raw_input()
#while i:
#    e.bark(Settings.SettingsHeader.TO_USER, \
#       match(compiledRegex, i, myCalc))
#    i = raw_input()
#
#e.bark(Settings.SettingsHeader.TO_USER, '\n__end__\n')
