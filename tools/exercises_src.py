"""Exercise source. Edit here, then run:  python tools/build_exercises.py
That verifies every reference solution and writes exercises.json for the app.

`tests` runs after the learner's code, in the same namespace. OUTPUT holds
everything the code printed. Assertion messages are shown to the learner.
"""

EXERCISES = []


def ex(id, topic, title, text, starter, tests, solution, stdin=""):
    EXERCISES.append(dict(id=id, topic=topic, title=title, text=text.strip(),
                          starter=starter.strip("\n") + "\n", tests=tests.strip(),
                          solution=solution.strip("\n") + "\n", stdin=stdin))


# ───────────────────────── Basics ─────────────────────────

ex("hello", "Basics", "Hello, Python!", """
`print()` shows text on the screen. Text goes inside quotes.

Print exactly: `Hello, Python!`
""", """
# Write your code below
""", """
assert OUTPUT.strip() == "Hello, Python!", f"Expected Hello, Python! but your program printed: {OUTPUT.strip()!r}"
""", """
print("Hello, Python!")
""")

ex("variables", "Basics", "Variables and f-strings", """
A variable stores a value: `city = "Tashkent"`.
An f-string puts variables inside text: `f"I live in {city}"`.

Create `name` with the value `"Ali"` and `age` with the value `20`.
Then print: `Ali is 20 years old`
""", """
name =
age =

""", """
assert name == "Ali", 'name should be "Ali"'
assert age == 20, "age should be the number 20 (no quotes)"
assert OUTPUT.strip() == "Ali is 20 years old", f"Expected: Ali is 20 years old - got: {OUTPUT.strip()!r}"
""", """
name = "Ali"
age = 20
print(f"{name} is {age} years old")
""")

ex("arithmetic", "Basics", "Arithmetic", """
Python does math with `+`, `-`, `*`, `/`.

A rectangle has `width = 7` and `height = 4`.
Store its area in `area` and its perimeter in `perimeter`.
""", """
width = 7
height = 4

area =
perimeter =
print(area, perimeter)
""", """
assert area == 28, f"area should be 28, got {area}"
assert perimeter == 22, f"perimeter should be 22, got {perimeter}"
""", """
width = 7
height = 4
area = width * height
perimeter = 2 * (width + height)
print(area, perimeter)
""")

ex("convert", "Basics", "Converting types", """
Text that looks like a number is still text. `float("2.5")` and `int("3")` turn text into numbers.

Convert the two strings to numbers and store the total cost (price x quantity) in `total`.
""", """
price_text = "19.99"
quantity_text = "3"

total =
print(total)
""", """
assert isinstance(total, float), "total should be a number (float), not text"
assert abs(total - 59.97) < 1e-6, f"total should be 59.97, got {total}"
""", """
price_text = "19.99"
quantity_text = "3"
total = float(price_text) * int(quantity_text)
print(total)
""")

ex("input", "Basics", "Reading input", """
`input()` reads one line the user types and gives it back as text.

Read a name with `input()` and print `Hello, <name>!`

When you press Run, the app types `Sara` for you, so the result should be `Hello, Sara!`
""", """
name = input("Your name: ")

""", """
assert "Hello, Sara!" in OUTPUT, f"Expected to see Hello, Sara! - your program printed: {OUTPUT!r}"
""", """
name = input("Your name: ")
print(f"Hello, {name}!")
""", stdin="Sara")

# ───────────────────────── Strings ─────────────────────────

ex("string-methods", "Strings", "String methods", """
Strings have built-in tools: `.strip()` removes spaces at both ends, `.lower()`, `.upper()`, `.title()` change the case.

Clean up `text` so that `cleaned` is `"Python Is Fun"`.
""", """
text = "   python is FUN  "

cleaned =
print(cleaned)
""", """
assert cleaned == "Python Is Fun", f'cleaned should be "Python Is Fun", got {cleaned!r}'
""", """
text = "   python is FUN  "
cleaned = text.strip().title()
print(cleaned)
""")

