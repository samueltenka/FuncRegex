FuncRegex
=========



This is a slice of an (interpreter-maker)-making project I started in summer 2012.



*Why a slice?*

I never finished it.
Indeed, there's always more to add. Later versions contain bugs I haven't conquered
(for, given school & a host of recently developed interests (chess algorithms!!), I haven't had time)
Thus, to make this repository I pruned away the bug-infested new growth,
leaving a core that I hope captures the main features of the program.



*What does the program do?*

It lets a programmer specify a language, and then creates an interpreter for the language.

A simple example of use is given in "THE_USE.py", in which we specify a calculator:
For example, `whitespace = '((" ")*)'` defines whitespace to be 0 or more spaces.
Similarly (don't worry about `pushDigit`, `numToStack` yet),

`digitList = '"0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"'` says that a `<digitList>` is "0", or "1", or "2", etc.;

`digit = '""<digitList>""<pushDigit>'`: a `<digit>` is just a `<digitLists>`;

`digits = '(($(""<digitList>)""<digit>)+)(""<numToStack>)'`: and a `<digits>` is a sequence of 1 or more digits.

The specification language is like standard regular expression languages.
Now, what makes FuncRegex _different_ from other tools is that we can specify
what action an interpreter should take given a certain parse tree, at the same time we describe
the possible tree structures! In this case, we specify that the parser perform `pushDigit`
when it recognizes `<digit>` by recognizing `<digitList>`. See? (`pushDigit` is defined in "SAM_CODE_FuncContaining_Class.py").

We build up our language this way. After describing how to recognize
whitespace, numerical digits, identifiers, etc., we proceed to define arithmetic operations:



*How is the progam organized?*


