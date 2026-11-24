"""Second batch of exercises, including the harder logic ones.
Same format as exercises_src.py. level: 1 = easy, 2 = medium, 3 = hard."""
from exercises_src import ex

# ───────────────────────── Basics ─────────────────────────

ex("swap", "Basics", "Swap two variables", """
Python can assign several variables at once: `x, y = 1, 2`. The right side is worked out first, so `x, y = y, x` swaps them.

Swap the values of `a` and `b` without typing the numbers again.
""", """
a = 5
b = 9

print(a, b)
""", """
assert a == 9 and b == 5, f"After swapping, a should be 9 and b should be 5 - got a={a!r}, b={b!r}"
""", """
a = 5
b = 9
a, b = b, a
print(a, b)
""")

ex("temperature", "Basics", "Celsius to Fahrenheit", """
The formula is: fahrenheit = celsius x 9 / 5 + 32.

Store the Fahrenheit value of `celsius` in `fahrenheit`.
""", """
celsius = 25

fahrenheit =
print(fahrenheit)
""", """
assert abs(fahrenheit - 77) < 1e-9, f"25 C should be 77.0 F, got {fahrenheit!r}"
""", """
celsius = 25
fahrenheit = celsius * 9 / 5 + 32
print(fahrenheit)
""")

ex("time-parts", "Basics", "Hours, minutes, seconds", """
`//` divides and throws away the remainder: `7 // 2` is `3`. `%` gives only the remainder: `7 % 2` is `1`.

Split `total_seconds` into `hours`, `minutes` and `seconds`.
3725 seconds is 1 hour, 2 minutes, 5 seconds.
""", """
total_seconds = 3725

hours =
minutes =
seconds =
print(hours, minutes, seconds)
""", """
assert hours == 1, f"hours should be 1, got {hours!r}"
assert minutes == 2, f"minutes should be 2, got {minutes!r}"
assert seconds == 5, f"seconds should be 5, got {seconds!r}"
""", """
total_seconds = 3725
hours = total_seconds // 3600
minutes = total_seconds % 3600 // 60
seconds = total_seconds % 60
print(hours, minutes, seconds)
""")

# ───────────────────────── Strings ─────────────────────────

ex("initials", "Strings", "Initials", """
`"a b".split()` gives `["a", "b"]`, and `".".join(["A", "B"])` gives `"A.B"`.

Write `initials(full_name)` that returns the first letter of every word, in upper case, each followed by a dot.
`initials("ali valiyev")` returns `A.V.`
""", """
def initials(full_name):


print(initials("ali valiyev"))
""", """
for name, want in [("ali valiyev", "A.V."), ("Guido van Rossum", "G.V.R."), ("ada", "A.")]:
    got = initials(name)
    assert got == want, f"initials({name!r}) should be {want!r}, got {got!r}"
""", """
def initials(full_name):
    result = ""
    for word in full_name.split():
        result += word[0].upper() + "."
    return result

print(initials("ali valiyev"))
""")

ex("strong-password", "Strings", "Strong password", """
Characters can be tested with `.isdigit()`, `.isupper()` and `.islower()`. `any(...)` is True when at least one item is True.

Write `is_strong(password)` that returns `True` only when the password:
- has at least 8 characters
- contains at least one digit
- contains at least one upper-case letter
- contains at least one lower-case letter
""", """
def is_strong(password):


print(is_strong("Python2024"))
""", """
for pw, want in [("Python2024", True), ("python2024", False), ("PYTHON2024", False), ("PythonLang", False),
                 ("Py1", False), ("aB3aB3aB", True), ("", False)]:
    got = is_strong(pw)
    assert got == want, f"is_strong({pw!r}) should be {want}, got {got!r}"
""", """
def is_strong(password):
    return (len(password) >= 8
            and any(c.isdigit() for c in password)
            and any(c.isupper() for c in password)
            and any(c.islower() for c in password))

print(is_strong("Python2024"))
""", level=2)

ex("compress", "Strings", "Compress repeated letters", """
Run-length encoding replaces each run of the same letter with the letter and how many times it repeats.

Write `compress(text)`: `"aaabbc"` becomes `"a3b2c1"`. An empty string stays empty.

Think about it: you need to remember the current letter and its count, and write them out each time the letter changes - and once more at the very end.
""", """
def compress(text):


print(compress("aaabbc"))
""", """
for text, want in [("aaabbc", "a3b2c1"), ("abc", "a1b1c1"), ("zzzz", "z4"), ("", ""), ("aabaa", "a2b1a2")]:
    got = compress(text)
    assert got == want, f"compress({text!r}) should be {want!r}, got {got!r}"
""", """
def compress(text):
    if not text:
        return ""
    result = ""
    current = text[0]
    count = 1
    for ch in text[1:]:
        if ch == current:
            count += 1
        else:
            result += current + str(count)
            current = ch
            count = 1
    return result + current + str(count)

print(compress("aaabbc"))
""", level=3)

# ───────────────────────── Conditions ─────────────────────────

ex("max-of-three", "Conditions", "Largest of three", """
Write `largest(a, b, c)` that returns the biggest of three numbers.

Do it with `if` and comparisons - no `max()` this time. Be careful when two numbers are equal.
""", """
def largest(a, b, c):


print(largest(3, 9, 5))
""", """
for args, want in [((3, 9, 5), 9), ((9, 3, 5), 9), ((3, 5, 9), 9), ((4, 4, 2), 4), ((1, 7, 7), 7), ((-3, -1, -2), -1), ((5, 5, 5), 5)]:
    got = largest(*args)
    assert got == want, f"largest{args} should be {want}, got {got!r}"
""", """
def largest(a, b, c):
    if a >= b and a >= c:
        return a
    elif b >= c:
        return b
    else:
        return c

print(largest(3, 9, 5))
""")