ex("slicing", "Strings", "Slicing", """
`word[0]` is the first letter. `word[a:b]` takes a slice from position a up to (not including) b. Negative numbers count from the end, and `word[::-1]` reverses.

From `word`, make:
- `first3` - the first three letters
- `last3` - the last three letters
- `backwards` - the whole word reversed
""", """
word = "programming"

first3 =
last3 =
backwards =
print(first3, last3, backwards)
""", """
assert first3 == "pro", f'first3 should be "pro", got {first3!r}'
assert last3 == "ing", f'last3 should be "ing", got {last3!r}'
assert backwards == "gnimmargorp", f'backwards should be "gnimmargorp", got {backwards!r}'
""", """
word = "programming"
first3 = word[:3]
last3 = word[-3:]
backwards = word[::-1]
print(first3, last3, backwards)
""")

ex("count-vowels", "Strings", "Count the vowels", """
You can loop over a string letter by letter: `for ch in text:`. Use `in` to test membership: `ch in "aeiou"`.

Write `count_vowels(text)` that returns how many vowels (a, e, i, o, u) are in the text. Upper and lower case both count.
""", """
def count_vowels(text):


print(count_vowels("Hello World"))
""", """
assert count_vowels("Hello World") == 3, f'count_vowels("Hello World") should be 3, got {count_vowels("Hello World")!r}'
assert count_vowels("AEIOU") == 5, "Upper-case vowels should count too"
assert count_vowels("rhythm") == 0, 'count_vowels("rhythm") should be 0'
assert count_vowels("") == 0, "An empty string has 0 vowels"
""", """
def count_vowels(text):
    count = 0
    for ch in text.lower():
        if ch in "aeiou":
            count += 1
    return count

print(count_vowels("Hello World"))
""")

# ───────────────────────── Conditions ─────────────────────────

ex("is-even", "Conditions", "Even or odd", """
`%` gives the remainder of a division: `7 % 2` is `1`. Comparisons like `==` give `True` or `False`.

Write `is_even(n)` that returns `True` when n is even and `False` otherwise.
""", """
def is_even(n):


print(is_even(4), is_even(7))
""", """
assert is_even(4) is True, "is_even(4) should be True"
assert is_even(7) is False, "is_even(7) should be False"
assert is_even(0) is True, "is_even(0) should be True"
assert is_even(-3) is False, "is_even(-3) should be False"
""", """
def is_even(n):
    return n % 2 == 0

print(is_even(4), is_even(7))
""")

ex("grade", "Conditions", "Letter grades", """
`if` / `elif` / `else` picks one branch. Conditions are checked top to bottom and the first true one wins.

Write `grade(score)`:
- 90 or more returns `"A"`
- 80 or more returns `"B"`
- 70 or more returns `"C"`
- anything lower returns `"F"`
""", """
def grade(score):


print(grade(85))
""", """
for score, want in [(95, "A"), (90, "A"), (89, "B"), (80, "B"), (75, "C"), (70, "C"), (69, "F"), (0, "F")]:
    got = grade(score)
    assert got == want, f"grade({score}) should be {want!r}, got {got!r}"
""", """
def grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    else:
        return "F"

print(grade(85))
""")

ex("leap-year", "Conditions", "Leap years", """
Combine conditions with `and`, `or`, `not`.

A year is a leap year if it divides by 4, except years that divide by 100 - unless they also divide by 400.
So 2024 and 2000 are leap years; 1900 and 2023 are not.

Write `is_leap(year)` that returns `True` or `False`.
""", """
def is_leap(year):


print(is_leap(2024))
""", """
for year, want in [(2024, True), (2023, False), (1900, False), (2000, True), (2100, False), (1996, True)]:
    got = is_leap(year)
    assert got == want, f"is_leap({year}) should be {want}, got {got!r}"
""", """
def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

print(is_leap(2024))
""")

# ───────────────────────── Loops ─────────────────────────

ex("sum-loop", "Loops", "Sum with a for loop", """
`range(1, 6)` gives 1, 2, 3, 4, 5 - the end number is not included.

Use a `for` loop to add up all the numbers from 1 to 100 and store the result in `total`.
""", """
total = 0

print(total)
""", """
assert total == 5050, f"total should be 5050, got {total}"
""", """
total = 0
for n in range(1, 101):
    total += n
print(total)
""")

