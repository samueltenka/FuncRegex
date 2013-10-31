FuncRegex
=========



This is a slice of an (interpreter-maker)-making project I started in summer 2012.



Why a slice?

I never finished it.
Indeed, there's always more to add. Later versions contain bugs I haven't conquered
(for, given school & a host of recently developed interests (chess algorithms!!), I haven't had time)
Thus, to make this repository I pruned away the bug-infested new growth,
leaving a core that I hope captures the main features of the program.



What does the program do?

It lets a programmer specify a language, and then creates an interpreter for the language.
A simple example of use is given in `THE_USE.py`, in which we specify a calculator:
For example, `whitespace = '((" ")*)'` defines whitespace to be 0 or more spaces.
We build up our language this way. After describing how to recognize
whitespace, numerical digits, identifiers, etc., we proceed to define
`digits = '(($(""<digitList>)""<digit>)+)(""<numToStack>)'`



How is the progam organized?


