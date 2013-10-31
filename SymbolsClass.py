'''
Created on Jun 27, 2011

@author: Sam
'''

import ErrorFileClass

class Symbols(ErrorFileClass.ErrorFileHandler):
    __lowerCaseAlphabet__ = 'abcdefghijklmnopqrstuvwxyz'
    alphabet = (__lowerCaseAlphabet__ + __lowerCaseAlphabet__.upper()).split()
    digits = '012456789'.split()
    alphaNumeric = alphabet + ['_'] + digits
    numSyms = digits + ['.'] + ['e']
    
    whitespace = ' \t\n'.split()
    endOfLine = '\n'.split()
    lineCommentSym = '#'.split()

    syms = "+ - * / % ! & | ^ && || ^^ < <= == >= > != << >> [ ] ( ) { } , . ? ~!@$^&() )(*&^%#@!~".split(' ')
