'''
Created on Jun 27, 2011

@author: Sam
'''

## debugOn
debugOn = True


## bark message
barkMessage = ' '
barkSpacer = '  '
barkIndent =  '    '
pauseMessage = '__PAUSED__ '

## bark levels
TO_USER = ALL_THE_TIME = 0
ALMOST_ALL_THE_TIME = -1
HIGH_LEVEL = GENERAL_BUG = -2
ENTER_OR_EXIT_FUNCTION = -3
MEDIUM_BARK = STATE_OF_HIGH_LEVEL_FUNCTION = -4
LOW_LEVEL = SPECIFIC_BUG = -5
LOWEST_LEVEL = -6


## error message
errorMessage = 'error!\n\t'

## errorFile name
errorFileName = 'sam_code_error.txt'

## error levels
OKAY = 0
PASSABLE = 1
MEDIUM = 2
FATAL = 3