ex("triangle-type", "Conditions", "Triangle types", """
Three lengths make a triangle only if every side is shorter than the other two added together.

Write `triangle_type(a, b, c)` that returns:
- `"not a triangle"` when the sides cannot form one
- `"equilateral"` when all three sides are equal
- `"isosceles"` when exactly two sides are equal
- `"scalene"` when all sides are different
""", """
def triangle_type(a, b, c):


print(triangle_type(3, 4, 5))
""", """
for args, want in [((3, 4, 5), "scalene"), ((2, 2, 2), "equilateral"), ((2, 2, 3), "isosceles"), ((3, 2, 2), "isosceles"),
                   ((1, 2, 3), "not a triangle"), ((1, 1, 5), "not a triangle"), ((5, 1, 1), "not a triangle")]:
    got = triangle_type(*args)
    assert got == want, f"triangle_type{args} should be {want!r}, got {got!r}"
""", """
def triangle_type(a, b, c):
    if a + b <= c or a + c <= b or b + c <= a:
        return "not a triangle"
    if a == b == c:
        return "equilateral"
    if a == b or b == c or a == c:
        return "isosceles"
    return "scalene"

print(triangle_type(3, 4, 5))
""", level=2)

ex("ticket-price", "Conditions", "Ticket prices", """
A cinema charges by age:
- under 6: free (0)
- 6 to 17: 5
- 18 to 64: 10, but students pay 7
- 65 and over: 6

Write `ticket_price(age, is_student)` that returns the price. The student discount only applies to the 18 to 64 group.
""", """
def ticket_price(age, is_student):


print(ticket_price(20, True))
""", """
for age, student, want in [(3, False, 0), (5, True, 0), (6, False, 5), (17, True, 5), (18, False, 10), (18, True, 7),
                           (64, True, 7), (64, False, 10), (65, False, 6), (80, True, 6)]:
    got = ticket_price(age, student)
    assert got == want, f"ticket_price({age}, {student}) should be {want}, got {got!r}"
""", """
def ticket_price(age, is_student):
    if age < 6:
        return 0
    elif age < 18:
        return 5
    elif age < 65:
        return 7 if is_student else 10
    else:
        return 6

print(ticket_price(20, True))
""", level=2)

# ───────────────────────── Loops ─────────────────────────

ex("star-triangle", "Loops", "Star triangle", """
Multiplying a string repeats it: `"*" * 3` is `"***"`.

Print a triangle of stars with 5 rows: one star on the first line, two on the second, up to five.
""", """
rows = 5

""", """
want = ["*" * i for i in range(1, 6)]
got = [line.rstrip() for line in OUTPUT.strip().splitlines()]
assert got == want, f"Expected 5 lines growing from * to ***** - your program printed: {got}"
""", """
rows = 5
for i in range(1, rows + 1):
    print("*" * i)
""")

ex("sum-digits", "Loops", "Sum of digits", """
`n % 10` gives the last digit of a number and `n // 10` removes it.

Write `sum_digits(n)` that adds up the digits of a positive whole number. `sum_digits(1234)` is 1 + 2 + 3 + 4 = `10`.
""", """
def sum_digits(n):


print(sum_digits(1234))
""", """
for n, want in [(1234, 10), (0, 0), (7, 7), (999, 27), (1000001, 2)]:
    got = sum_digits(n)
    assert got == want, f"sum_digits({n}) should be {want}, got {got!r}"
""", """
def sum_digits(n):
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total

print(sum_digits(1234))
""")

ex("reverse-number", "Loops", "Reverse a number", """
Write `reverse_number(n)` that reverses the digits of a positive whole number and returns a number: `1234` becomes `4321`, and `1200` becomes `21`.

Try it with arithmetic (`% 10` and `// 10`): build the result by multiplying it by 10 and adding the next digit.
""", """
def reverse_number(n):


print(reverse_number(1234))
""", """
for n, want in [(1234, 4321), (1200, 21), (7, 7), (0, 0), (1001, 1001)]:
    got = reverse_number(n)
    assert got == want and isinstance(got, int), f"reverse_number({n}) should be the number {want}, got {got!r}"
""", """
def reverse_number(n):
    result = 0
    while n > 0:
        result = result * 10 + n % 10
        n //= 10
    return result

print(reverse_number(1234))
""", level=2)

ex("collatz", "Loops", "Collatz steps", """
Take any positive number. If it is even, halve it. If it is odd, multiply by 3 and add 1. Repeat. Nobody has proved it, but every number tried so far ends at 1.

Write `collatz_steps(n)` that returns how many steps it takes to reach 1.
6 goes 6, 3, 10, 5, 16, 8, 4, 2, 1 - that is `8` steps. Starting at 1 takes `0` steps.
""", """
def collatz_steps(n):


print(collatz_steps(6))
""", """
for n, want in [(1, 0), (2, 1), (6, 8), (7, 16), (27, 111)]:
    got = collatz_steps(n)
    assert got == want, f"collatz_steps({n}) should be {want}, got {got!r}"
""", """
def collatz_steps(n):
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

print(collatz_steps(6))
""", level=2)

ex("gcd", "Loops", "Greatest common divisor", """
The greatest common divisor (GCD) of two numbers is the largest number that divides both. For 12 and 18 it is 6.

Euclid's method, over 2000 years old: keep replacing the pair `(a, b)` with `(b, a % b)` until `b` is 0. Then `a` is the answer.

Write `gcd(a, b)` using a loop.
""", """
def gcd(a, b):


print(gcd(12, 18))
""", """
for a, b, want in [(12, 18, 6), (18, 12, 6), (17, 5, 1), (100, 25, 25), (7, 0, 7), (270, 192, 6)]:
    got = gcd(a, b)
    assert got == want, f"gcd({a}, {b}) should be {want}, got {got!r}"
""", """
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

print(gcd(12, 18))
""", level=2)

# ───────────────────────── Lists ─────────────────────────

ex("running-total", "Lists", "Running total", """
Write `running_total(nums)` that returns a new list where each item is the sum of all the numbers up to and including that position.

`running_total([1, 2, 3, 4])` returns `[1, 3, 6, 10]`.
""", """
def running_total(nums):


print(running_total([1, 2, 3, 4]))
""", """
for nums, want in [([1, 2, 3, 4], [1, 3, 6, 10]), ([], []), ([5], [5]), ([2, -2, 2], [2, 0, 2])]:
    got = running_total(list(nums))
    assert got == want, f"running_total({nums}) should be {want}, got {got!r}"
""", """
def running_total(nums):
    result = []
    total = 0
    for n in nums:
        total += n
        result.append(total)
    return result

print(running_total([1, 2, 3, 4]))
""")

