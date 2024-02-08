
[![Unit tests](https://github.com/MarcoMeijer/ppythonp/actions/workflows/python-app.yml/badge.svg)](https://github.com/MarcoMeijer/ppythonp/actions/workflows/python-app.yml)

# +python+

+python+ is an improved version of python.
Just like c++ is an improvement of c,
Kotlin is an improvement of Java,
Typescript is an improvement of Javascript,
and php is an improvement of html.

## The Zen of Python

The language tries to improve python based on "The Zen of Python".

```
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```

Lets go over how +python+ improves on some of these:

### "There should be one-- and preferably only one --obvious way to do it."

The number one requested feature for python is the ++ and -- operator.
The reason that they never added it is obviously because of this rule.
Because where would you put it? Before or after the variable name?
This is something c++/++c developers love to argue about.
Thats why in +python+, to increment a variable you put a plus before AND after the variable name like this:

```py
i = 0
+i+
print(i) # prints 1
```

This is also where +python+ got its name from.

### "Beatiful is better than ugly."

Is there anything more beatifull then the golden ratio?
Thats why in +python+ the indentation increases based on the fibonacci sequence:

```py
x = 0
if x < 10:
 while x < 10:
  x += 1
  if x == 6:
   for i in range(10):
     if i % 2 == 0:
        for j in range(i):
             print(i)
```

### Readability counts.

Many new users of python are confused by the "def" keyword,
because they don't know what the abreviation means.
Thats why in +python+ we removed that abreviation:

```py
definitely f(x):
 return x + 1

print(f(10)) # prints 11
```

This will make the code more readible to people not familiar with +python+.

### "Flat is better than nested."

Everyone knows the pain of having multiple nested for loops.
Thats why +python+ adds an alternative to loops that doesn't require nesting: The reverse variable.
This is a builtin variable that allows you to reverse the direction of the code.
Here is an example to print the numbers from 0 to 10 using the reverse operator

```py
i = 0
if reverse:
 reverse = false
if reverse == false:
 print(i)
 +i+
if i < 10:
 reverse = true
```

And here is an example to print 3 times the numbers from 0 to 10 without any nesting.

```py
i = 0
if reverse:
 reverse = false
j_loop = true
j = 0
if j_loop and reverse:
 reverse = false
if j_loop and reverse == false:
 print(j)
 +j+
if j_loop and j < 10:
 reverse = true
j_loop = false
if reverse == false:
 +i+
if i < 3:
 reverse = true
```

As you can see this is much better then nested for loops.

### "Explicit is better than implicit."

As a fulltime javascript developer I strongly agree with this statement.
It is way better if you have to explicitely tell the language that you want to compare if the types are also equal.
So in +python+ types are automatically converted, unless explicitely told not to.
So the == operator does type coercion, while the === operator works the same as the normal python == operator.
If you want to test if two objects are pointing to the same memory address use the ==== operator.

```py
x = 1
y = "1"
if x == y: # this is true
 print("x == y")
if x === y: # this is not true
 print("x === y")

a = [1, 2]
b = [1, 2]
if a === b: # this is true
 print("a === b")
if a ==== b: # this is not true
 print("a === b")
a = b
if a ==== b: # this is true
 print("a ==== b")
```

For addition it will convert both of the variables to a string, unless explicitely told not to do that.
If you want to get an error when adding an int to a string, use the ++ operator.

```py
print(1 + "2") # prints 12
print("1" ++ "2") # prints 12
print(1 ++ "2") # crashes the program
```

### "Errors should never pass silently. Unless explicitly silenced."

Any time an error is raised it will play a sound.
This will make sure the programmer is aware of the error.
This also applies to compile errors.
The only way to stop the sound is to type stop in the console.


## Python api improvements

### range

Normally in python you can pass at most 3 arguments to the range function.
But in +python+ you can pass an infinite amount.
Normally if you have three arguments, the third argument specifies the change after each iteration.

```py
# prints the numbers 0, 2, 4, 6, 8
for i in range(0,10,2):
 print(i)
```

But if you pass a fourth argument, it will increment the third argument each iteration:
```py
# prints the numbers 0, 2, 5, 9
for i in range(0,10,2,1):
 print(i)
```

This pattern continues with all the other arguments:
```py
# print the numbers 0, 2, 10, 27, 57, 111, 213, 406, 758, 1368, 2372, 3949, 6327, 9789
for i in range(0,10000,2,6,3,1,6):
 print(i)
```

You are probably wondering why this is useful.

## How to run

You first need to have python 3.12 installed on your system.
Then you can execute code by running the ppythonp script like this: `./ppythonp [filename]`.
For example try running `./ppythonp example.ppp`.

## Full feature list

- integers
- strings
- lists
- printing
- list indexing
- if statements
- if else statements
- while loops
- for loops
- functions
- recursion
- comparisons
- bitwise operators
- binary logic operators
- increment operator
- reversing code direction
