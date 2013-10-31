'''
Created on Jul 8, 2011

@author: Sam
'''

"""multiple-digits!!!
killed off `self.ans` and replaced with more local `ans`
fixed 'every other one' memory.memory bug
MEMORY MANAGENMENT: Check!
lists!!"""

from ErrorFileClass import e
from SettingsHeader import *

from FunctionRegexLibrary import SAMcompile, match

from FuncHeader import nullFunc



class SAM_Object: ## TODO: work on this
    value = None
    SAMtype = 'NoneType'
    
    def __init__(self, value = '', SAMtype = None):
        self.value = value
        if SAMtype is None:
            if type(value) == type(0):
                self.SAMtype = 'int'
            elif type(value) == type(0.0):
                self.SAMtype = 'float'
            elif type(value) == type(''):
                self.SAMtype = 'str'
            elif type(value) == type([]):
                self.SAMtype = 'list'
            else:
                e.error(MEDIUM, 'could not identify type of object')
    def __str__(self):
        return ' ' + str(self.value) + ' ' +  str(self.SAMtype) + '  '
    pass

nullObject = SAM_Object() ## will be the `None` of SAM_CODE


SAMMemException = Exception('SAMMemException')

def memSizeError():
    raise SAMMemException


def __strOfList__(l):
    return reduce(lambda x, y: x+' '+y, [str(object) for object in l])


class Stack:
    """ Stack simulates an "infinite" stack. 
    `None` in `stack` means that we are at the very bottom of stack (do not modify `None` at bottom of `stack`) """
    
    stack = [None]
    registerA = 0
    registerB = 0    
    
    def __str__(self):
        return 'stack = ' + __strOfList__(self.stack) + '\n registerA = ' + str(self.registerA) + '\n registerB = ' + str(self.registerB)
    
    def stackLength(self):
        return len(self.stack) - 1 ## because at the very bottom of stack is `None`, which we don't use (just a marker to show end of stack)
    def stackPop(self):
        if self.stackLength() > 0:
            self.registerA = self.stack.pop()
            e.bark(HIGH_LEVEL, 'stack =', self.stack)
            return self.registerA 
        else:
            memSizeError()
        e.bark(HIGH_LEVEL, 'stack =', self.stack)
    def stackPush(self, value):
        self.stack.append(value)
        e.bark(HIGH_LEVEL, 'stack =', self.stack)
    def stackReset(self):
        self.stack = [None]


