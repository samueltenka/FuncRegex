'''
Created on Jun 27, 2011

@author: Sam
'''

import time


import SettingsHeader


class Barker:
    """ barks for debugging; level-adjustable so that we can easily set to \
    almost not bark at all (set self.level = SettingsHeader.TO_USER) """
    debugOn = SettingsHeader.debugOn
    
    level = SettingsHeader.LOW_LEVEL
    
    def bark(self, level = SettingsHeader.LOW_LEVEL, *args):
        if level >= self.level:
            if self.debugOn:
                print SettingsHeader.barkMessage, SettingsHeader.barkIndent * -level,
                for arg in args:
                    print arg, ## print(arg, sep = SettingsHeader.barkSpacer, end = '')
                print
    def pause(self, level = SettingsHeader.LOWEST_LEVEL, *args):
        if level >= self.level:
            if self.debugOn:
                self.bark(level, SettingsHeader.pauseMessage, *args)
                raw_input()


class Debug(Barker):
    """ just a little class to help with debugging, which is globbed onto ErrorFileHandler """
    debugOn = SettingsHeader.debugOn
    
    watchedVars = []
    
    def appendWatchedVars(self, *args):
        self.watchedVars += [arg for arg in args if not arg in self.watchedVars]
    def setWatchedVars(self, *args):
        self.watchedVars = args
    def resetWatchedVars(self, *args):
        self.watchedVars = []
        
    def watch(self, *args):
        for i in self.watchedVars:
            self.bark(i)

class ErrorFileHandler(Debug):
    """ fill in """
      
    errorFile = None
    
    def __init__(self, errorFileName = SettingsHeader.errorFileName):
        self.errorFile = open(errorFileName, 'w')
        
    def error(self, level, message = ""):
        localTime = time.ctime(time.time())
        fullmessage = localTime + ':\t (level ' + str(level) + ')  ' + message
        print SettingsHeader.errorMessage + fullmessage
        self.errorFile.write(fullmessage)
        
    def getMessages(self, aboveOrEqualToThisErrorLevel, startTimeInclusive = None, endTimeExclusive = None):
        ## TODO: FIT TO localTime, "level" level, message format!!!!! (SEE ErrorFileHandler.error)
        ## add startTimeInclusive/endTimeExclusive FUNCtionality!! !!
        return [fullmessage for fullmessage in self.errorFile.read() \
                if eval(fullmessage.split()[0]) >= aboveOrEqualToThisErrorLevel] #and ]
    
    def __del__(self):
        if self.errorFile:
            self.errorFile.close()


e = ErrorFileHandler()
if e.level >= SettingsHeader.GENERAL_BUG:
    print 'BARK:'
    e.bark(SettingsHeader.GENERAL_BUG, 'test of bark capabilities:', 'bark is OK!')
    print ':KRAB'
