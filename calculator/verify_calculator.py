"""
Headless unit verification script for the Calculator logic.
Validates all operations, edge cases, and arithmetic requirements.
"""

def simulate_calc(operations):
    current = '0'
    previous = ''
    op = None
    should_reset = False

    def append_num(n):
        nonlocal current, should_reset
        if should_reset:
            current = ''
            should_reset = False
        if n == '.':
            if '.' in current:
                return
            if current == '' or current == '0':
                current = '0.'
                return
        if current == '0' and n != '.':
            current = n
        else:
            current += n

    def choose_op(new_op):
        nonlocal current, previous, op, should_reset
        if current == '' and previous != '':
            op = new_op
            return
        if previous != '' and current != '':
            compute()
        op = new_op
        previous = current
        current = ''
        should_reset = False

    def compute():
        nonlocal current, previous, op, should_reset
        if previous == '' or current == '':
            return
        p = float(previous)
        c = float(current)
        if op == '+':
            res = p + c
        elif op in ('−', '-'):
            res = p - c
        elif op in ('×', '*'):
            res = p * c
        elif op in ('÷', '/'):
            if c == 0:
                current = 'Cannot divide by 0'
                previous = ''
                op = None
                should_reset = True
                return
            res = p / c
        else:
            return
        res = round(res + 1e-15, 12)
        if res.is_integer():
            current = str(int(res))
        else:
            current = str(res).rstrip('0').rstrip('.')
        op = None
        previous = ''
        should_reset = True

    def delete():
        nonlocal current, should_reset
        if should_reset:
            current = '0'
            should_reset = False
            return
        if current in ('0', 'Cannot divide by 0', 'Error'):
            current = '0'
            return
        if len(current) <= 1 or (len(current) == 2 and current.startswith('-')):
            current = '0'
        else:
            current = current[:-1]

    for item in operations:
        if item in ['0','1','2','3','4','5','6','7','8','9','.']:
            append_num(item)
        elif item in ['+', '-', '−', '*', '×', '/', '÷']:
            choose_op(item)
        elif item == '=':
            compute()
        elif item == 'AC':
            current = '0'
            previous = ''
            op = None
            should_reset = False
        elif item == 'DEL':
            delete()
        elif item == '%':
            current = str(float(current) / 100)
        elif item == '±':
            if current.startswith('-'):
                current = current[1:]
            elif current != '0':
                current = '-' + current

    return current

# Test suite
tests = [
    (["7", "+", "5", "="], "12"),
    (["1", "5", "−", "8", "="], "7"),
    (["9", "×", "6", "="], "54"),
    (["8", "4", "÷", "4", "="], "21"),
    (["1", "0", "÷", "0", "="], "Cannot divide by 0"),
    (["0", ".", "1", "+", "0", ".", "2", "="], "0.3"),
    (["5", "0", "%"], "0.5"),
    (["5", "±"], "-5"),
    (["1", ".", "2", ".", "3"], "1.23"),
    (["2", "+", "3", "+", "4", "="], "9"),
    (["5", "+", "×", "3", "="], "15"), # Operator replacement test
    (["5", "±", "DEL"], "0"),           # Negative single digit delete test
]

all_passed = True
print("Running Calculator Logic Unit Tests...")
for inputs, expected in tests:
    result = simulate_calc(inputs)
    passed = (result == expected)
    if not passed:
        all_passed = False
        print(f"FAILED: {' '.join(inputs)} -> got '{result}', expected '{expected}'")
    else:
        print(f"PASSED: {' '.join(inputs)} = {result}")

if all_passed:
    print("\nALL 12 UNIT TESTS PASSED SUCCESSFULLY!")
else:
    exit(1)
