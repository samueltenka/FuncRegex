'''
Created on Jun 27, 2011

@author: Sam
'''

from TokenClass import Token
import TextSkipperClass

class Tokenizer(TextSkipperClass.TextSkipper):
    text = ""
    tokensList = []

    def __init__(self, text):
        self.myText = text
        self.tokenize()

    def tokenize(self):
        self.tokensList = []
        while not self.atEnd():
            currentChar = self.currentChar()
            if currentChar in self.alphabet:
                self.tokensList += [Token(self.getIdentifier())]
            elif currentChar in self.numberSyms:
                self.tokensList += [Token(self.getNumber())]
            else:
                self.tokensList += [Token(self.getSym())]
    
    def __getStringOfACharType__(self, listOfAllowableChars):
        """"""
        text = ""
        while self.currentChar() in listOfAllowableChars:
            text += self.currentChar()
            self.forward()
        return text
    def getNumber(self):
        """These representations are all OK: "729.", "729.0", "08.80", ".8080" """
        if self.currentChar() in self.numberSyms:
            text = ""
            text += self.__getStringOfACharType__(self.digits) ## get pre-decimal-point digits
            if self.currentChar() == self.decimalPoint: ## get possible decimal point . . .
                text += '.'
                text += self.__getStringOfACharType__(self.digits) ## . . . and get digits after decimal point
            return text
    def getIdentifier(self):
        """ "Abc", "sls_34567vs__", "a234567", and "a______a_" are OK, but "_Abc", "4ndo", and "268" are not. """
        if self.currentChar() in self.alphabet:
            return self.__getStringOfACharType__(self.alphaNumeric)
    def getSym(self):
        """ gets the longest symbol it can, given the starting position """
        text = ""
        charToPossiblyAppend = self.currentChar()
        while text + charToPossiblyAppend in self.syms:
            text += charToPossiblyAppend
            self.forward()
        return text