class Memory:
    """ Memory simulates a fixed amount of memory, in addition to a dictionary which maps names to object memory-addresses 
    `None` in `memory` means that it is free """
    
    memory = []
    __firstFreeMemoryPosition__ = 0 ## just to speed-up free-memory finding
                                    ## (REMEMBER TO ADJUST THIS ACCORDINGLY WHENEVER MEMORY IS FILLED / FREED!)
    dictOfVarsAddresses = {}
    addressToReferencesDict = {}
    
    def __str__(self):
        return 'memory =' + __strOfList__(self.memory) + \
            '\n dictOfVarsAddresses = ' + str(self.dictOfVarsAddresses) + '\n addressToReferencesDict = ' + str(self.addressToReferencesDict) + \
            '\n __firstFreeMemoryPosition__ = ' + str(self.__firstFreeMemoryPosition__)
    
    def __init__(self, memorySize):
        if memorySize > 1:
            self.memory = [None] * memorySize
        else:
            e.error(MEDIUM, 'memory of virtual machine must be longer than 0 slots!')
    
    def getMemory(self, position):
        if position < len(self.memory):
            return self.memory[position]
        else:
            memSizeError()
    def setMemory(self, position, object):
        if type(object) != type(nullObject):
            e.error(MEDIUM, 'object is not of type \'SAM_Object\', and so should not be in memory.')
            return
        if position < len(self.memory):
            self.memory[position] = object
        else:
            memSizeError()
    
    def findFreeMemory(self, numberOfSlotsNeeded = 1):
        returnPositions = []
        locationInMemory = self.__firstFreeMemoryPosition__ - 1 ## ( we subtract 1 because even in the very beginning of the following loop, we add 1 to locationInMemory)
        
        for i in xrange(numberOfSlotsNeeded): ## stop
            try:
                locationInMemory += 1
                while self.getMemory(locationInMemory) != None:
                    locationInMemory += 1
                returnPositions += [locationInMemory]
            except SAMMemException:
                e.error(MEDIUM, 'not enough free memory! (' + len(returnPositions) + ' slots available out of ' + numberOfSlotsNeeded + ')')
        
        e.bark(MEDIUM_BARK, 'returnPositions=', returnPositions)
        return returnPositions
    
    def placeObjects(self, dictOfNamesToObjects):
        names = dictOfNamesToObjects.keys()
        objects = [dictOfNamesToObjects[key] for key in dictOfNamesToObjects.keys()]
        
        freeAddresses = self.findFreeMemory(len(objects))
        whichAddress = 0
        for name, object in zip(names, objects):            
            freeAddressToFill = freeAddresses[whichAddress]
            self.__firstFreeMemoryPosition__ = freeAddressToFill ## but not really firstFreeMemoryPosition; we'll make it so at the _end_ of the loop
            whichAddress += 1
            
            self.setMemory(freeAddressToFill, object)
            if name in self.dictOfVarsAddresses.keys():
                oldAddress = self.dictOfVarsAddresses[name]
                self.addressToReferencesDict[oldAddress].discard(name)
            self.dictOfVarsAddresses[name] = freeAddressToFill
            
            if freeAddressToFill in self.addressToReferencesDict.keys():
                self.addressToReferencesDict[freeAddressToFill].add(name)
            else:
                self.addressToReferencesDict[freeAddressToFill] = set([name])
                
        ## set __firstFreeMemoryPosition__
        for i in xrange(self.__firstFreeMemoryPosition__, len(self.memory)): ## THIS IS IMPORTANT! (but good the way it is)
            self.__firstFreeMemoryPosition__ += 1                            ## THIS IS IMPORTANT! (but good the way it is)
            if self.getMemory(self.__firstFreeMemoryPosition__ + i) == None: ## THIS IS IMPORTANT! (but good the way it is)
                break                                                        ## THIS IS IMPORTANT! (but good the way it is)
        else:                                                                ## THIS IS IMPORTANT! (but good the way it is)
            e.error(PASSABLE, 'MEMORY IS FULL!')                             ## THIS IS IMPORTANT! (but good the way it is)
    def objectsExist(self, listOfNames):
        return reduce(lambda x,y: x and y, [name in self.dictOfVarsAddresses.keys() for name in listOfNames])
    def retrieveObjects(self, listOfNames):
        rtrn = []
        for name in listOfNames:
            rtrn += [self.memory[self.dictOfVarsAddresses[name]]]
        return rtrn
    
    def deleteObject(self, addressToFree):
        self.memory[addressToFree] = None
        for name in self.addressToReferencesDict[addressToFree]:
            del self.dictOfVarsAddresses[name]
        del self.addressToReferencesDict[addressToFree]
        if addressToFree < self.__firstFreeMemoryPosition__: ## THIS IS IMPORTANT! (but good the way it is)
            self.__firstFreeMemoryPosition__ = addressToFree ## THIS IS IMPORTANT! (but good the way it is)
    
    def removeReference(self, var_name):
        if var_name in self.memory:
            address = self.dictOfVarsAddresses[var_name]
            self.addressToReferencesDict[address].discard(var_name)
            
            if self.addressToReferencesDict[address] == set([]):
                self.deleteObject(address)
        else:
            e.error(MEDIUM, 'trying to remove reference of non-existent object \'' + var_name + '\'!')
            
    def collectGarbage(self):
        for address in self.addressToReferencesDict.keys():
            if self.addressToReferencesDict[address] == set([]):
                self.deleteObject(address)


class BaseMachine(Stack, Memory):
    def __init__(self, memorySize):
        Memory.__init__(self, memorySize)
    
    def __str__(self):
        return 'Stack = ' + Stack.__str__(self) + '\n\n Memory = ' + Memory.__str__(self)