ex("dedupe-order", "Lists", "Remove duplicates, keep order", """
`set()` removes duplicates but forgets the order. Here the order matters.

Write `dedupe(items)` that returns a new list with repeats removed, keeping the first time each item appears.
`dedupe([3, 1, 3, 2, 1])` returns `[3, 1, 2]`.
""", """
def dedupe(items):


print(dedupe([3, 1, 3, 2, 1]))
""", """
for items, want in [([3, 1, 3, 2, 1], [3, 1, 2]), ([], []), (["b", "a", "b"], ["b", "a"]), ([1, 1, 1], [1])]:
    got = dedupe(list(items))
    assert got == want, f"dedupe({items}) should be {want}, got {got!r}"
""", """
def dedupe(items):
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result

print(dedupe([3, 1, 3, 2, 1]))
""", level=2)

ex("rotate", "Lists", "Rotate a list", """
Rotating a list to the right by 1 moves the last item to the front: `[1, 2, 3, 4]` becomes `[4, 1, 2, 3]`.

Write `rotate(items, k)` that returns a new list rotated right by k positions. k can be bigger than the list (rotating 4 items by 5 is the same as by 1). An empty list stays empty.
""", """
def rotate(items, k):


print(rotate([1, 2, 3, 4], 1))
""", """
for items, k, want in [([1, 2, 3, 4], 1, [4, 1, 2, 3]), ([1, 2, 3, 4], 2, [3, 4, 1, 2]), ([1, 2, 3, 4], 0, [1, 2, 3, 4]),
                       ([1, 2, 3, 4], 4, [1, 2, 3, 4]), ([1, 2, 3, 4], 5, [4, 1, 2, 3]), ([], 3, []), ([7], 9, [7])]:
    got = rotate(list(items), k)
    assert got == want, f"rotate({items}, {k}) should be {want}, got {got!r}"
""", """
def rotate(items, k):
    if not items:
        return []
    k = k % len(items)
    return items[len(items) - k:] + items[:len(items) - k]

print(rotate([1, 2, 3, 4], 1))
""", level=2)

ex("merge-sorted", "Lists", "Merge two sorted lists", """
You have two lists that are each already sorted. Merge them into one sorted list.

Do it without `sorted()` or `.sort()`: keep one position in each list, compare the two current items, take the smaller one and move that position forward. When one list runs out, add what is left of the other.

Write `merge(a, b)`.
""", """
def merge(a, b):


print(merge([1, 4, 9], [2, 3, 10]))
""", """
for a, b, want in [([1, 4, 9], [2, 3, 10], [1, 2, 3, 4, 9, 10]), ([], [1, 2], [1, 2]), ([1, 2], [], [1, 2]), ([], [], []),
                   ([1, 1], [1], [1, 1, 1]), ([5, 6], [1, 2], [1, 2, 5, 6])]:
    got = merge(list(a), list(b))
    assert got == want, f"merge({a}, {b}) should be {want}, got {got!r}"
""", """
def merge(a, b):
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    return result + a[i:] + b[j:]

print(merge([1, 4, 9], [2, 3, 10]))
""", level=3)

ex("two-sum", "Lists", "Two sum", """
A famous interview question.

Write `two_sum(nums, target)` that finds two different positions whose numbers add up to `target`, and returns the positions as a tuple `(i, j)` with `i` smaller than `j`. Return `None` when no pair exists.

`two_sum([2, 7, 11, 15], 9)` returns `(0, 1)` because 2 + 7 = 9.
Each test has at most one correct pair.
""", """
def two_sum(nums, target):


print(two_sum([2, 7, 11, 15], 9))
""", """
for nums, target, want in [([2, 7, 11, 15], 9, (0, 1)), ([3, 2, 4], 6, (1, 2)), ([1, 2, 3], 7, None), ([5], 10, None),
                           ([3, 3], 6, (0, 1)), ([1, 5, 9, 2], 11, (2, 3))]:
    got = two_sum(list(nums), target)
    got = tuple(got) if got is not None else None
    assert got == want, f"two_sum({nums}, {target}) should be {want}, got {got!r}"
""", """
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None

print(two_sum([2, 7, 11, 15], 9))
""", level=2)

# ───────────────────────── Functions ─────────────────────────

ex("average-args", "Functions", "Any number of arguments", """
A parameter written `*nums` collects all the arguments into a tuple, so the function can be called with any number of values.

Write `average(*nums)` that returns the average of its arguments, or `0` when called with none.
""", """
def average(*nums):


print(average(2, 4, 6))
""", """
assert average(2, 4, 6) == 4, f"average(2, 4, 6) should be 4.0, got {average(2, 4, 6)!r}"
assert average(5) == 5, f"average(5) should be 5.0, got {average(5)!r}"
assert average() == 0, f"average() with no arguments should be 0, got {average()!r}"
assert average(1, 2) == 1.5, f"average(1, 2) should be 1.5, got {average(1, 2)!r}"
""", """
def average(*nums):
    if not nums:
        return 0
    return sum(nums) / len(nums)

print(average(2, 4, 6))
""")

ex("apply-twice", "Functions", "Functions as values", """
In Python a function is a value like any other. You can pass it to another function and call it there.

Write `apply_twice(func, value)` that calls `func` on the value, then calls `func` again on the result.
With `add_three` below, `apply_twice(add_three, 10)` returns `16`.
""", """
def add_three(x):
    return x + 3

def apply_twice(func, value):


print(apply_twice(add_three, 10))
""", """
assert apply_twice(lambda x: x + 3, 10) == 16, "apply_twice(add_three, 10) should be 16"
assert apply_twice(lambda x: x * 2, 5) == 20, "With a doubling function, apply_twice(double, 5) should be 20"
assert apply_twice(str.upper, "hi") == "HI", "It should work with any function, for example str.upper"
assert apply_twice(lambda s: s + "!", "hey") == "hey!!", "The second call must use the result of the first call"
""", """
def add_three(x):
    return x + 3

def apply_twice(func, value):
    return func(func(value))

print(apply_twice(add_three, 10))
""", level=2)

# ───────────────────────── Dictionaries ─────────────────────────

