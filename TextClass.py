'''
Created on Jun 27, 2011

@author: Sam
'''

"""CHANGES FROM PREVIOUS VERSION: 
    * skipwhitespace added
    * minor docstring changes made
    * imported from symbolsclass to write skipwhitespace
    * made matchStringSkippingWhitespace"""


from ErrorFileClass import e, SettingsHeader
import SymbolsClass


class Text:
    """ wraps a string to be ready for a funcRegex to be applied to it; \
    even is good for wrapping (string rep.s of) funcRegexes, as they are governed by funcRegexes themselves CHANGE!"""
    
    string = ""
    position = 0
    positionStack = [] ## see text.push() / text.popAndDontKeep()/text.popAndKeep()
    
    def __init__(self, string):
        self.position = 0
        self.string = string
    
    """ the following culminates in matchString, which matches a string from the text """ 
    def isAtEnd(self):
        return self.position >= len(self.string)
    def current(self):
        e.bark(SettingsHeader.LOW_LEVEL, \
               'in current poos =', self.position, \
               ' content=', self.string[self.position] if not self.isAtEnd() else None)
        if not self.isAtEnd():
            return self.string[self.position]
    def next(self):
        self.position += 1
        e.bark(SettingsHeader.LOW_LEVEL, 'Next ', 'pos was ', self.position-1, ' pos is ', self.position)   
    def skipWhitespace(self):
        e.bark(SettingsHeader.LOWEST_LEVEL, 'entering SkipWhitespace')
        while self.current() in SymbolsClass.Symbols.whitespace:
            self.next()
            e.bark(SettingsHeader.LOWEST_LEVEL, 'skipped the whitespace char \''+self.current()+'\'')
    def currentSkippingWhitespace(self):
        self.skipWhitespace()
        return self.current()
    def matchChar(self, char, errorOnFailure):
        e.bark(SettingsHeader.LOW_LEVEL, 'trying to match', char)
        if self.current() == char:
            self.next()
            e.bark(SettingsHeader.LOW_LEVEL, 'matched', char, '', 'new pos =', self.position)
            return True
        else:
            if errorOnFailure:  
                e.error(level = SettingsHeader.MEDIUM, message = 'could not match character \'' + char + \
                        '\' in string \'' + self.string + '\' at position ' + str(self.position) + '.')
            else:
                return False
    def matchString(self, string, errorOnFailure = None):
        e.bark(SettingsHeader.STATE_OF_HIGH_LEVEL_FUNCTION, 'entering matchString')
        if errorOnFailure == None:
            errorOnFailure = True if self.isReal() else False
        
        rtrn = True
        for char in string:
            e.bark(SettingsHeader.LOW_LEVEL, 'regex-char we want to match is', char)
            rtrn = self.matchChar(char, errorOnFailure) and rtrn ## ORDER MATTERS!
        
        e.bark(SettingsHeader.STATE_OF_HIGH_LEVEL_FUNCTION, 'exiting matchString', 'rtrn=', rtrn)
        return rtrn
    def matchStringSkippingWhitespace(self, string, errorOnFailure = None):
        e.bark(SettingsHeader.MEDIUM_BARK, 'entering matchStringSkippingWhitespace')
        e.bark(SettingsHeader.LOW_LEVEL, 'skipping whitespace')
        self.skipWhitespace()
        rtrn = self.matchString(string, errorOnFailure)
        #self.skipWhitespace()
        return rtrn
        
    """ just some useful stuff """
    def restOfString(self):
        return self.string[:self.position]
  
    """ for back-tracking """
    def depth(self):
        return len(self.positionStack)
    def isReal(self):
        return self.depth() == 0
    """ more stuff for back-tracking """
    def push(self):
        self.positionStack += [self.position]
    def popAndDontKeep(self):
        self.position = self.positionStack[-1]
        self.positionStack = self.positionStack[:-1]
    def popAndKeep(self):
        self.positionStack = self.positionStack[:-1]
        self.position = self.position
        