ex("fizzbuzz", "Loops", "FizzBuzz", """
The classic. Print the numbers from 1 to 15, one per line, but:
- for multiples of 3 print `Fizz`
- for multiples of 5 print `Buzz`
- for multiples of both print `FizzBuzz`

Tip: check the "both" case first.
""", """
for n in range(1, 16):

""", """
want = ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]
got = OUTPUT.split()
assert len(got) == 15, f"Expected 15 lines, your program printed {len(got)}"
for i, (g, w) in enumerate(zip(got, want), start=1):
    assert g == w, f"Line {i} should be {w}, got {g}"
""", """
for n in range(1, 16):
    if n % 15 == 0:
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)
""")

ex("countdown", "Loops", "While loop countdown", """
A `while` loop repeats as long as its condition is true. Something inside the loop must change, or it never stops.

Print 5, 4, 3, 2, 1 (one per line) using a `while` loop, then print `Liftoff!`
""", """
n = 5

""", """
assert OUTPUT.split() == ["5", "4", "3", "2", "1", "Liftoff!"], f"Expected 5 4 3 2 1 Liftoff! on separate lines - got: {OUTPUT.split()}"
""", """
n = 5
while n > 0:
    print(n)
    n -= 1
print("Liftoff!")
""")

ex("factorial", "Loops", "Factorial", """
5! (five factorial) is 5 x 4 x 3 x 2 x 1 = 120. By definition 0! is 1.

Write `factorial(n)` using a loop. Start a result at 1 and multiply it by each number up to n.
""", """
def factorial(n):


print(factorial(5))
""", """
for n, want in [(0, 1), (1, 1), (5, 120), (10, 3628800)]:
    got = factorial(n)
    assert got == want, f"factorial({n}) should be {want}, got {got!r}"
""", """
def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

print(factorial(5))
""")

# ───────────────────────── Lists ─────────────────────────

ex("list-stats", "Lists", "List basics", """
A list holds many values: `nums = [3, 1, 2]`. Useful built-ins: `len()`, `sum()`, `min()`, `max()`.

For `numbers`, store the largest value in `biggest`, the smallest in `smallest`, and the average in `average`.
""", """
numbers = [4, 8, 15, 16, 23, 42]

biggest =
smallest =
average =
print(biggest, smallest, average)
""", """
assert biggest == 42, f"biggest should be 42, got {biggest!r}"
assert smallest == 4, f"smallest should be 4, got {smallest!r}"
assert average == 18, f"average should be 18.0, got {average!r}"
""", """
numbers = [4, 8, 15, 16, 23, 42]
biggest = max(numbers)
smallest = min(numbers)
average = sum(numbers) / len(numbers)
print(biggest, smallest, average)
""")

ex("evens-only", "Lists", "Filter a list", """
Start with an empty list `result = []` and add items with `result.append(x)`.

Write `evens_only(nums)` that returns a new list with only the even numbers, in the same order.
""", """
def evens_only(nums):


print(evens_only([1, 2, 3, 4, 5, 6]))
""", """
assert evens_only([1, 2, 3, 4, 5, 6]) == [2, 4, 6], f"evens_only([1, 2, 3, 4, 5, 6]) should be [2, 4, 6], got {evens_only([1, 2, 3, 4, 5, 6])!r}"
assert evens_only([1, 3, 5]) == [], "With no even numbers the result should be an empty list []"
assert evens_only([]) == [], "An empty list should give an empty list"
assert evens_only([0, -2, 7]) == [0, -2], "0 and negative even numbers count as even"
""", """
def evens_only(nums):
    result = []
    for n in nums:
        if n % 2 == 0:
            result.append(n)
    return result

print(evens_only([1, 2, 3, 4, 5, 6]))
""")

ex("reverse-list", "Lists", "Reverse a list", """
Write `reverse_list(items)` that returns a new list with the items in reverse order.

The original list must not be changed. (So `items.reverse()` alone is not enough - it changes the original.)
""", """
def reverse_list(items):


print(reverse_list([1, 2, 3]))
""", """
original = [1, 2, 3]
got = reverse_list(original)
assert got == [3, 2, 1], f"reverse_list([1, 2, 3]) should be [3, 2, 1], got {got!r}"
assert original == [1, 2, 3], "The original list was changed - return a new list instead"
assert reverse_list([]) == [], "An empty list reversed is an empty list"
assert reverse_list(["a", "b"]) == ["b", "a"], "It should work for text items too"
""", """
def reverse_list(items):
    return items[::-1]

print(reverse_list([1, 2, 3]))
""")

