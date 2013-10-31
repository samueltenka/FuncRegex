'''
Created on Jun 27, 2011

@author: Sam
'''

from ErrorFileClass import e
import SettingsHeader as S
import Symbols as Syms

class Token():
    text = ""
    tokenType = ""
    
    def __init__(self, text):
        self.text = text
        if not text:
            e.error(S.PASSABLE, 'empty text for token found')
        elif self.text in Syms.digits:
            self.tokenType = 'NUMBER'
        elif self.text in Syms.alphaNumeric:
            if self.text in ['if', 'elif', 'else', 'while', 'for']
            self.tokenType =  ''
        elif self.text in Syms.digits:
            self.tokenType = 'NUMBER'
        elif self.text in Syms.digits:
            self.tokenType = 'NUMBER'
        elif self.text in Syms.digits:
            self.tokenType = 'NUMBER'
