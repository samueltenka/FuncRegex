'''
Created on Jun 27, 2011

@author: Sam
'''

import TokenizerClass

class TokenList:
    position = 0
    tokensList = []

    doesMatchEat = True

    def __init__(self, text):
        myTokenizer = TokenizerClass.Tokenizer(text)
        self.tokensList = myTokenizer.tokensList

    def __len__(self):
        return len(self.tokensList)
    def atEnd(self):
        return self.position >= self.__len__()
    def currentToken(self):
        if not self.atEnd():
            return self.tokensList[self.position]
    def match(self, tokenType):
        text = ""

        if self.currentToken().tokenType == tokenType:
            if self.doesMatchEat:
                self.position += 1
        else:
            #
            ###
            ## TODO: tHIS iS ThE mOST imPOrtanT BIT of ERROR HANDLING!!!
            ###
            #
            pass
            
        return text
    def matcher(self, tokenType):
        def returnFunction():
            self.match(tokenType)
        return returnFunction
    pass
