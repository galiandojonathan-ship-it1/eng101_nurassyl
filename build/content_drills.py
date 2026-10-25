"""Predict-the-output drills. build.py runs every drill and checks `out`.

`out` is the exact stdout. `why` explains the trace. Code that raises
on purpose sets `error` to the exception name and `out` to what prints first.
"""

DRILLS = [
    # ---------------- Foundations ----------------
    {"week": "w1-6", "title": "Operators depend on types", "code": '''\
print("7" + "2", int("7") + 2)
print(7 / 2, 7 // 2, 7 % 2)
print("3" * 2, 3 * 2)
print(2 + 3 * 4, (2 + 3) * 4)''',
     "out": "72 9\n3.5 3 1\n33 6\n14 20",
     "why": "String + joins text; int() converts first. / is true division, // floors, % is the remainder. A string times an int repeats it. * binds tighter than + unless parentheses say otherwise."},
    {"week": "w1-6", "title": "Assignment is not a formula", "code": '''\
radius = 2.0
area = 3.14 * radius**2
radius = 3.0
print(radius, area)''',
     "out": "3.0 12.56",
     "why": "area was computed once, when radius was 2.0. Rebinding radius does not recompute area."},
    {"week": "w1-6", "title": "range never includes stop", "code": '''\
print(list(range(4)))
print(list(range(1, 5)))
print(list(range(2, 9, 2)))
print(list(range(5, 0, -2)))
print(list(range(3, 3)))''',
     "out": "[0, 1, 2, 3]\n[1, 2, 3, 4]\n[2, 4, 6, 8]\n[5, 3, 1]\n[]",
     "why": "Start defaults to 0, step to 1. With a negative step the stop is still excluded. range(3, 3) is empty, so a loop over it runs zero times."},
    {"week": "w1-6", "title": "break and continue", "code": '''\
total = 0
for value in range(1, 7):
    if value == 2:
        continue
    if value == 5:
        break
    total += value
print(total)''',
     "out": "8",
     "why": "Visited: 1, 2, 3, 4, 5. Running total: 1, 1 (skip 2), 4, 8, then break at 5 before adding. 6 is in the range but never visited."},
    {"week": "w1-6", "title": "Strings are immutable", "code": '''\
raw = "  valve-204b  "
code = raw.strip().upper()
print(code[:5], code[6:9], code[-1])
print(code[1:8:2])
print(repr(raw))''',
     "out": "VALVE 204 B\nAV-0\n'  valve-204b  '",
     "why": "code is \"VALVE-204B\". [6:9] takes indices 6, 7, 8 → \"204\". [1:8:2] takes 1, 3, 5, 7 → A, V, -, 0. strip() and upper() return new strings, so raw still has its spaces."},
    {"week": "w1-6", "title": "print is not return", "code": '''\
def energy(power_w, time_s=2):
    energy_j = power_w * time_s
    print(energy_j)

result = energy(10)
print(result)''',
     "out": "20\nNone",
     "why": "The default time_s = 2 gives 20 J, which is printed inside the function. No return runs, so the caller stores None."},
    {"week": "w1-6", "title": "Early return in a loop", "code": '''\
def total_load(loads_n):
    total = 0.0
    for load in loads_n:
        total += load
        return total

print(total_load([2.0, 3.0, 4.0]))''',
     "out": "2.0",
     "why": "return ends the whole call on the first pass. 3.0 and 4.0 never contribute. Dedent the return to line up with the for to get 9.0."},
    {"week": "w1-6", "title": "Local names vs outer names", "code": '''\
gain = 10
def scale(value, gain=2):
    return value * gain

print(scale(3), scale(3, gain=4))
print(gain)''',
     "out": "6 12\n10",
     "why": "Inside the function gain is a local parameter: default 2, or 4 when passed. The outer gain is a different name and stays 10."},
    {"week": "w1-6", "title": "List operations: effect vs return", "code": '''\
values = [10, 20, 30]
values[1] = 25
result = values.append(40)
values.extend([50, 60])
removed = values.pop()
print(values)
print(result)
print(removed)''',
     "out": "[10, 25, 30, 40, 50]\nNone\n60",
     "why": "append mutates and returns None. extend adds 50 and 60 separately. pop() removes and returns the last item, 60."},
    {"week": "w1-6", "title": "Alias or copy?", "code": '''\
raw = [10, 20, 30]
alias = raw
copied = raw.copy()
alias[1] = 99
copied.append(40)
print(raw)
print(alias)
print(copied)''',
     "out": "[10, 99, 30]\n[10, 99, 30]\n[10, 20, 30, 40]",
     "why": "alias and raw name one list, so the change shows through both. copied is a separate outer list made before the change."},
    {"week": "w1-6", "title": "Shallow copy of nested lists", "code": '''\
raw = [[1, 2], [3, 4]]
copied = raw.copy()
copied[0][0] = 9
print(raw)
print(copied is raw, copied[0] is raw[0])''',
     "out": "[[9, 2], [3, 4]]\nFalse True",
     "why": "copy() makes a new outer list, but both outer lists hold the same inner lists. Mutating an inner list is visible through both."},
    {"week": "w1-6", "title": "A tuple holding a list", "code": '''\
record = ("A", [1, 2])
record[1].append(3)
print(record)''',
     "out": "('A', [1, 2, 3])",
     "why": "The tuple's slots can't be replaced, but the list inside is still mutable. record[0] = \"B\" would raise TypeError."},
    {"week": "w1-6", "title": "Before or after the recursive call", "code": '''\
def show(n):
    if n == 0:
        return
    show(n - 1)
    print(n)

show(3)''',
     "out": "1\n2\n3",
     "why": "Calls descend 3 → 2 → 1 → 0 before anything prints. The prints run while the calls return, so 1, 2, 3. Put print above the call to get 3, 2, 1."},
    {"week": "w1-6", "title": "Dictionary membership and get", "code": '''\
readings = {"P-01": 0.0, "P-02": 120.0}
print("P-01" in readings, 120.0 in readings)
print(readings.get("P-01"))
print(readings.get("P-03"))
print("P-03" in readings)''',
     "out": "True False\n0.0\nNone\nFalse",
     "why": "in checks keys, not values. The stored 0.0 is a real reading. get on a missing key returns None and does not insert it."},
    {"week": "w1-6", "title": "Iterative Fibonacci (course convention)", "code": '''\
def fib(n):
    previous, current = 1, 1
    for index in range(2, n + 1):
        previous, current = current, previous + current
    return current

print(fib(4), fib(5))''',
     "out": "5 8",
     "why": "The course uses F(0) = F(1) = 1. Pairs go (1,1) → (1,2) → (2,3) → (3,5) → (5,8)."},

    # ---------------- Week 7 ----------------
    {"week": "w7", "title": "The missing last load", "code": '''\
def total_load(loads_n):
    total_n = 0.0
    for index in range(len(loads_n) - 1):
        total_n += loads_n[index]
    return total_n

print(total_load([]))
print(total_load([5.0]))
print(total_load([2.0, 3.0, 4.0]))''',
     "out": "0.0\n0.0\n5.0",
     "why": "range(len - 1) stops one early. Empty: range(-1) is empty. Singleton: range(0) is empty, so 5.0 is lost. Three items: indices 0 and 1 only. Expected 0, 5, 9."},
    {"week": "w7", "title": "Accumulator reset inside the loop", "code": '''\
powers_kw = [1.0, 2.0, 3.0]
interval_h = 0.5
for power_kw in powers_kw:
    total_kwh = 0.0
    total_kwh += power_kw * interval_h
print("Final:", total_kwh, "kWh")''',
     "out": "Final: 1.5 kWh",
     "why": "The total is reset every pass, so only the last interval (3.0 × 0.5) survives. Initialise before the loop to get 3.0 kWh."},
    {"week": "w7", "title": "Exact equality on floats", "code": '''\
actual = 0.1 + 0.2
print(actual)
print(actual == 0.3)
print(abs(actual - 0.3) <= 1e-12)''',
     "out": "0.30000000000000004\nFalse\nTrue",
     "why": "0.1 and 0.2 are stored approximately in binary. Compare with an explicit tolerance instead of ==."},
    {"week": "w7", "title": "Which letters print?", "code": '''\
text = "bad"
try:
    print("A")
    value = float(text)
    print("B")
except ValueError:
    print("C")
print("D")''',
     "out": "A\nC\nD",
     "why": "A prints, the conversion fails, B is skipped, the handler prints C, then execution continues after the block with D. With \"12.5\" the output is A, B, D."},
    {"week": "w7", "title": "Two handlers, one route", "code": '''\
text = "0"
try:
    resistance_ohm = float(text)
    current_a = 12.0 / resistance_ohm
except ValueError:
    print("Resistance must be numerical.")
except ZeroDivisionError:
    print("Resistance cannot be zero.")
else:
    print(f"Current = {current_a:.2f} A")''',
     "out": "Resistance cannot be zero.",
     "why": "\"0\" parses fine, then dividing by zero raises ZeroDivisionError. Only the matching handler runs, and else is skipped. \"bad\" → first handler; \"4\" → Current = 3.00 A."},
    {"week": "w7", "title": "else and finally", "code": '''\
text = "bad"
try:
    value = float(text)
except ValueError:
    print("Cannot convert")
else:
    print("Converted", value)
finally:
    print("Check finished")''',
     "out": "Cannot convert\nCheck finished",
     "why": "The failure skips else. finally runs on both routes, so it marks cleanup, not success."},
    {"week": "w7", "title": "Aliasing breaks a non-mutation promise", "code": '''\
def corrected(raw_c, offset_c):
    processed = raw_c
    for i in range(len(processed)):
        processed[i] -= offset_c
    return processed

raw_c = [22.0, 23.0]
result = corrected(raw_c, 0.5)
print(raw_c)
print(result)''',
     "out": "[21.5, 22.5]\n[21.5, 22.5]",
     "why": "processed = raw_c is an alias, so the caller's list is changed too. Use raw_c.copy() inside the function."},
    {"week": "w7", "title": "Broad handler fabricates data", "code": '''\
def hidden_failure(force_n, area_m2):
    try:
        return force_n / area_m2
    except Exception:
        return 0.0

print(hidden_failure(100.0, 0.0))''',
     "out": "0.0",
     "why": "Division by zero is hidden and reported as 0.0 Pa, which looks like an unloaded part. Reject invalid area explicitly instead."},
    {"week": "w7", "title": "Internal counting invariant", "code": '''\
readings_c = [19.0, 22.0, 31.0]
normal = 0
warning = 0
for value_c in readings_c:
    if 20.0 <= value_c <= 30.0:
        normal += 1
    else:
        warning += 1
assert normal + warning == len(readings_c)
print(normal, warning)''',
     "out": "1 2",
     "why": "19 and 31 are warnings, 22 is normal. The assert checks every reading went to exactly one group, not that the thresholds are right."},
    {"week": "w7", "title": "Parseable is not finite", "code": '''\
import math
for text in ["12.5", "nan", "inf"]:
    value = float(text)
    print(text, math.isfinite(value))''',
     "out": "12.5 True\nnan False\ninf False",
     "why": "All three strings convert with float(). Only 12.5 is a finite reading."},

    # ---------------- Week 9 ----------------
    {"week": "w9", "title": "Saved query vs live state", "code": '''\
class IntroSensor:
    def __init__(self, value, lower, upper):
        self.value = value
        self.lower = lower
        self.upper = upper
    def is_safe(self):
        return self.lower <= self.value <= self.upper
    def update(self, new_value):
        self.value = new_value

s = IntroSensor(25.0, 20.0, 30.0)
old_ok = s.is_safe()
result = s.update(35.0)
print(old_ok, s.is_safe(), result)''',
     "out": "True False None",
     "why": "old_ok was computed at 25.0 and doesn't recompute. The new query sees 35.0. update has no return, so result is None."},
    {"week": "w9", "title": "Alias of an object", "code": '''\
class IntroSensor:
    def __init__(self, value):
        self.value = value
    def update(self, new_value):
        self.value = new_value

a = IntroSensor(25.0)
b = a
answer = b.update(35.0)
print(a.value, b.value, answer)''',
     "out": "35.0 35.0 None",
     "why": "b = a gives a second name for the same sensor. The update shows through both names. The method returns None."},
    {"week": "w9", "title": "Class default and instance override", "code": '''\
class Display:
    digits = 1

a = Display()
b = Display()
a.digits = 3
Display.digits = 2
print(a.digits, b.digits, Display.digits)''',
     "out": "3 2 2",
     "why": "a has its own attribute 3, which shadows the class. b has none, so lookup falls back to the class value, now 2."},
    {"week": "w9", "title": "Deleting an override", "code": '''\
class Display:
    digits = 2

a = Display()
b = Display()
a.digits = 4
Display.digits = 1
print(a.digits, b.digits)
del a.digits
print(a.digits, b.digits)''',
     "out": "4 1\n1 1",
     "why": "del removes only a's instance attribute. Lookup then reaches the class value 1."},
    {"week": "w9", "title": "Shared mutable class attribute", "code": '''\
class BadLog:
    history = []
    def add(self, value):
        self.history.append(value)

class GoodLog:
    def __init__(self):
        self.history = []
    def add(self, value):
        self.history.append(value)

a, b = BadLog(), BadLog()
a.add(1)
print("Shared:", b.history)
c, d = GoodLog(), GoodLog()
c.add(1)
print("Independent:", d.history)''',
     "out": "Shared: [1]\nIndependent: []",
     "why": "BadLog's single list belongs to the class, so every instance appends to it. GoodLog makes a new list per instance in __init__."},
    {"week": "w9", "title": "The wrong counter", "code": '''\
class Reading:
    total_created = 0
    def __init__(self, value):
        self.value = value
        self.total_created += 1

r1 = Reading(10)
r2 = Reading(20)
print(Reading.total_created, r1.total_created, r2.total_created)''',
     "out": "0 1 1",
     "why": "self.total_created += 1 reads the class 0, then creates an instance attribute 1 on each object. The class counter never changes. Write Reading.total_created += 1."},
    {"week": "w9", "title": "super() and isinstance", "code": '''\
class Sensor:
    def __init__(self, name, unit):
        self.name = name
        self.unit = unit
    def report(self):
        return f"{self.name} [{self.unit}]"

class TemperatureSensor(Sensor):
    def __init__(self, name):
        super().__init__(name, "deg C")
    def report(self):
        return "Temperature | " + super().report()

t = TemperatureSensor("Tank")
print(t.report())
print(isinstance(t, Sensor), type(t) is Sensor)''',
     "out": "Temperature | Tank [deg C]\nTrue False",
     "why": "super().__init__ sets name and unit on t itself. The child report reuses the parent string. t is a Sensor by isinstance, but its exact type is TemperatureSensor."},
    {"week": "w9", "title": "Polymorphic reporting loop", "code": '''\
class Sensor:
    def report(self):
        return "generic"

class Pressure(Sensor):
    def report(self):
        return "pressure"

class Temperature(Sensor):
    pass

for s in [Sensor(), Pressure(), Temperature()]:
    print(s.report())''',
     "out": "generic\npressure\ngeneric",
     "why": "Each object uses the report of its own class. Temperature defines none, so it inherits Sensor's."},
    {"week": "w9", "title": "Override that prints", "code": '''\
class Sensor:
    def report(self):
        return "Tank: 25.0"

class Loud(Sensor):
    def report(self):
        print(super().report())

reports = []
reports.append(Loud().report())
print(reports)''',
     "out": "Tank: 25.0\n[None]",
     "why": "The override prints the text but returns None, so None is appended. Fix: return super().report()."},
    {"week": "w9", "title": "Rejected setter keeps old state", "code": '''\
import math
class Sensor:
    def __init__(self, value):
        self._value = 0.0
        self.set_value(value)
    def get_value(self):
        return self._value
    def set_value(self, proposed):
        if isinstance(proposed, bool) or not isinstance(proposed, (int, float)):
            raise TypeError("reading must be a number")
        if not math.isfinite(proposed):
            raise ValueError("reading must be finite")
        self._value = float(proposed)

s = Sensor(25.0)
try:
    s.set_value(float("nan"))
except ValueError:
    print("rejected")
print(s.get_value())''',
     "out": "rejected\n25.0",
     "why": "Validation raises before the assignment, so 25.0 survives. A valid 35.0 would be stored (and simply be outside limits)."},

    # ---------------- Week 10 ----------------
    {"week": "w10", "title": "Fixed inner loop", "code": '''\
n = 4
visits = 0
for i in range(n):
    for j in range(5):
        visits += 1
print(visits)''',
     "out": "20",
     "why": "5n = 20. The inner loop never grows with n, so this is Θ(n) despite two loop levels."},
    {"week": "w10", "title": "Triangular loop", "code": '''\
n = 5
visits = 0
for i in range(n):
    for j in range(i):
        visits += 1
print(visits)''',
     "out": "10",
     "why": "Inner lengths 0 + 1 + 2 + 3 + 4 = n(n−1)/2 = 10. Θ(n²)."},
    {"week": "w10", "title": "Warnings vs comparisons", "code": '''\
def count_warnings(readings, limit):
    warnings = 0
    comparisons = 0
    for value in readings:
        comparisons += 1
        if value > limit:
            warnings += 1
    return warnings, comparisons

print(count_warnings([20.0, 30.0, 28.0, 30.0, 25.0], 30.0))''',
     "out": "(0, 5)",
     "why": "Nothing is strictly above 30, but all 5 comparisons were needed to know that."},
    {"week": "w10", "title": "Floor halving", "code": '''\
n = 10
steps = 0
while n > 1:
    n //= 2
    steps += 1
print(steps)''',
     "out": "3",
     "why": "10 → 5 → 2 → 1: three body passes, ⌊log₂ 10⌋ = 3."},
    {"week": "w10", "title": "Counting naive Fibonacci calls", "code": '''\
calls = 0
def fib(n):
    global calls
    calls += 1
    if n <= 1:
        return 1
    return fib(n - 1) + fib(n - 2)

print(fib(5), calls)''',
     "out": "8 15",
     "why": "F(5) = 8 and the call tree has 2·F(5) − 1 = 15 calls. Overlapping subproblems make it exponential."},

    # ---------------- Week 11 ----------------
    {"week": "w11", "title": "Shrinking workload", "code": '''\
size = 8
visits = 0
while size > 0:
    for _ in range(size):
        visits += 1
    size //= 2
print(visits)''',
     "out": "15",
     "why": "8 + 4 + 2 + 1 = 15, always less than 2n. Θ(n), not n log n."},
    {"week": "w11", "title": "Memoized Fibonacci", "code": '''\
def cached(n, cache):
    if n not in cache:
        cache[n] = cached(n - 1, cache) + cached(n - 2, cache)
    return cache[n]

cache = {0: 1, 1: 1}
print(cached(5, cache))
print(sorted(cache.items()))''',
     "out": "8\n[(0, 1), (1, 1), (2, 2), (3, 3), (4, 5), (5, 8)]",
     "why": "Each missing state is computed once and stored, so a fresh request does linear work. Asking for 5 again is a warm hit."},
    {"week": "w11", "title": "Index vs slice recursion", "code": '''\
def sum_index(values, index=0):
    if index == len(values):
        return 0
    return values[index] + sum_index(values, index + 1)

def sum_slice(values):
    if not values:
        return 0
    return values[0] + sum_slice(values[1:])

print(sum_index([1, 2, 3]), sum_slice([1, 2, 3]))''',
     "out": "6 6",
     "why": "Same answer, different memory. sum_slice copies a new tail each call (quadratic total copying) and waiting frames keep those tails alive."},
    {"week": "w11", "title": "Running window loses information", "code": '''\
def direct(values, w):
    return [sum(values[s:s + w]) / w for s in range(len(values) - w + 1)]

def running(values, w):
    total = sum(values[:w])
    means = [total / w]
    for end in range(w, len(values)):
        total -= values[end - w]
        total += values[end]
        means.append(total / w)
    return means

values = [1e16, 1.0, 1.0]
print(direct(values, 2))
print(running(values, 2))''',
     "out": "[5000000000000000.0, 1.0]\n[5000000000000000.0, 0.5]",
     "why": "1e16 + 1.0 rounds to 1e16, so the 1.0 is lost. Subtracting 1e16 later can't bring it back. Algebraically equal is not numerically equal."},
    {"week": "w11", "title": "Index once, flag every record", "code": '''\
installed = ["A", "B", "A", "C"]
approved = ["A", "C"]
index = {}
for name in approved:
    index[name] = True
flags = []
for name in installed:
    flags.append(name in index)
print(flags)''',
     "out": "[True, False, True, True]",
     "why": "Build the dict once (m work), then each lookup is expected O(1). One flag per installed record, repeats included."},

    # ---------------- Week 12 ----------------
    {"week": "w12", "title": "Index zero is a success", "code": '''\
def linear_search(values, target):
    for index, value in enumerate(values):
        if value == target:
            return index
    return None

index = linear_search(["A", "B", "A"], "A")
print(index, bool(index), index is not None)
print(linear_search(["A", "B"], "C"))''',
     "out": "0 False True\nNone",
     "why": "The first A is at 0, which is falsy. Test is not None. Absence returns None only after every position fails."},
    {"week": "w12", "title": "Binary search trace", "code": '''\
def binary_search(values, target):
    low, high = 0, len(values) - 1
    while low <= high:
        mid = (low + high) // 2
        print("mid", mid)
        if values[mid] == target:
            return mid
        if values[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return None

print(binary_search([8, 12, 18, 22, 31, 40, 55], 31))''',
     "out": "mid 3\nmid 5\nmid 4\n4",
     "why": "22 < 31 → low 4. 40 > 31 → high 4. Single candidate at 4 still gets checked (that's why the condition is <=)."},
    {"week": "w12", "title": "Insertion position is not membership", "code": '''\
from bisect import bisect_left
values = [10, 20, 30]
pos = bisect_left(values, 40)
found = pos < len(values) and values[pos] == 40
print(pos)
print(found)''',
     "out": "3\nFalse",
     "why": "40 would go at position 3 = len(values). The bounds test is False, so and short-circuits and values[3] is never read (it would raise IndexError)."},
    {"week": "w12", "title": "sorted() vs .sort()", "code": '''\
raw = [3, 1, 2, 1]
ranked = sorted(raw)
result = raw.sort()
print(ranked, raw, result)''',
     "out": "[1, 1, 2, 3] [1, 1, 2, 3] None",
     "why": "sorted returns a new list. raw.sort() then reorders raw itself and returns None."},
    {"week": "w12", "title": "Stable sort by one key", "code": '''\
records = [("A", 2), ("B", 1), ("C", 1)]
def key(record):
    return record[1]

print(sorted(records, key=key))
print(records)''',
     "out": "[('B', 1), ('C', 1), ('A', 2)]\n[('A', 2), ('B', 1), ('C', 1)]",
     "why": "B and C tie on key 1 and keep their input order (stability). sorted leaves the original list alone."},
    {"week": "w12", "title": "Merge with ties and tails", "code": '''\
def merge(left, right):
    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

print(merge([1, 3, 3], [2, 3, 4]))''',
     "out": "[1, 2, 3, 3, 3, 4]",
     "why": "Take 1 (L), 2 (R), 3 (L), 3 (L, ties go left). Left is empty, so append the right tail [3, 4]."},
    {"week": "w12", "title": "First selection-sort pass", "code": '''\
values = [4, 1, 3, 1]
smallest = 0
for index in range(1, len(values)):
    if values[index] < values[smallest]:
        smallest = index
values[0], values[smallest] = values[smallest], values[0]
print(smallest, values)''',
     "out": "1 [1, 4, 3, 1]",
     "why": "The strict < keeps the first minimum (index 1); the later 1 is equal, not smaller."},
    {"week": "w12", "title": "Sort complete records", "code": '''\
materials = [("steel", 7850), ("aluminum", 2700), ("copper", 8960)]
for name, density in sorted(materials, key=lambda r: r[1], reverse=True):
    print(name, density)''',
     "out": "copper 8960\nsteel 7850\naluminum 2700",
     "why": "The key compares densities but each tuple moves as a whole, so names stay attached."},

    # ---------------- Week 13 ----------------
    {"week": "w13", "title": "Integer division before conversion", "code": '''\
a = float(7 // 2)
b = 7 / 2
print(a, b)
print(3 ^ 2, 3 ** 2)''',
     "out": "3.0 3.5\n1 9",
     "why": "float(7 // 2) converts an already floored 3. This mirrors double a = 7 / 2; in C++/Java. ^ is bitwise XOR (011 ^ 010 = 001), ** is power."},
    {"week": "w13", "title": "Cooling recurrence sample count", "code": '''\
temperature_c = 100.0
ambient_c = 25.0
k = 0.05
dt = 1.0
samples = [temperature_c]
for _ in range(100):
    temperature_c -= dt * k * (temperature_c - ambient_c)
    samples.append(temperature_c)
print(len(samples), samples[1])''',
     "out": "101 96.25",
     "why": "Initial value + 100 updates = 101 samples. First update: 100 − 0.05·75 = 96.25 (Python index 1, MATLAB position 2)."},
    {"week": "w13", "title": "Python list alias (like a Java array)", "code": '''\
a = [10.0, 20.0]
b = a
b[0] = 99.0
c = list(a)
c[1] = 0.0
print(a, b is a, c)''',
     "out": "[99.0, 20.0] True [99.0, 0.0]",
     "why": "b = a aliases (Java arrays behave the same way). list(a) builds a new list, like a C++ vector copy."},

    # ---------------- Week 14 ----------------
    {"week": "w14", "title": "The seven-record pipeline", "code": '''\
import math
RAW = ["T-01,19.5,C", "T-02,20.0,C", "T-03,25.0,C", "T-04,30.0,C",
       "T-05,30.5,C", "T-06,bad,C", "T-07,300.0,K"]

def parse(text):
    parts = text.split(",")
    if len(parts) != 3:
        raise ValueError("expected three fields")
    name, value_text, unit = [p.strip() for p in parts]
    if not name or unit != "C":
        raise ValueError("need ID and unit C")
    value = float(value_text)
    if not math.isfinite(value):
        raise ValueError("not finite")
    return name, value

accepted, rejected = [], []
for i, raw in enumerate(RAW):
    try:
        name, value = parse(raw)
    except ValueError:
        rejected.append(i)
    else:
        accepted.append((i, name, value))
mean = sum(r[2] for r in accepted) / len(accepted)
warnings = [r[0] for r in accepted if not 20 <= r[2] <= 30]
print(len(accepted), rejected, mean, warnings)''',
     "out": "5 [5, 6] 25.0 [0, 4]",
     "why": "\"bad\" fails float(); K fails the unit check. Five accepted values sum to 125, mean 25.0. Indices 0 and 4 are valid but outside 20–30."},
]