ex("second-largest", "Lists", "Second largest", """
Write `second_largest(nums)` that returns the second largest different value in the list.

For `[5, 1, 9, 9, 7]` the answer is `7` - the two 9s are the same value.
You can assume the list has at least two different numbers.
""", """
def second_largest(nums):


print(second_largest([5, 1, 9, 9, 7]))
""", """
for nums, want in [([5, 1, 9, 9, 7], 7), ([1, 2], 1), ([3, 3, 2, 2, 1], 2), ([-5, -1, -3], -3)]:
    got = second_largest(list(nums))
    assert got == want, f"second_largest({nums}) should be {want}, got {got!r}"
""", """
def second_largest(nums):
    unique = sorted(set(nums))
    return unique[-2]

print(second_largest([5, 1, 9, 9, 7]))
""")

# ───────────────────────── Functions ─────────────────────────

ex("greet", "Functions", "Default arguments", """
A parameter can have a default value: `def power(x, n=2):`. If the caller leaves it out, the default is used.

Write `greet(name, greeting="Hello")` that returns text like `Hello, Ali!`
So `greet("Ali", "Salom")` returns `Salom, Ali!`
""", """
def greet():


print(greet("Ali"))
print(greet("Ali", "Salom"))
""", """
assert greet("Ali") == "Hello, Ali!", f'greet("Ali") should return "Hello, Ali!", got {greet("Ali")!r}'
assert greet("Ali", "Salom") == "Salom, Ali!", f'greet("Ali", "Salom") should return "Salom, Ali!", got {greet("Ali", "Salom")!r}'
""", """
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Ali"))
print(greet("Ali", "Salom"))
""")

ex("palindrome", "Functions", "Palindromes", """
A palindrome reads the same forwards and backwards, like "level".

Write `is_palindrome(text)` that returns `True` or `False`. Ignore upper/lower case and ignore spaces, so `"Never odd or even"` is a palindrome.
""", """
def is_palindrome(text):


print(is_palindrome("Never odd or even"))
""", """
for text, want in [("level", True), ("Level", True), ("Never odd or even", True), ("python", False), ("", True), ("ab", False)]:
    got = is_palindrome(text)
    assert got == want, f"is_palindrome({text!r}) should be {want}, got {got!r}"
""", """
def is_palindrome(text):
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]

print(is_palindrome("Never odd or even"))
""")

ex("fibonacci", "Functions", "Fibonacci", """
The Fibonacci sequence starts 0, 1 and each next number is the sum of the two before it: 0, 1, 1, 2, 3, 5, 8, ...

Write `fibonacci(n)` that returns a list with the first n Fibonacci numbers.
`fibonacci(6)` returns `[0, 1, 1, 2, 3, 5]`.
""", """
def fibonacci(n):


print(fibonacci(6))
""", """
for n, want in [(0, []), (1, [0]), (2, [0, 1]), (6, [0, 1, 1, 2, 3, 5]), (10, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])]:
    got = fibonacci(n)
    assert got == want, f"fibonacci({n}) should be {want}, got {got!r}"
""", """
def fibonacci(n):
    result = []
    a, b = 0, 1
    for _ in range(n):
        result.append(a)
        a, b = b, a + b
    return result

print(fibonacci(6))
""")

# ───────────────────────── Dictionaries ─────────────────────────

ex("dict-basics", "Dictionaries", "Dictionary basics", """
A dictionary maps keys to values: `d = {"a": 1}`. Read with `d["a"]`, add or change with `d["b"] = 2`.

1. Create `student` with `"name"` set to `"Malika"` and `"age"` set to `19`.
2. Then add a new key `"city"` with the value `"Samarkand"`.
3. Then increase the age by 1.
""", """
student =

print(student)
""", """
assert isinstance(student, dict), "student should be a dictionary"
assert student.get("name") == "Malika", 'student["name"] should be "Malika"'
assert student.get("city") == "Samarkand", 'student["city"] should be "Samarkand"'
assert student.get("age") == 20, f'student["age"] should be 20 after adding 1, got {student.get("age")!r}'
""", """
student = {"name": "Malika", "age": 19}
student["city"] = "Samarkand"
student["age"] += 1
print(student)
""")