ex("invert-dict", "Dictionaries", "Swap keys and values", """
Write `invert(d)` that returns a new dictionary where every value becomes a key and every key becomes its value.

`invert({"a": 1, "b": 2})` returns `{1: "a", 2: "b"}`. You can assume all values are different.
""", """
def invert(d):


print(invert({"a": 1, "b": 2}))
""", """
got = invert({"a": 1, "b": 2})
assert got == {1: "a", 2: "b"}, f'invert({{"a": 1, "b": 2}}) should be {{1: "a", 2: "b"}}, got {got!r}'
assert invert({}) == {}, "An empty dictionary stays empty"
src = {"x": "y"}
assert invert(src) == {"y": "x"} and src == {"x": "y"}, "Return a new dictionary and leave the original unchanged"
""", """
def invert(d):
    result = {}
    for key, value in d.items():
        result[value] = key
    return result

print(invert({"a": 1, "b": 2}))
""")

ex("group-by-length", "Dictionaries", "Group words by length", """
A dictionary value can be a list. Before appending to it, make sure the key exists: `if key not in d: d[key] = []`.

Write `group_by_length(words)` that returns a dictionary from word length to the list of words with that length, in their original order.
`group_by_length(["sun", "moon", "cat"])` returns `{3: ["sun", "cat"], 4: ["moon"]}`.
""", """
def group_by_length(words):


print(group_by_length(["sun", "moon", "cat"]))
""", """
got = group_by_length(["sun", "moon", "cat"])
assert got == {3: ["sun", "cat"], 4: ["moon"]}, f"Expected {{3: ['sun', 'cat'], 4: ['moon']}}, got {got!r}"
assert group_by_length([]) == {}, "An empty list should give an empty dictionary"
got = group_by_length(["a", "b", "cc", "d"])
assert got == {1: ["a", "b", "d"], 2: ["cc"]}, f"Words must stay in their original order, got {got!r}"
""", """
def group_by_length(words):
    groups = {}
    for word in words:
        if len(word) not in groups:
            groups[len(word)] = []
        groups[len(word)].append(word)
    return groups

print(group_by_length(["sun", "moon", "cat"]))
""", level=2)

ex("most-common-letter", "Dictionaries", "Most common letter", """
Write `most_common_letter(text)` that returns the letter that appears most often.

Rules:
- ignore upper/lower case and return the letter in lower case
- count only letters (use `.isalpha()`), not spaces or punctuation
- when several letters tie, return the one that comes first in the alphabet
""", """
def most_common_letter(text):


print(most_common_letter("Hello World"))
""", """
for text, want in [("Hello World", "l"), ("banana", "a"), ("abcABC", "a"), ("zz yy", "y"), ("x", "x"), ("a.b.b!!!", "b")]:
    got = most_common_letter(text)
    assert got == want, f"most_common_letter({text!r}) should be {want!r}, got {got!r}"
""", """
def most_common_letter(text):
    counts = {}
    for ch in text.lower():
        if ch.isalpha():
            counts[ch] = counts.get(ch, 0) + 1
    best = None
    for letter in sorted(counts):
        if best is None or counts[letter] > counts[best]:
            best = letter
    return best

print(most_common_letter("Hello World"))
""", level=3)

# ───────────────────────── Comprehensions ─────────────────────────

ex("dict-comprehension", "Comprehensions", "Dictionary comprehension", """
Comprehensions build dictionaries too: `{n: n * n for n in range(3)}` gives `{0: 0, 1: 1, 2: 4}`.

Use one to make `lengths`: each word in `words` mapped to its number of letters.
""", """
words = ["apple", "fig", "banana"]

lengths =
print(lengths)
""", """
assert lengths == {"apple": 5, "fig": 3, "banana": 6}, f"lengths should be {{'apple': 5, 'fig': 3, 'banana': 6}}, got {lengths!r}"
""", """
words = ["apple", "fig", "banana"]
lengths = {w: len(w) for w in words}
print(lengths)
""")

ex("flatten", "Comprehensions", "Flatten a list of lists", """
A comprehension can have two `for` parts. They read in the same order as nested loops:
`[x for row in rows for x in row]`

Write `flatten(rows)` that turns a list of lists into one flat list.
`flatten([[1, 2], [3], [4, 5]])` returns `[1, 2, 3, 4, 5]`.
""", """
def flatten(rows):


print(flatten([[1, 2], [3], [4, 5]]))
""", """
for rows, want in [([[1, 2], [3], [4, 5]], [1, 2, 3, 4, 5]), ([], []), ([[], [1], []], [1]), ([["a"], ["b", "c"]], ["a", "b", "c"])]:
    got = flatten(rows)
    assert got == want, f"flatten({rows}) should be {want}, got {got!r}"
""", """
def flatten(rows):
    return [x for row in rows for x in row]

print(flatten([[1, 2], [3], [4, 5]]))
""", level=2)

# ───────────────────────── Errors ─────────────────────────

ex("validate-age", "Errors", "Raising your own errors", """
`raise ValueError("message")` stops the function and reports a problem to whoever called it.

Write `validate_age(age)`:
- if age is below 0 or above 150, raise `ValueError`
- otherwise return the age unchanged
""", """
def validate_age(age):


print(validate_age(30))
""", """
assert validate_age(30) == 30, f"validate_age(30) should return 30, got {validate_age(30)!r}"
assert validate_age(0) == 0, "0 is a valid age"
assert validate_age(150) == 150, "150 is still allowed"
for bad in (-1, 151, 999):
    try:
        validate_age(bad)
    except ValueError:
        pass
    else:
        raise AssertionError(f"validate_age({bad}) should raise ValueError")
""", """
def validate_age(age):
    if age < 0 or age > 150:
        raise ValueError("age must be between 0 and 150")
    return age

print(validate_age(30))
""", level=2)

# ───────────────────────── Classes ─────────────────────────

ex("stack", "Classes", "Build a stack", """
A stack works like a pile of plates: you add to the top and take from the top.

Write a class `Stack`:
- `.push(item)` adds an item on top
- `.pop()` removes the top item and returns it
- `.peek()` returns the top item without removing it
- `.is_empty()` returns `True` or `False`
- `.size()` returns how many items it holds

Keep the items in a list stored on `self`.
""", """
class Stack:


s = Stack()
s.push(1)
s.push(2)
print(s.pop(), s.peek(), s.size())
""", """
s = Stack()
assert s.is_empty() is True, "A new stack should be empty"
assert s.size() == 0, "A new stack should have size 0"
s.push("a"); s.push("b"); s.push("c")
assert s.size() == 3, f"After three pushes size() should be 3, got {s.size()!r}"
assert s.peek() == "c", f"peek() should return the last item pushed, got {s.peek()!r}"
assert s.size() == 3, "peek() must not remove the item"
assert s.pop() == "c", "pop() should return the last item pushed"
assert s.pop() == "b", "The second pop() should return the item pushed before that"
assert s.size() == 1 and s.is_empty() is False, "After two pops, one item should remain"
other = Stack()
assert other.is_empty(), "Each Stack needs its own list - create it inside __init__"
""", """
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

s = Stack()
s.push(1)
s.push(2)
print(s.pop(), s.peek(), s.size())
""", level=2)

