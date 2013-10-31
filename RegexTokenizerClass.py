'''
Created on Jun 27, 2011

@author: Sam
'''

"""CHANGES FROM LAST VERSION:
    * noMatch added (so doesn't eat up text) symbol is '$'"""


import SettingsHeader as S
from TextClass import Text, e

class RegexTokenizer(Text):
    """ RegexTokenizer's `__init__' takes in a string which is supposed \
    to contain a text-form of a funcRegex. `tokenizeRegex' is the function \
    which tokenizes the regex you passed; must be called manually (i.e., \
    `tokenizeRegex' is not called by `__init__' 
    
    It inherits from the Text class."""
    
    success = True
    
    def __init__(self, string):
        Text.__init__(self, string)
    
    def and_MatchSuccess_WithSuccess(self, stringToMatch):
        value = self.matchStringSkippingWhitespace(stringToMatch)
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, 'success=', self.success, 'stringToMatch=', stringToMatch, 'value=', value)
        self.success = value \
                and self.success ## ORDER MATTERS!!!
       
    def tokenizeRegex(self):
        """ takes a funcRegex such as `("a"|"b"<b_func>|"c")*' and converts 
        it to Polish nested-list-form, e.g. ['*', ['|', 'a', ['b', 'b_func'], 'c']]. NO SPACE ALLOWED IN INPUT """
        
        def unbracketifyAsMuchAsPossible(x):
            while type(x) == type([]) and len(x) == 1:
                x = x[0]
            if type(x) == type([]):
                x_ = []
                for y in x:
                    x_ += [unbracketifyAsMuchAsPossible(y)]
                x = x_                       
                    
            return x
        
        def bracketifyOnceIfNecessary(x):
            return [x] if type(x) != type([]) else x
        
        rtrn = []
        while not self.isAtEnd() and not self.current() == ')':
            e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, 'bigLoop poos=', self.position)
            e.bark(S.ENTER_OR_EXIT_FUNCTION, '{entering or')
            rtrn += [self.tokenizeWithIfElse()]
            e.bark(S.ENTER_OR_EXIT_FUNCTION, '}exiting or')
            
        if self.success != True:
            e.error(S.MEDIUM, 'unsuccessful regex tokeniztion of \'' + self.string + '\'')
        return bracketifyOnceIfNecessary(unbracketifyAsMuchAsPossible(rtrn))
       
    def tokenizeString(self):     
        e.bark(S.ENTER_OR_EXIT_FUNCTION, 'entering tokeniZeString')
        e.bark(S.LOW_LEVEL, 'pos=', self.position)

        self.and_MatchSuccess_WithSuccess('"')
        
        content = ''
        e.bark(S.LOW_LEVEL, 'success so far=', self.success)
        while self.current() and self.current() in ' \t\n' + '0123456789' + ',./<>?;:[]\\{}|`~!@#$%^&*()-=_+' + 'abcdefghijklmnopqrstuvwxyz_': ## TODO: replace with proper text-symbols from SymbolsClass
            e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, 'finding content of string')
            content += self.current()
            e.bark(S.LOW_LEVEL, 'conmtent=', content)
            self.next()
            e.bark(S.LOW_LEVEL, 'pos=', self.position)

        self.and_MatchSuccess_WithSuccess('"')
        e.bark(S.LOW_LEVEL, 'success so far=', self.success)
        
        e.bark(S.ENTER_OR_EXIT_FUNCTION, 'done with tokenizeString; returning:', '"' + content + '"')
        return ['"' + content + '"']
    def tokenizeFunc(self):
        e.bark(S.ENTER_OR_EXIT_FUNCTION, 'entering tokenizeFunc')
        self.and_MatchSuccess_WithSuccess('<')
        
        name = ""    
        if self.current() in '_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz': ## TODO: replace with proper identifier from SymbolsClass
            name += self.current()
            self.next()
        else:
            e.error(S.MEDIUM, 'function name must start with alphanumeric char')
        while self.current() in '0123456789_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz': ## TODO: replace with proper identifier from SymbolsClass
            name += self.current()
            self.next()

        self.and_MatchSuccess_WithSuccess('>')
        
        e.bark(S.LOW_LEVEL, 'name =', name)
        return [name]
    def tokenizeUnit(self):
        rtrn = []
        if self.current() == '"' or self.current() == '(':
            if self.current() == '"':
                e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '{entering string')
                rtrn = self.tokenizeString()
                e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '}exiting string; rtrn=', rtrn)
                
                e.bark(S.SPECIFIC_BUG, 'tokenizeUnit: identified / tokenized string. about \
                to tokenize function , if there is any.')
                
                while self.currentSkippingWhitespace() == '<': ## TODO: RIGHT NOW FUNCTIONS ARE ONLY AVAILABLE RIGHT AFTER STRINGS; \
                    ## MAKE THEM AVAILABLE RIGHT AFTER PARENTHESIZED EXPRESSIONS, TOO! (when we do so, change \
                    ## compilerClass, too!
                    e.bark(S.SPECIFIC_BUG, 'self.current() == \'<\'')
                    rtrn += self.tokenizeFunc()
                    
                rtrn = [rtrn]
                e.bark(S.MEDIUM_BARK, 'rtrn for unit of string with possible function is', rtrn)
            elif self.current() == '(':
                e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '{entering paren')
                
                self.and_MatchSuccess_WithSuccess('(')
                
                e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '{entering regex in paren')
                
                rtrn = self.tokenizeRegex()
                
                e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '}exiting regex in paren')
                e.bark(S.LOW_LEVEL, self.position, self.current())
                
                self.and_MatchSuccess_WithSuccess(')')
                
                e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '}entering paren')
                e.bark(S.LOW_LEVEL, 'position=', self.position)
        
        e.bark(S.MEDIUM_BARK, 'exiting tokenizeUnit')
        e.pause(S.LOW_LEVEL)
        return rtrn
    def tokenizeWithNoMatch(self):             
        thereIsQuestion = (self.currentSkippingWhitespace() == '$')
        if thereIsQuestion:
            self.matchStringSkippingWhitespace('$')
        
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, 'thereIs'+'$'+'  =', thereIsQuestion)
        
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '{entering unit')
        unitBefore = self.tokenizeUnit()
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '}exiting unit')
        
        if thereIsQuestion:
            return ['$'] + [unitBefore]
        else:
            return [unitBefore]    
    def tokenizeWithNot(self):             
        thereIsQuestion = (self.currentSkippingWhitespace() == '~')
        if thereIsQuestion:
            self.matchStringSkippingWhitespace('~')
        
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, 'thereIs'+'~'+'  =', thereIsQuestion)
        
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '{entering noMatch')
        unitBefore = self.tokenizeWithNoMatch()
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '}exiting noMatch')
        
        if thereIsQuestion:
            return ['~'] + [unitBefore]
        else:
            return [unitBefore]
    def tokenizeWithQuestion(self):
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '{entering not')
        unitBefore = self.tokenizeWithNot()
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '}exiting not')
                 
        thereIsQuestion = (self.currentSkippingWhitespace() == '?')
        if thereIsQuestion:
            self.matchStringSkippingWhitespace('?')
        
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, 'thereIs'+'?'+'  =', thereIsQuestion)
        
        if thereIsQuestion:
            return ['?'] + [unitBefore]
        else:
            return [unitBefore]
    def tokenizeWithStar(self):
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '{entering question')
        unitBefore = self.tokenizeWithQuestion()
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '}exiting question')
                 
        thereIsStar = (self.currentSkippingWhitespace() == '*')
        if thereIsStar:
            self.matchStringSkippingWhitespace('*')
        
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, 'thereIs'+'*'+'  =', thereIsStar)
        
        if thereIsStar:
            return ['*'] + [unitBefore]
        else:
            return [unitBefore]
    def tokenizeWithPlus(self):
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '{entering star')
        unitBefore = self.tokenizeWithStar()
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '}exiting star')
                 
        thereIsPlus = (self.currentSkippingWhitespace() == '+')
        if thereIsPlus:
            self.matchStringSkippingWhitespace('+')
        
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, 'thereIs'+'+'+'  =', thereIsPlus)
        
        if thereIsPlus:
            return ['+'] + [unitBefore]
        else:
            return [unitBefore]
    def tokenizeWithOr(self):
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '{entering plus')
        rtrn = self.tokenizeWithPlus()
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '}exiting plus')
        
        while self.currentSkippingWhitespace() == '|':
            if rtrn[0] != '|':
                rtrn = ['|'] + [rtrn]
            self.next()
            e.bark(S.LOW_LEVEL, self.position)
            e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '{entering plus')
            addMe = self.tokenizeWithPlus()
            e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '}exiting plus')
            rtrn += addMe
        
        return [rtrn]
    
    def tokenizeWithRecord(self):
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '{entering or')
        unitBefore = self.tokenizeWithOr()
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '}exiting or')
                 
        thereIsRecord = (self.currentSkippingWhitespace() == '@')
        if thereIsRecord:
            self.matchStringSkippingWhitespace('@')
        
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, 'thereIs'+'@'+'  =', thereIsRecord)
        
        if thereIsRecord:
            return ['@'] + [unitBefore]
        else:
            return [unitBefore]
    
    def tokenizeWithIfElse(self):
        thereIsIfElse = (self.currentSkippingWhitespace() == '^')
        
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '{entering record')
        unitBefore1 = self.tokenizeWithRecord()
        e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '}exiting record')
        
        if thereIsIfElse:
            self.matchStringSkippingWhitespace('^')
            
            e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '{entering record')
            unitBefore2 = self.tokenizeWithRecord()
            e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, '}exiting record')
            
            e.bark(S.STATE_OF_HIGH_LEVEL_FUNCTION, 'thereIs'+'^'+'  =', thereIsIfElse)
            
            return ['^'] + [unitBefore1, unitBefore2]
        else:
            return [unitBefore1]
        

pass ## this `pass' is just to separate the code / comments below from the class defined above.

#e.level = S.LOWEST_LEVEL
#raw_input('3')
##a = RegexTokenizer('(~("hames"|"heam"))')
#a = RegexTokenizer('"hames"|("j"+)')
#print a.current()
#print a.tokenizeRegex()
#print a.current()
#raw_input('30')