ex("word-count", "Dictionaries", "Count words", """
`sentence.split()` breaks text into a list of words. `d.get(key, 0)` reads a value, or gives 0 when the key is missing.

Write `word_count(sentence)` that returns a dictionary of how many times each word appears. Treat upper and lower case as the same word (use lower case keys).
""", """
def word_count(sentence):


print(word_count("the cat and the hat"))
""", """
got = word_count("the cat and the hat")
assert got == {"the": 2, "cat": 1, "and": 1, "hat": 1}, f"Wrong counts for 'the cat and the hat': {got!r}"
got = word_count("Go go GO")
assert got == {"go": 3}, f"'Go go GO' should give {{'go': 3}}, got {got!r}"
assert word_count("") == {}, "An empty sentence should give an empty dictionary"
""", """
def word_count(sentence):
    counts = {}
    for word in sentence.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts

print(word_count("the cat and the hat"))
""")

ex("most-expensive", "Dictionaries", "Loop over a dictionary", """
`for key, value in d.items():` walks through every pair.

Write `most_expensive(prices)` that takes a dictionary of item names and prices and returns the name of the most expensive item.
""", """
def most_expensive(prices):


print(most_expensive({"tea": 3, "plov": 12, "bread": 2}))
""", """
got = most_expensive({"tea": 3, "plov": 12, "bread": 2})
assert got == "plov", f'Expected "plov", got {got!r}'
got = most_expensive({"a": 1})
assert got == "a", f'With one item it should return that item, got {got!r}'
got = most_expensive({"x": -5, "y": -2})
assert got == "y", f'It should work with negative prices too, got {got!r}'
""", """
def most_expensive(prices):
    best_name = None
    best_price = None
    for name, price in prices.items():
        if best_price is None or price > best_price:
            best_name = name
            best_price = price
    return best_name

print(most_expensive({"tea": 3, "plov": 12, "bread": 2}))
""")

# ───────────────────────── Tuples & sets ─────────────────────────

ex("unique-sorted", "Tuples & sets", "Remove duplicates", """
A `set` keeps only unique values: `set([1, 1, 2])` is `{1, 2}`. `sorted()` returns a sorted list from any collection.

Write `unique_sorted(nums)` that returns a sorted list with duplicates removed.
""", """
def unique_sorted(nums):


print(unique_sorted([3, 1, 3, 2, 1]))
""", """
got = unique_sorted([3, 1, 3, 2, 1])
assert got == [1, 2, 3], f"unique_sorted([3, 1, 3, 2, 1]) should be [1, 2, 3], got {got!r}"
assert isinstance(got, list), "Return a list, not a set"
assert unique_sorted([]) == [], "An empty list should give an empty list"
""", """
def unique_sorted(nums):
    return sorted(set(nums))

print(unique_sorted([3, 1, 3, 2, 1]))
""")

ex("min-max", "Tuples & sets", "Return two values", """
A function can return several values at once as a tuple: `return a, b`. The caller can unpack them: `low, high = f()`.

Write `min_max(nums)` that returns the smallest and the largest number as a tuple `(smallest, largest)`.
""", """
def min_max(nums):


low, high = min_max([4, 9, 2, 7])
print(low, high)
""", """
got = min_max([4, 9, 2, 7])
assert tuple(got) == (2, 9), f"min_max([4, 9, 2, 7]) should be (2, 9), got {got!r}"
assert tuple(min_max([5])) == (5, 5), "With one number, both values are that number"
""", """
def min_max(nums):
    return min(nums), max(nums)

low, high = min_max([4, 9, 2, 7])
print(low, high)
""")

# ───────────────────────── Comprehensions ─────────────────────────