ex("student-class", "Classes", "Student grades", """
Write a class `Student`:
- `Student("Aziz")` stores the name and starts with no grades
- `.add_grade(score)` records a score
- `.average()` returns the average score, or `0` when there are no grades yet
- `.best()` returns the highest score, or `None` when there are no grades yet
""", """
class Student:


aziz = Student("Aziz")
aziz.add_grade(80)
aziz.add_grade(90)
print(aziz.name, aziz.average(), aziz.best())
""", """
s = Student("Aziz")
assert s.name == "Aziz", "The name should be stored in self.name"
assert s.average() == 0, f"With no grades average() should be 0, got {s.average()!r}"
assert s.best() is None, f"With no grades best() should be None, got {s.best()!r}"
s.add_grade(80); s.add_grade(90); s.add_grade(70)
assert s.average() == 80, f"The average of 80, 90, 70 should be 80.0, got {s.average()!r}"
assert s.best() == 90, f"best() should be 90, got {s.best()!r}"
t = Student("Lola")
assert t.average() == 0, "Each student needs their own list of grades - create it inside __init__"
""", """
class Student:
    def __init__(self, name):
        self.name = name
        self.grades = []

    def add_grade(self, score):
        self.grades.append(score)

    def average(self):
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)

    def best(self):
        if not self.grades:
            return None
        return max(self.grades)

aziz = Student("Aziz")
aziz.add_grade(80)
aziz.add_grade(90)
print(aziz.name, aziz.average(), aziz.best())
""", level=2)

# ───────────────────────── Recursion ─────────────────────────

ex("power", "Recursion", "Power by recursion", """
A recursive function calls itself on a smaller version of the problem. It always needs a base case - the smallest problem, answered directly - or it never stops.

2 to the power 5 is 2 times (2 to the power 4). And anything to the power 0 is 1.

Write `power(base, exp)` using recursion - no `**` and no loops. `exp` is a whole number, 0 or more.
""", """
def power(base, exp):


print(power(2, 5))
""", """
for b, e, want in [(2, 5, 32), (2, 0, 1), (5, 1, 5), (3, 4, 81), (10, 3, 1000), (0, 3, 0)]:
    got = power(b, e)
    assert got == want, f"power({b}, {e}) should be {want}, got {got!r}"
""", """
def power(base, exp):
    if exp == 0:
        return 1
    return base * power(base, exp - 1)

print(power(2, 5))
""", level=2)

ex("recursive-sum", "Recursion", "Sum a list recursively", """
The sum of a list is its first item plus the sum of the rest: `nums[0]` plus the sum of `nums[1:]`. The sum of an empty list is 0.

Write `total(nums)` using recursion - no `sum()` and no loops.
""", """
def total(nums):


print(total([1, 2, 3, 4]))
""", """
for nums, want in [([1, 2, 3, 4], 10), ([], 0), ([7], 7), ([-1, 1], 0), (list(range(50)), 1225)]:
    got = total(list(nums))
    assert got == want, f"total({nums if len(nums) < 8 else 'range(50)'}) should be {want}, got {got!r}"
""", """
def total(nums):
    if not nums:
        return 0
    return nums[0] + total(nums[1:])

print(total([1, 2, 3, 4]))
""", level=2)

ex("flatten-deep", "Recursion", "Flatten any depth", """
Lists can contain lists that contain lists. `isinstance(x, list)` tells you whether `x` is a list.

Write `flatten_deep(items)` that returns one flat list no matter how deeply the lists are nested.
`flatten_deep([1, [2, [3, [4]], 5]])` returns `[1, 2, 3, 4, 5]`.

Idea: go through the items. A plain value is added to the result. A list is flattened by calling the same function on it, and its values are added.
""", """
def flatten_deep(items):


print(flatten_deep([1, [2, [3, [4]], 5]]))
""", """
for items, want in [([1, [2, [3, [4]], 5]], [1, 2, 3, 4, 5]), ([], []), ([1, 2], [1, 2]), ([[[]]], []),
                    ([[1], [[2]], [[[3]]]], [1, 2, 3]), (["a", ["b"]], ["a", "b"])]:
    got = flatten_deep(items)
    assert got == want, f"flatten_deep({items}) should be {want}, got {got!r}"
""", """
def flatten_deep(items):
    result = []
    for item in items:
        if isinstance(item, list):
            result.extend(flatten_deep(item))
        else:
            result.append(item)
    return result

print(flatten_deep([1, [2, [3, [4]], 5]]))
""", level=3)

ex("permutations", "Recursion", "All permutations", """
The permutations of "abc" are all the ways to order its letters: abc, acb, bac, bca, cab, cba.

Write `permutations(text)` that returns a sorted list of all of them. All letters in the text are different. For an empty string return `[""]`.

Idea: pick each letter in turn to go first, then put every permutation of the remaining letters after it.
""", """
def permutations(text):


print(permutations("abc"))
""", """
for text, want in [("abc", ["abc", "acb", "bac", "bca", "cab", "cba"]), ("a", ["a"]), ("", [""]), ("ba", ["ab", "ba"])]:
    got = permutations(text)
    assert got == want, f"permutations({text!r}) should be {want}, got {got!r}"
got = permutations("abcd")
assert len(got) == 24 and len(set(got)) == 24 and got == sorted(got), "permutations('abcd') should be 24 different strings, sorted"
""", """
def permutations(text):
    if len(text) <= 1:
        return [text]
    result = []
    for i in range(len(text)):
        rest = text[:i] + text[i + 1:]
        for p in permutations(rest):
            result.append(text[i] + p)
    return sorted(result)

print(permutations("abc"))
""", level=3)

# ───────────────────────── Grids ─────────────────────────

