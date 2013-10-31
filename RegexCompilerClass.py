'''
Created on Jun 27, 2011

@author: Sam
'''

""" CHANGES:
        * changed rtrn of RegexCompiler to force string to type Text (if not already of type Text)
        * IMporTANT!: stringTogether now returns a non-success the moment (as opposed to at the end) one of the \
            functions it's stringing together returns a non-success!! 
        * !!Y!A!Y!!:! now functions' rtrn-values are actually anded with success!"""


import SettingsHeader

import FuncHeader

from TextClass import Text, e


class RegexCompiler:
    """ This class takes in a tokenized funcRegex (see RegexTokenizerClass) """
    
    classInstanceContainingFuncs = None
    
    def __init__(self, classInstanceContainingFuncs):
        self.classInstanceContainingFuncs = classInstanceContainingFuncs
     
    def compile(self, tokenizedFuncRegex):
        """ the function users of this class are interested in. EXPAND"""
        
        rtrn = FuncHeader.nullFunc
        
        if tokenizedFuncRegex: ## otherwise, we return the current rtrn, which is nullFunc 
            first = tokenizedFuncRegex[0]
            
            def bracketifyOnceIfNecessary(x):
                return [x] if type(x) != type([]) else x
            
            if type(first) == type(''):
                firstLet = first[0]
                if firstLet == '"':
                    firstWithoutDoubleQuotes = first[1:-1]
                    funcNames = []
                    if len(tokenizedFuncRegex) > 1:
                        for i in xrange(1, len(tokenizedFuncRegex)):
                            if not type(tokenizedFuncRegex[i]) == type(''):
                                break
                            funcName = tokenizedFuncRegex[i]
                            e.bark(SettingsHeader.LOW_LEVEL, 'tokenizedFuncRegex=', tokenizedFuncRegex)
                            e.bark(SettingsHeader.MEDIUM_BARK, 'funcName=', funcName)
                            funcNames += [funcName]
                    rtrn = self.compileString(firstWithoutDoubleQuotes, funcNames) ## or to make more consistent, \
                                            ##tokenizedFuncRegex[0][1:-1]
                elif firstLet == '$':
                    rtrn = self.compileNoMatch(self.compile(bracketifyOnceIfNecessary(tokenizedFuncRegex[1])))
                elif firstLet == '~':
                    rtrn = self.compileNot(self.compile(bracketifyOnceIfNecessary(tokenizedFuncRegex[1])))
                elif firstLet == '?':
                    rtrn = self.compileQuestion(self.compile(bracketifyOnceIfNecessary(tokenizedFuncRegex[1])))
                elif firstLet == '*':
                    rtrn = self.compileStar(self.compile(bracketifyOnceIfNecessary(tokenizedFuncRegex[1])))
                elif firstLet == '+':
                    rtrn = self.compilePlus(self.compile(bracketifyOnceIfNecessary(tokenizedFuncRegex[1])))
                elif firstLet == '|':
                    rtrn = self.compileOr([self.compile(bracketifyOnceIfNecessary(nestedRegex)) for nestedRegex in tokenizedFuncRegex[1:]])
                elif firstLet == '@':
                    rtrn = self.compileRecord(self.compile(bracketifyOnceIfNecessary(tokenizedFuncRegex[1])))
            elif type(first) == type([]):
                rtrn = self.stringTogether(*[self.compile(bracketifyOnceIfNecessary(nestedRegex)) \
                                      for nestedRegex in tokenizedFuncRegex])
        
        return (lambda string: rtrn(Text(string)) if type(string)==type('') else rtrn(string))
            
    ## TODO: make *funcs/listOfFuncs in following arguments
    ## (and calls to following functions), MORE CONSISTENT!
    def compileString(self, matchMe, namesOf_funcToExecuteOnSuccess):
        def rtrn(string):
            string.push()
            success = string.matchString(matchMe)

            if success:
                ## update
                self.classInstanceContainingFuncs.lastStringMatched = matchMe
                if matchMe:
                    self.classInstanceContainingFuncs.lastNonemptyStringMatched = matchMe
                
                ## keep successfully-matched string
                string.popAndKeep()
                
                ## function-capability stuff:                
                e.bark(SettingsHeader.LOW_LEVEL, 'namesOf_funcToExecuteOnSuccess=', namesOf_funcToExecuteOnSuccess)
                e.bark(SettingsHeader.MEDIUM_BARK, 'nameToFind =', namesOf_funcToExecuteOnSuccess)
                
                funcRtrn = True
                
                for nameOf_funcToExecuteOnSuccess in namesOf_funcToExecuteOnSuccess:
                    if nameOf_funcToExecuteOnSuccess:
                        if hasattr(self.classInstanceContainingFuncs, nameOf_funcToExecuteOnSuccess):
                            thisFuncRtrn = None
                            try:
                                thisFuncRtrn = getattr(self.classInstanceContainingFuncs, \
                                        nameOf_funcToExecuteOnSuccess)()
                            except TypeError:   ## this is the exception raised when the number of \
                                                ## arguments is wrong
                                try: #TODO: WORK ON THIS!!!!!!!!
                                    thisFuncRtrn = getattr(self.classInstanceContainingFuncs, \
                                                           nameOf_funcToExecuteOnSuccess)(string)
                                except TypeError:
                                    try:
                                        thisFuncRtrn = getattr(self.classInstanceContainingFuncs, \
                                                               nameOf_funcToExecuteOnSuccess)(self.classInstanceContainingFuncs, string)
                                    except TypeError:
                                        thisFuncRtrn = getattr(self.classInstanceContainingFuncs, \
                                                               nameOf_funcToExecuteOnSuccess)(self.classInstanceContainingFuncs)
                            finally:
                                funcRtrn = (thisFuncRtrn or thisFuncRtrn is None) and funcRtrn
                        else:
                            e.error(level = SettingsHeader.MEDIUM, \
                                    message = 'could not find function named \'' + nameOf_funcToExecuteOnSuccess + '\'')
                    else:
                        string.popAndDontKeep()
                        
                success = funcRtrn and success
            return success
        return rtrn
    @staticmethod
    def stringTogether(*funcs):
        def rtrn(string):
            success = True
            for func in funcs:
                success = (True if func(string) in [True, None] else False) and success
                if not success:
                    e.bark(SettingsHeader.LOW_LEVEL, 'not a success \
                    (look in RegexCompilerClass.RegexCompiler.stringTogether')
                    break
            return success
        return rtrn
    @staticmethod
    def compileNoMatch(func):
        def rtrn(string):
            string.push()
    
            success = func(string)
            
            string.popAndDontKeep() ## always DON'T keep
            return success
        return rtrn
    @staticmethod
    def compileNot(func):
        def rtrn(string):
            string.push()
    
            success = not func(string)
            
            if success:
                string.popAndKeep()
            else:
                string.popAndDontKeep()
            return success
        return rtrn
    @staticmethod
    def compileQuestion(func):
        def rtrn(string):
            if func(string):
                pass
    
            success = True
            return success
        return rtrn
    @staticmethod
    def compileStar(func):
        def rtrn(string):    
            
            while True:
                string.push()
                if func(string):
                    string.popAndKeep()
                    continue
                else:
                    string.popAndDontKeep()
                    break
    
            success = True
            return success
        return rtrn
    @staticmethod
    def compilePlus(func):
        def rtrn(string):
            string.push()
            success = func(string) ## important
            
            rtrnBool = success
            
            if success:
                string.popAndKeep()
            else:
                string.popAndDontKeep()
            
            while success:
                string.push()
                success = func(string) ## important
                if success:
                    string.popAndKeep()
                    continue
                else:
                    string.popAndDontKeep()
                    break
    
            return rtrnBool
        return rtrn
    @staticmethod
    def compileOr(listOfFuncs):
        def rtrn(string):
            string.push()
            
            success = False
            for func in listOfFuncs:
                success = success or func(string)
                if success:
                    break
            
            if success:
                string.popAndKeep()
            else:
                string.popAndDontKeep()
            return success
                
        return rtrn
    def compileRecord(self, func):
        def rtrnFunc(string):
            begin = string.position
            rtrn = func(string)
            end = string.position
            self.classInstanceContainingFuncs.recordStack.append(string.string[begin:end])
            return rtrn
        return rtrnFunc
    @staticmethod
    def compileIfElse(func1, func2):
        def rtrn(string):
            pas
            return True


#c = RegexCompiler()
#digit = ['|', '"0"', '"1"']
#operand = ['|', '"-"', '"+"']
#g = c.compile([digit, ['*', [operand, digit]]])
#raw_input()
#expression = Text('0-1+1')
#print g(Text('0-1+1'))
