## +python+

+python+ is an improved version of python.
Just like Kotlin is an improvement of Java,
Typescript is an improvement of Javascript,
and php is an improvement of html.

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

13. There should be one-- and preferably only one --obvious way to do it.

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

1. Beatiful is better than ugly.

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

7. Readability counts.

Many new users of python are confused by the "def" keyword,
because they don't know what the abreviation means.
Thats why in +python+ we removed that abreviation:

```py
definitely f(x):
    return x + 1

print(f(10)) # prints 11
```

This will make the code more readible to people not familiar with +python+.

5. Flat is better than nested.

Everyone knows the pain of having multiple nested for loops.
Thats why +python+ adds an alternative to loops that doesn't require nesting: The reverse operator.
It allows you to reverse the direction of the code.
Here is an example to print the numbers from 0 to 10 using the reverse operator

```py
i = 0
if i != 0:
    reverse
print(i)
+i+
if i < 10:
    reverse
```

And here is an example to find all pairs of numbers between 0 and 10 whose sum is even without any nesting:

```py
res = []
i = 0
if i != 0:
    reverse
j = 0
if j != 0:
    reverse
if (i + j) % 2 == 0:
    print(i + "," + j)
+j+
if j < 10:
    reverse
j = -1
+i+
if i < 10:
    reverse
```

As you can see this is much better then nested for loops.

10. Errors should never pass silently.
11. Unless explicitly silenced.

Any time an error is raised it will play a sound.
This will make sure the programmer is aware of the error.
This also applies to compile errors.
The only way to stop the sound is to type stop in the console.