ex("row-sums", "Grids", "Row sums", """
A grid is a list of rows, and each row is a list: `grid[1][0]` is row 1, column 0.

Write `row_sums(grid)` that returns a list with the sum of each row.
""", """
def row_sums(grid):


print(row_sums([[1, 2, 3], [4, 5, 6]]))
""", """
for grid, want in [([[1, 2, 3], [4, 5, 6]], [6, 15]), ([], []), ([[7]], [7]), ([[1, -1], [0, 0], [2, 2]], [0, 0, 4])]:
    got = row_sums(grid)
    assert got == want, f"row_sums({grid}) should be {want}, got {got!r}"
""", """
def row_sums(grid):
    return [sum(row) for row in grid]

print(row_sums([[1, 2, 3], [4, 5, 6]]))
""")

ex("transpose", "Grids", "Transpose a grid", """
Transposing turns rows into columns:

`[[1, 2, 3], [4, 5, 6]]` becomes `[[1, 4], [2, 5], [3, 6]]`.

Write `transpose(grid)`. The grid has at least one row and all rows have the same length.
""", """
def transpose(grid):


print(transpose([[1, 2, 3], [4, 5, 6]]))
""", """
for grid, want in [([[1, 2, 3], [4, 5, 6]], [[1, 4], [2, 5], [3, 6]]), ([[1]], [[1]]), ([[1, 2]], [[1], [2]]),
                   ([[1], [2]], [[1, 2]])]:
    got = [list(row) for row in transpose(grid)]
    assert got == want, f"transpose({grid}) should be {want}, got {got!r}"
""", """
def transpose(grid):
    result = []
    for col in range(len(grid[0])):
        result.append([row[col] for row in grid])
    return result

print(transpose([[1, 2, 3], [4, 5, 6]]))
""", level=2)

ex("tic-tac-toe", "Grids", "Tic-tac-toe winner", """
A tic-tac-toe board is a 3 x 3 grid of `"X"`, `"O"` or `""` (empty).

Write `winner(board)` that returns `"X"` or `"O"` when that player has three in a row - across, down or diagonally - and `None` when nobody has won.
""", """
def winner(board):


print(winner([["X", "O", ""],
              ["O", "X", ""],
              ["", "", "X"]]))
""", """
cases = [
    ([["X", "O", ""], ["O", "X", ""], ["", "", "X"]], "X"),
    ([["O", "O", "O"], ["X", "X", ""], ["", "", "X"]], "O"),
    ([["X", "O", ""], ["X", "O", ""], ["X", "", ""]], "X"),
    ([["X", "X", "O"], ["X", "O", ""], ["O", "", ""]], "O"),
    ([["", "", ""], ["", "", ""], ["", "", ""]], None),
    ([["X", "O", "X"], ["X", "O", "O"], ["O", "X", "X"]], None),
    ([["", "", "O"], ["", "", "O"], ["X", "X", "O"]], "O"),
    ([["", "", ""], ["", "", ""], ["X", "X", "X"]], "X"),
]
for board, want in cases:
    got = winner(board)
    assert got == want, f"For the board {board} the winner should be {want!r}, got {got!r}"
""", """
def winner(board):
    lines = []
    for i in range(3):
        lines.append([board[i][0], board[i][1], board[i][2]])
        lines.append([board[0][i], board[1][i], board[2][i]])
    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])
    for line in lines:
        if line[0] != "" and line[0] == line[1] == line[2]:
            return line[0]
    return None

print(winner([["X", "O", ""],
              ["O", "X", ""],
              ["", "", "X"]]))
""", level=3)

ex("count-islands", "Grids", "Count the islands", """
A map is a grid of `1` (land) and `0` (water). An island is a group of land cells connected up, down, left or right - not diagonally.

Write `count_islands(grid)` that returns the number of islands.

Idea: scan every cell. When you find land you have not visited, that is a new island - then "sink" the whole island by visiting all the land connected to it, so it is not counted again.
""", """
def count_islands(grid):


print(count_islands([[1, 1, 0, 0],
                     [0, 1, 0, 1],
                     [0, 0, 0, 1],
                     [1, 0, 0, 0]]))
""", """
cases = [
    ([[1, 1, 0, 0], [0, 1, 0, 1], [0, 0, 0, 1], [1, 0, 0, 0]], 3),
    ([[0, 0], [0, 0]], 0),
    ([[1, 1], [1, 1]], 1),
    ([[1, 0], [0, 1]], 2),
    ([[1, 0, 1, 0, 1]], 3),
    ([], 0),
    ([[1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0]], 1),
]
for grid, want in cases:
    got = count_islands([list(row) for row in grid])
    assert got == want, f"count_islands({grid}) should be {want}, got {got!r}"
""", """
def count_islands(grid):
    seen = set()
    count = 0
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == 1 and (r, c) not in seen:
                count += 1
                todo = [(r, c)]
                while todo:
                    y, x = todo.pop()
                    if (y, x) in seen:
                        continue
                    seen.add((y, x))
                    for ny, nx in [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]:
                        if 0 <= ny < len(grid) and 0 <= nx < len(grid[ny]) and grid[ny][nx] == 1:
                            todo.append((ny, nx))
    return count

print(count_islands([[1, 1, 0, 0],
                     [0, 1, 0, 1],
                     [0, 0, 0, 1],
                     [1, 0, 0, 0]]))
""", level=3)

# ───────────────────────── Logic puzzles ─────────────────────────

ex("missing-number", "Logic puzzles", "The missing number", """
A list should contain every number from 1 to n exactly once, but one number is missing.

Write `missing_number(nums, n)` that returns the missing one. The list is not sorted.
`missing_number([3, 1, 4], 4)` returns `2`.

There is a neat trick: you know what the numbers 1 to n should add up to.
""", """
def missing_number(nums, n):


print(missing_number([3, 1, 4], 4))
""", """
for nums, n, want in [([3, 1, 4], 4, 2), ([2, 3], 3, 1), ([1, 2], 3, 3), ([], 1, 1), ([5, 2, 1, 3, 6], 6, 4)]:
    got = missing_number(list(nums), n)
    assert got == want, f"missing_number({nums}, {n}) should be {want}, got {got!r}"
""", """
def missing_number(nums, n):
    return n * (n + 1) // 2 - sum(nums)

print(missing_number([3, 1, 4], 4))
""", level=2)