ex("squares", "Comprehensions", "List comprehension", """
A list comprehension builds a list in one line: `[n * 2 for n in range(5)]` gives `[0, 2, 4, 6, 8]`.

Use one to make `squares`: the squares of the numbers 1 to 10.
""", """
squares =
print(squares)
""", """
assert squares == [1, 4, 9, 16, 25, 36, 49, 64, 81, 100], f"squares should be [1, 4, 9, ..., 100], got {squares!r}"
""", """
squares = [n * n for n in range(1, 11)]
print(squares)
""")

ex("long-words", "Comprehensions", "Comprehension with a filter", """
Add an `if` at the end to keep only some items: `[x for x in items if x > 0]`.

Write `long_words(words, n)` that returns the words longer than n letters, in upper case.
""", """
def long_words(words, n):


print(long_words(["sun", "planet", "moon", "galaxy"], 4))
""", """
got = long_words(["sun", "planet", "moon", "galaxy"], 4)
assert got == ["PLANET", "GALAXY"], f'Expected ["PLANET", "GALAXY"], got {got!r}'
assert long_words(["a", "bb"], 5) == [], "When no word is long enough, return an empty list"
assert long_words(["abc"], 2) == ["ABC"], 'long_words(["abc"], 2) should be ["ABC"]'
""", """
def long_words(words, n):
    return [w.upper() for w in words if len(w) > n]

print(long_words(["sun", "planet", "moon", "galaxy"], 4))
""")

# ───────────────────────── Errors ─────────────────────────

ex("safe-divide", "Errors", "try / except", """
Dividing by zero raises `ZeroDivisionError` and stops the program. `try:` / `except ZeroDivisionError:` lets you catch it and carry on.

Write `safe_divide(a, b)` that returns `a / b`, or `None` when b is zero. Use try/except.
""", """
def safe_divide(a, b):


print(safe_divide(10, 2))
print(safe_divide(1, 0))
""", """
assert safe_divide(10, 2) == 5, f"safe_divide(10, 2) should be 5.0, got {safe_divide(10, 2)!r}"
assert safe_divide(1, 0) is None, f"safe_divide(1, 0) should be None, got {safe_divide(1, 0)!r}"
assert safe_divide(0, 5) == 0, "safe_divide(0, 5) should be 0.0"
""", """
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

print(safe_divide(10, 2))
print(safe_divide(1, 0))
""")

ex("to-int", "Errors", "Catching bad input", """
`int("abc")` raises `ValueError`.

Write `to_int(text, default=0)` that returns the text converted to an integer, or `default` when the text is not a valid whole number.
""", """
def to_int(text, default=0):


print(to_int("42"), to_int("abc"), to_int("x", -1))
""", """
assert to_int("42") == 42, f'to_int("42") should be 42, got {to_int("42")!r}'
assert to_int("abc") == 0, f'to_int("abc") should be 0, got {to_int("abc")!r}'
assert to_int("x", -1) == -1, 'to_int("x", -1) should return the default, -1'
assert to_int(" 7 ") == 7, 'to_int(" 7 ") should be 7'
""", """
def to_int(text, default=0):
    try:
        return int(text)
    except ValueError:
        return default

print(to_int("42"), to_int("abc"), to_int("x", -1))
""")

# ───────────────────────── Classes ─────────────────────────

ex("dog-class", "Classes", "Your first class", """
A class bundles data and functions. `__init__` runs when you create an object, and `self` is the object itself.

Write a class `Dog`:
- `Dog("Rex")` stores the name in `self.name`
- `.bark()` returns the text `Rex says Woof!` (with that dog's name)
""", """
class Dog:
    def __init__(self, name):


rex = Dog("Rex")
print(rex.bark())
""", """
d = Dog("Rex")
assert d.name == "Rex", "Dog('Rex').name should be 'Rex'"
assert d.bark() == "Rex says Woof!", f'bark() should return "Rex says Woof!", got {d.bark()!r}'
assert Dog("Bobik").bark() == "Bobik says Woof!", "bark() should use each dog's own name"
""", """
class Dog:
    def __init__(self, name):
        self.name = name

    def bark(self):
        return f"{self.name} says Woof!"

rex = Dog("Rex")
print(rex.bark())
""")

