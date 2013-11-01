FuncRegex
=========



This is a slice of an (interpreter-maker)-making project I started in summer 2011. I worked in Python (2.7). 



**Why a slice?**

I never finished it. 
Indeed, there's always more to add. Later versions contain bugs I haven't conquered
(for, given school and a host of other, recently developed interests (chess algorithms!!), I haven't since had time)
Thus, to make this repository I pruned away the bug-infested new growth,
leaving a core that I hope captures the main features of the program.



**What does the program do?**

It lets a programmer specify a language, and then creates an interpreter for the language.

A simple example of use is given in "THE_USE.py", in which we specify a calculator:
For example, `whitespace = '((" ")*)'` defines whitespace to be 0 or more spaces.
Similarly (don't worry about `pushDigit`, `numToStack` yet),

* `digitList = '"0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"'` says that a `<digitList>` is "0", or "1", or "2", etc.;
* `digit = '""<digitList>""<pushDigit>'`: a `<digit>` is just a `<digitList>`;
* `digits = '(($(""<digitList>)""<digit>)+)(""<numToStack>)'`: and a `<digits>` is a sequence of 1 or more digits.

The specification language is like standard regular expression languages.
Now, what makes FuncRegex **different** from other tools is that we can specify
what action an interpreter should take given a certain parse tree, at the same time we describe
the possible tree structures! In this case, we specify that the parser perform `pushDigit`
when it recognizes `<digit>` by recognizing `<digitList>`. `pushDigit` isn't a syntax-specification; it is a
method that multiplies a certain "register" of the Calculator by 10, then adds the digit just read.
`pushDigit` can see the current state of the parser.
Similarly, `numToStack` pushes the register;s value onto the stack.

Thus we embed actions into our specification; each language feature's syntax and function are in the same place,
which is elegant. Embedding is useful, see?

(`pushDigit` and other parser-called methods are defined in "SAM\_CODE\_FuncContaining_Class.py)

After describing how to recognize whitespace, numerical digits, etc.,
we proceed to describe expressions of arithmetic. A powerful feature of FuncRegex is that language-definition
is allowed to be **recursive**! Here's one more excerpt from "THE_USE.py", showing (in this case indirect) recursion:

    unit = '(("+"|"-"<negate>)?)(("("<expression>")")|(($(""<digitList>)""<digits>)|(""<list>)|($(""<alphabetList>)""<variable>)))""<whitespace>'
    ...
    ... (lots of intermediate definitions, for lists, multiplication, addition, logic)
    ... To simplify, term := product of units; arithmetic expression := sum of terms; orExp = arith. expr.s combined by "or".
    ...
    expression = '""<orExp>'

OK, the definition of `<unit>` is a bit long. It handles expressions like "8", and "-42", and "mylist[255]".
But it also handles "(8 * -42 == my_list[255])"! This is because recognizing an `<expression>`, enclosed by parens,
suffices to recognize `<unit>`. If not for recursion, `<expression>` could recognize "1\*2 + 3\*4" but not "1\*(2+3)\*4".

Note: there's a **problem** with our approach, namely that we don't want to
indiscriminately evaluate the bodies of if-statements, etc. One solution is to lazily evaluate arguments to the
parser-called methods. I had begun but not finished this feature when school started / I got distracted by other projects. 

This concludes our tour of language-specification. Let's try out the calculator we built!




**Output of Example (Calculator Language)**

Our calculator language allows us to define and use variables:

    please enter an expression
    a = 7
    please enter an expression
    print a
    answer: 7
    please enter an expression

And to calculate:

    print 1*(2+3)*4 + a
    answer: 27

_It works!_

The compact language-specification language allows modular language-specifications, and easy modification.
To add a list feature to the calculator language, all we had to do was add a few lines to the language-spec, and
write some functions for the parser to call. The linking of functions to syntax was automatic. (Repository contains modified files.)

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

_Utility functions_:

"ErrorFileClass.py"

"SettingsHeader.py"

_Parser of Language-Specification Language_ (would have been cool to bootstrap :D ... didn't):

"RegexCompilerClass.py"

The _meat_ --- _describes how to combine two parsers P and Q into "P or Q", "P then Q", "P*", etc._:

"RegexTokenizerClass.py"

_Wraps string class, catalyzing digestion by FuncRegex_:

"TextClass.py"

"TextSkipperClass.py"

_Data structures to contain parser state/output_:

"TokenClass.py"

"TokenListClass.py"

_And to tokenize_:

"TokenizerClass.py"

"SymbolsClass.py"

_Putting it all together_:

"FunctionRegexLibrary.py"

_Calculator Example_:

"THE_USE.py" --- language specification

"SAM\_CODE\_FuncContaining_Class.py" --- virtual machine; parser-called metods

_Defines "doing nothing"_:

"FuncHeader.py"