ex("chickens-rabbits", "Logic puzzles", "Chickens and rabbits", """
An old puzzle: a farm has chickens (2 legs) and rabbits (4 legs). You count the heads and the legs.

Write `solve(heads, legs)` that returns a tuple `(chickens, rabbits)`, or `None` when no whole-number answer is possible.

`solve(35, 94)` returns `(23, 12)`: 23 chickens and 12 rabbits have 35 heads and 94 legs.

You can try every possible number of chickens, or work it out with algebra.
""", """
def solve(heads, legs):


print(solve(35, 94))
""", """
for heads, legs, want in [(35, 94, (23, 12)), (3, 8, (2, 1)), (2, 8, (0, 2)), (2, 4, (2, 0)), (0, 0, (0, 0)),
                          (3, 7, None), (2, 10, None), (5, 6, None)]:
    got = solve(heads, legs)
    got = tuple(got) if got is not None else None
    assert got == want, f"solve({heads}, {legs}) should be {want}, got {got!r}"
""", """
def solve(heads, legs):
    for chickens in range(heads + 1):
        rabbits = heads - chickens
        if 2 * chickens + 4 * rabbits == legs:
            return (chickens, rabbits)
    return None

print(solve(35, 94))
""", level=2)

ex("longest-streak", "Logic puzzles", "Longest streak", """
Write `longest_streak(items)` that returns the length of the longest run of equal items next to each other.

`longest_streak([1, 1, 2, 2, 2, 1])` returns `3` (the three 2s). An empty list gives `0`.
""", """
def longest_streak(items):


print(longest_streak([1, 1, 2, 2, 2, 1]))
""", """
for items, want in [([1, 1, 2, 2, 2, 1], 3), ([], 0), ([5], 1), ([1, 2, 3], 1), ([4, 4, 4, 4], 4), (list("aabbbbc"), 4),
                    ([1, 2, 2, 3, 3, 3], 3)]:
    got = longest_streak(list(items))
    assert got == want, f"longest_streak({items}) should be {want}, got {got!r}"
""", """
def longest_streak(items):
    best = 0
    current = 0
    previous = None
    for i, item in enumerate(items):
        if i > 0 and item == previous:
            current += 1
        else:
            current = 1
        previous = item
        best = max(best, current)
    return best

print(longest_streak([1, 1, 2, 2, 2, 1]))
""", level=2)

ex("common-prefix", "Logic puzzles", "Longest common prefix", """
Write `common_prefix(words)` that returns the longest beginning shared by every word in the list.

`common_prefix(["flower", "flow", "flight"])` returns `"fl"`. If the words share nothing, or the list is empty, return `""`.
""", """
def common_prefix(words):


print(common_prefix(["flower", "flow", "flight"]))
""", """
for words, want in [(["flower", "flow", "flight"], "fl"), (["dog", "car"], ""), ([], ""), (["same"], "same"),
                    (["abc", "abc"], "abc"), (["ab", "a"], "a"), (["", "abc"], ""), (["interview", "internet", "into"], "int")]:
    got = common_prefix(list(words))
    assert got == want, f"common_prefix({words}) should be {want!r}, got {got!r}"
""", """
def common_prefix(words):
    if not words:
        return ""
    prefix = words[0]
    for word in words[1:]:
        while not word.startswith(prefix):
            prefix = prefix[:-1]
    return prefix

print(common_prefix(["flower", "flow", "flight"]))
""", level=2)

ex("prime-factors", "Logic puzzles", "Prime factors", """
Every whole number above 1 can be written as primes multiplied together: 60 = 2 x 2 x 3 x 5.

Write `prime_factors(n)` that returns the list of prime factors from smallest to largest, with repeats.
`prime_factors(60)` returns `[2, 2, 3, 5]`.

Idea: try dividing by 2 as many times as it works, then by 3, then 4, and so on. You never need to check whether the divisor is prime - think about why.
""", """
def prime_factors(n):


print(prime_factors(60))
""", """
for n, want in [(60, [2, 2, 3, 5]), (2, [2]), (13, [13]), (8, [2, 2, 2]), (97, [97]), (1001, [7, 11, 13]), (360, [2, 2, 2, 3, 3, 5])]:
    got = prime_factors(n)
    assert got == want, f"prime_factors({n}) should be {want}, got {got!r}"
""", """
def prime_factors(n):
    factors = []
    d = 2
    while n > 1:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    return factors

print(prime_factors(60))
""", level=2)

ex("balanced-brackets", "Logic puzzles", "Balanced brackets", """
Code editors check that brackets match. `"([]{})"` is balanced. `"(]"` is not, `"(("` is not, and `"([)]"` is not - the brackets close in the wrong order.

Write `is_balanced(text)` that returns `True` or `False`. Only the characters `( ) [ ] { }` matter; ignore everything else.

Idea: keep a list of the brackets that are still open. An opening bracket goes on the end of the list. A closing bracket must match the last one on the list, which is then removed.
""", """
def is_balanced(text):


print(is_balanced("([]{})"))
""", """
for text, want in [("([]{})", True), ("", True), ("(]", False), ("((", False), ("([)]", False), (")", False), ("())", False),
                   ("print(data[0])", True), ("{[()()]}", True), ("{[(])}", False), ("(()", False)]:
    got = is_balanced(text)
    assert got == want, f"is_balanced({text!r}) should be {want}, got {got!r}"
""", """
def is_balanced(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    open_brackets = []
    for ch in text:
        if ch in "([{":
            open_brackets.append(ch)
        elif ch in pairs:
            if not open_brackets or open_brackets.pop() != pairs[ch]:
                return False
    return not open_brackets

print(is_balanced("([]{})"))
""", level=3)

