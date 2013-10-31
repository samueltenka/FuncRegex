FuncRegex
=========



This is a slice of an (interpreter-maker)-making project I started in summer 2012.



_Why a slice?_

I never finished it.
Indeed, there's always more to add. Later versions contain bugs I haven't conquered
(for, given school & a host of recently developed interests (chess algorithms!!), I haven't had time)
Thus, to make this repository I pruned away the bug-infested new growth,
leaving a core that I hope captures the main features of the program.



_What does the program do?_

It lets a programmer specify a language, and then creates an interpreter for the language.

A _simple example_ of use is given in `THE_USE.py`, in which we specify a _calculator_:
For example, `whitespace = '((" ")*)'` defines whitespace to be 0 or more spaces.
Similarly (don't worry about `pushDigit`, `numToStack` yet),
`digitList = '"0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"'`     says in that a <digitList> is "0", or "1", or "2", etc.;
`digit = '""<digitList>""<pushDigit>'`                      a <digit> is just a <digitLists>;
`digits = '(($(""<digitList>)""<digit>)+)(""<numToStack>)'` and a <digits> is a sequence of 1 or more digits.
The specification-language is like standard regular expressions.
Now, what makes FuncRegex _different_ 

We build up our language this way. After describing how to recognize
whitespace, numerical digits, identifiers, etc., we proceed to define arithmetic operations:



_How is the progam organized?_