ex("bank-account", "Classes", "Bank account", """
`raise ValueError("message")` signals an error on purpose.

Write a class `BankAccount`:
- starts with `balance` of 0
- `.deposit(amount)` adds to the balance
- `.withdraw(amount)` subtracts from the balance, but raises `ValueError` if the amount is more than the balance
""", """
class BankAccount:


acc = BankAccount()
acc.deposit(100)
acc.withdraw(30)
print(acc.balance)
""", """
a = BankAccount()
assert a.balance == 0, "A new account should have balance 0"
a.deposit(100)
assert a.balance == 100, f"After deposit(100) balance should be 100, got {a.balance!r}"
a.withdraw(30)
assert a.balance == 70, f"After withdraw(30) balance should be 70, got {a.balance!r}"
try:
    a.withdraw(500)
except ValueError:
    pass
else:
    raise AssertionError("withdraw(500) with only 70 in the account should raise ValueError")
assert a.balance == 70, "A failed withdrawal must not change the balance"
b = BankAccount()
assert b.balance == 0, "Each account needs its own balance - set it in __init__ with self.balance"
""", """
class BankAccount:
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Not enough money")
        self.balance -= amount

acc = BankAccount()
acc.deposit(100)
acc.withdraw(30)
print(acc.balance)
""")

# ───────────────────────── Challenges ─────────────────────────

ex("is-prime", "Challenges", "Prime numbers", """
A prime number is greater than 1 and divides evenly only by 1 and itself: 2, 3, 5, 7, 11, ...

Write `is_prime(n)` that returns `True` or `False`.
""", """
def is_prime(n):


print([n for n in range(20) if is_prime(n)])
""", """
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
for n in range(-2, 50):
    got = is_prime(n)
    want = n in primes
    assert got == want, f"is_prime({n}) should be {want}, got {got!r}"
assert is_prime(7919) is True, "is_prime(7919) should be True"
""", """
def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

print([n for n in range(20) if is_prime(n)])
""")

ex("anagrams", "Challenges", "Anagrams", """
Two words are anagrams when they use exactly the same letters, like "listen" and "silent".

Write `are_anagrams(a, b)` that returns `True` or `False`. Ignore upper/lower case and spaces.
""", """
def are_anagrams(a, b):


print(are_anagrams("listen", "silent"))
""", """
for a, b, want in [("listen", "silent", True), ("Listen", "Silent", True), ("dormitory", "dirty room", True),
                   ("hello", "world", False), ("aab", "abb", False), ("abc", "abcd", False)]:
    got = are_anagrams(a, b)
    assert got == want, f"are_anagrams({a!r}, {b!r}) should be {want}, got {got!r}"
""", """
def are_anagrams(a, b):
    def clean(s):
        return sorted(s.lower().replace(" ", ""))
    return clean(a) == clean(b)

print(are_anagrams("listen", "silent"))
""")

ex("caesar", "Challenges", "Caesar cipher", """
A Caesar cipher shifts every letter forward in the alphabet. With a shift of 3, `a` becomes `d` and `z` wraps around to `c`.

`ord("a")` gives a letter's number and `chr(number)` turns it back into a letter.

Write `caesar(text, shift)` that shifts lower-case letters a-z and leaves every other character unchanged.
`caesar("hello, world", 3)` returns `khoor, zruog`.
""", """
def caesar(text, shift):


print(caesar("hello, world", 3))
""", """
assert caesar("abc", 1) == "bcd", f'caesar("abc", 1) should be "bcd", got {caesar("abc", 1)!r}'
assert caesar("xyz", 3) == "abc", f'caesar("xyz", 3) should wrap around to "abc", got {caesar("xyz", 3)!r}'
assert caesar("hello, world", 3) == "khoor, zruog", f'caesar("hello, world", 3) should be "khoor, zruog", got {caesar("hello, world", 3)!r}'
assert caesar(caesar("python", 5), -5) == "python", "Shifting by 5 and then by -5 should give back the original text"
""", """
def caesar(text, shift):
    result = ""
    for ch in text:
        if "a" <= ch <= "z":
            result += chr((ord(ch) - ord("a") + shift) % 26 + ord("a"))
        else:
            result += ch
    return result

print(caesar("hello, world", 3))
""")