ex("binary-search", "Logic puzzles", "Binary search", """
To find a word in a dictionary you open it in the middle and decide which half to keep. Binary search does the same on a sorted list, halving the search area each step.

Write `binary_search(nums, target)` that returns the position of `target` in the sorted list `nums`, or `-1` when it is not there.

Keep two positions, `low` and `high`. Look at the middle item: if it is the target you are done, if it is too small move `low` past it, if it is too big move `high` before it. Stop when `low` passes `high`.
""", """
def binary_search(nums, target):


print(binary_search([1, 3, 5, 7, 9, 11], 7))
""", """
nums = [1, 3, 5, 7, 9, 11]
for target, want in [(7, 3), (1, 0), (11, 5), (4, -1), (0, -1), (12, -1)]:
    got = binary_search(list(nums), target)
    assert got == want, f"binary_search({nums}, {target}) should be {want}, got {got!r}"
assert binary_search([], 5) == -1, "Searching an empty list should return -1"
assert binary_search([5], 5) == 0, "binary_search([5], 5) should be 0"

class Watched(list):
    looks = 0
    def __getitem__(self, i):
        Watched.looks += 1
        return super().__getitem__(i)
    def index(self, *a):
        raise AssertionError("Do the search yourself - .index() looks at every item one by one")
    def __contains__(self, x):
        raise AssertionError("Do the search yourself - 'in' looks at every item one by one")
    def __iter__(self):
        raise AssertionError("Do not loop over the whole list - jump to the middle with nums[mid]")

big = Watched(range(0, 2000, 2))
got = binary_search(big, 1338)
assert got == 669, f"In a list of 1000 even numbers, 1338 is at position 669, got {got!r}"
assert Watched.looks <= 40, f"Binary search needs about 10 looks for 1000 items; yours used {Watched.looks}. Halve the search area each step."
""", """
def binary_search(nums, target):
    low = 0
    high = len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

print(binary_search([1, 3, 5, 7, 9, 11], 7))
""", level=3)

ex("bubble-sort", "Logic puzzles", "Write your own sort", """
Bubble sort: go through the list comparing each pair of neighbours, and swap them when they are in the wrong order. After one pass the largest item has "bubbled" to the end. Repeat until a full pass makes no swaps.

Write `bubble_sort(nums)` that returns a new sorted list, smallest first, without using `sorted()` or `.sort()`. Do not change the list you were given.
""", """
def bubble_sort(nums):


print(bubble_sort([5, 2, 9, 1]))
""", """
import builtins
_real_sorted = builtins.sorted
def _no_sorted(*a, **k):
    raise AssertionError("Write the sorting yourself - no sorted() this time")
builtins.sorted = _no_sorted
try:
    for nums in ([5, 2, 9, 1], [], [1], [3, 3, 1], [1, 2, 3], [9, 8, 7, 6, 5], [2, -1, 0, -5]):
        original = list(nums)
        got = bubble_sort(nums)
        want = _real_sorted(original)
        assert list(got) == want, f"bubble_sort({original}) should be {want}, got {got!r}"
        assert nums == original, "The list you were given was changed - copy it first with nums[:] or list(nums)"
finally:
    builtins.sorted = _real_sorted
""", """
def bubble_sort(nums):
    result = nums[:]
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(result) - 1):
            if result[i] > result[i + 1]:
                result[i], result[i + 1] = result[i + 1], result[i]
                swapped = True
    return result

print(bubble_sort([5, 2, 9, 1]))
""", level=3)

ex("roman", "Logic puzzles", "Roman numerals", """
Roman numerals use letters: I = 1, V = 5, X = 10, L = 50, C = 100, D = 500, M = 1000. A smaller letter before a bigger one is subtracted: IV = 4, IX = 9, XL = 40, XC = 90, CD = 400, CM = 900.

Write `to_roman(n)` for numbers from 1 to 3999. `to_roman(1994)` returns `MCMXCIV`.

Idea: make a list of values with their symbols, from 1000 down to 1, including the six subtraction pairs. Keep taking the biggest value that still fits.
""", """
def to_roman(n):


print(to_roman(1994))
""", """
for n, want in [(1, "I"), (3, "III"), (4, "IV"), (9, "IX"), (14, "XIV"), (40, "XL"), (58, "LVIII"), (90, "XC"),
                (400, "CD"), (1994, "MCMXCIV"), (2024, "MMXXIV"), (3999, "MMMCMXCIX")]:
    got = to_roman(n)
    assert got == want, f"to_roman({n}) should be {want!r}, got {got!r}"
""", """
def to_roman(n):
    table = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
             (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    result = ""
    for value, symbol in table:
        while n >= value:
            result += symbol
            n -= value
    return result

print(to_roman(1994))
""", level=3)

ex("pascal", "Logic puzzles", "Pascal's triangle", """
In Pascal's triangle every row starts and ends with 1, and each number in between is the sum of the two numbers above it:

`[1]`
`[1, 1]`
`[1, 2, 1]`
`[1, 3, 3, 1]`
`[1, 4, 6, 4, 1]`

Write `pascal(n)` that returns the first n rows as a list of lists. `pascal(0)` returns `[]`.
""", """
def pascal(n):


for row in pascal(5):
    print(row)
""", """
want = [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1]]
for n in range(0, 7):
    got = pascal(n)
    assert got == want[:n], f"pascal({n}) should be {want[:n]}, got {got!r}"
""", """
def pascal(n):
    rows = []
    for i in range(n):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = rows[i - 1][j - 1] + rows[i - 1][j]
        rows.append(row)
    return rows

for row in pascal(5):
    print(row)
""", level=3)

ex("min-coins", "Logic puzzles", "Fewest coins", """
You must pay an exact amount using as few coins as possible. You have unlimited coins of each given value.

Write `min_coins(amount, coins)` that returns the smallest number of coins, or `-1` when the amount cannot be made.

`min_coins(6, [1, 3, 4])` returns `2` (3 + 3). Careful: always grabbing the biggest coin gives 4 + 1 + 1, which is 3 coins - so that shortcut is wrong.

Idea: work out the best answer for every amount from 0 up to the target. The best for an amount is 1 plus the best for (amount minus a coin), over whichever coin makes that smallest.
""", """
def min_coins(amount, coins):


print(min_coins(6, [1, 3, 4]))
""", """
for amount, coins, want in [(6, [1, 3, 4], 2), (0, [1, 2], 0), (11, [1, 2, 5], 3), (3, [2], -1), (7, [2, 4], -1),
                            (30, [1, 15, 25], 2), (63, [1, 5, 10, 21, 25], 3), (100, [1, 5, 10, 25], 4)]:
    got = min_coins(amount, list(coins))
    assert got == want, f"min_coins({amount}, {coins}) should be {want}, got {got!r}"
""", """
def min_coins(amount, coins):
    best = [0] + [None] * amount
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a and best[a - coin] is not None:
                if best[a] is None or best[a - coin] + 1 < best[a]:
                    best[a] = best[a - coin] + 1
    return best[amount] if best[amount] is not None else -1

print(min_coins(6, [1, 3, 4]))
""", level=3)
