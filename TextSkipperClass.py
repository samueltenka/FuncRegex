'''
Created on Jun 27, 2011

@author: Sam
'''

import SymbolsClass
import TextClass

class TextSkipper(SymbolsClass.Symbols, Parser.TextClass.Text):
    position = 0
    myText = ""
    def atEnd(self):
        return self.position >= len(self.myText)
    def currentChar(self):
        if not self.atEnd():
            return self.myText[self.position]
    def forward(self):
        self.position += 1
    def matchChar(self, char):
        if self.currentChar() == char:
            self.forward()
        else:
            pass #
    def skipWhiteSpace(self):
        while self.currentChar() in self.whitespace:
            self.forward()
    def skipComment(self):
        self.match('lineCommentSym') ## TODO: ??? (understand what this does)
        while self.currentChar() != self.endOfLine:
            self.forward()
