FuncRegex
=========



This is a slice of an (interpreter-maker)-making project I started in summer 2011.


************
*Why a slice?*


I never finished it.
Indeed, there's always more to add. Later versions contain bugs I haven't conquered
(for, given school and a host of other, recently developed interests (chess algorithms!!), I haven't since had time)
Thus, to make this repository I pruned away the bug-infested new growth,
leaving a core that I hope captures the main features of the program.


************
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
when it recognizes `<digit>` by recognizing `<digitList>`. `pushDigit` isn't a syntax-specification; it is a
method that multiplies the top of the stack by 10, then adds the digit just read.
`pushDigit` can see the current state of the parser.
It's useful, see?

(`pushDigit` and other parser-called methods are defined in "SAM\_CODE\_FuncContaining_Class.py)

After describing how to recognize whitespace, numerical digits, etc.,
we proceed to describe expressions of arithmetic. A powerful feature of FuncRegex is that language-
definition is allowed to be _recursive_! Here's one more excerpt from "THE_USE.py", showing recursion:

`unit = '(("+"|"-"<negate>)?)(("("<expression>")")|(($(""<digitList>)""<digits>)|(""<list>)|($(""<alphabetList>)""<variable>)))""<whitespace>'`

...

... (lots of intermediate definitions, for lists, multiplication, addition, logic)

... To simplify, term := product of units; arithmetic expression := sum of terms; orExp = arith. expr.s combined by "or".

...

`expression = '""<orExp>'`

OK, the definition of `<unit>` is a bit long. It handles expressions like "8", and "-42", and "mylist[255]".
But it also handles "(8 * -42 == my_list[255])"! This is because recognizing an `<expression>`, enclosed by parens,
suffices to recognize `<unit>`. If not for recursion, `<expression>` could recognize "1\*2 + 3\*4" but not "1\*(2+3)\*4".

Note: there's a problem with our approach, namely that we don't want to
indiscriminately evaluate the bodies of if-statements, etc. One solution is to lazily evaluate arguments to the
parser-called methods. I had begun but not finished this feature when school started / I got distracted by other projects. 

This concludes our tour of language-specification. Let's try out the calculator we built!

************
*Ouput of Example (Calculator Language)*

> please enter an expression
> a = 7

> please enter an expression
> print a
> answer: 7

> please enter an expression
> print 1*(2+3)*4
> answer: 20

_It works!_

The compact language-specification language allows modular language-specifications, and easy modification.
We added a list feature to the language by modifying the language-spec, and by 
writing some functions for the parser to call. (Repository contains modified files.)

> please enter an expression
> mylist = [3 1 4 1 5 9 2 6]

> please enter an expression
> print mylist[4]
> answer: 5

> please enter an expression
> print mylist[4]==6
> answer: False

> please enter an expression
> print mylist[4]+mylist[5]
> answer: 14

_Super!_

************
*How is the progam organized?*

Utility functions:
> "ErrorFileClass.py"
> "SettingsHeader.py"

Parser of Language-Specification Language (would have been cool to bootstrap :D ... didn't):
> "RegexCompilerClass.py"

The _meat_ --- describes how to combine two parsers P and Q into "P or Q", "P then Q", "P*", etc.:
> "RegexTokenizerClass.py"

Wraps string class, catalyzing digestion by FuncRegex:
> "TextClass.py"
> "TextSkipperClass.py"

Data structures to contain parser state/output:
> "TokenClass.py"
> "TokenListClass.py"
And to tokenize:
> "TokenizerClass.py"
> "SymbolsClass.py"

Putting it all together:
> "FunctionRegexLibrary.py"

Calculator Example:
> "THE_USE.py" --- language specification
> "SAM\_CODE\_FuncContaining_Class.py" --- virtual machine; parser-called metods
Defines "doing nothing":
> "FuncHeader.py"