class ArithRoutines(Stack):
    num = 0
    
    def __init__(self):
        self.recordStack = []
        
        self.negate = self.unaryOperatorTemplate(lambda x: -x)
        
        self.addOp = self.binaryOperatorTemplate(lambda x,y: x+y)
        self.subOp = self.binaryOperatorTemplate(lambda x,y: y-x)
        
        self.mulOp = self.binaryOperatorTemplate(lambda x,y: x*y)
        self.divOp = self.binaryOperatorTemplate(lambda x,y: y/x)
        
        
        self.eqsOp = self.binaryOperatorTemplate(lambda x,y: x==y)
        self.neqOp = self.binaryOperatorTemplate(lambda x,y: x!=y)
        
        
        self.andOp = self.binaryOperatorTemplate(lambda x,y: x and y) ## bools _are_ ints, in a stronger sense than in Python/C++
        self.orOp = self.binaryOperatorTemplate(lambda x,y: x or y)   ## bools _are_ ints, in a stronger sense than in Python/C++
    
    def binaryOperatorTemplate(self, operator):
        def rtrn():
            self.stackPop()
            self.registerB = self.registerA
            self.stackPop()
            
            self.stackPush(operator(self.registerB, self.registerA))
        return rtrn
    def unaryOperatorTemplate(self, operator):
        def rtrn():
            self.stackPop()
            
            self.stackPush(operator(self.registerA))
        return rtrn
  
    def __str__(self):
        return 'num = ', str(self.num), \
            '\n lastNonemptyStringMatched = ' + str(self.lastNonemptyStringMatched) + '\n recordStack = ' + str(self.recordStack)
  
    def expressionError(self, string = ''):
        print 'ERROR!:', string
    
    def pushDigit(self):
        e.bark(MEDIUM_BARK, 'l', self.lastNonemptyStringMatched)
        if type(self.lastNonemptyStringMatched) == type('') and \
        len(self.lastNonemptyStringMatched) == 1:
            digit = ord(self.lastNonemptyStringMatched) - ord('0')
            if True: #self.stackLength() >= 2:
                self.num = digit + 10 * self.num 
            else:
                self.num = digit
        else:
            self.expressionError('not a digit!')
            return False
    
    def numToStack(self):
        self.stackPush(self.num)
        self.num = 0
    
    def out(self):
        if self.stackLength() >= 1:
            ans = self.stackPop()
            print 'answer:', ans
        else:
            self.expressionError('no answer!')
    
    def SAM_CODE_EVAL(self, valStr):
        if valStr[0] in '0123456789':
            return eval(valStr)
    
    def assign(self):
        value = self.stackPop()
        name = self.recordStack.pop()
        self.placeObjects({name:SAM_Object(value)})
        
    def delete(self):
        name = self.recordStack.pop()
        address = self.dictOfVarsAddresses[name]
        self.deleteObject(address)
    
    def varExists(self, name):
        return self.objectsExist([name])
        
    def useVar(self):
        name = self.recordStack.pop()
        if self.varExists(name):
            self.stackPush(self.retrieveObjects([name])[0].value)
            e.bark(HIGH_LEVEL, 'stack =', self.stack)
            #print self.stack
        else:
            return False
        
    def initList(self):
        self.stackPush([])
    def appendToList(self):
        appendMe = self.stackPop()
        appendToMe = self.stackPop()
        self.stackPush(appendToMe + [appendMe])
    def getElement(self):
        index = self.stackPop()
        myList = self.stackPop()
        self.stackPush(myList[index])
        
    def endOfStatement(self):
        self.stackReset()
        self.collectGarbage()
        
    def returnStackPop(self):
        return bool(self.stackPop())
    def returnNotStackPop(self):
        return not bool(self.stackPop())
    
    def hi(self):
        print "hi"
    
    def returnTrue(self):
        return True


class Machine(BaseMachine, ArithRoutines):
    def __init__(self, memorySize):
        BaseMachine.__init__(self, memorySize)
        ArithRoutines.__init__(self)
    
    def __str__(self):
        return 'BaseMachine = ' + BaseMachine.__str__(self) + '\n\n ArithRoutines = ' +  ArithRoutines.__str__(self)
    
    def reveal(self):
        print Memory.__str__(self)
        #print __strOfList__(self.memory)


#m = BaseMachine(10)
#v = SAM_Object()
#v.value = '3467'
#u = SAM_Object()
#u.value = 387.0
#m.placeObjects({'v': v, 'u': u})
#m.stackPush(8)
#m.stackPush(9)
#m.stackPop()
#print m
