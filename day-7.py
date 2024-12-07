import sys
import itertools

input = {}

def generate_permutations(n):
    # Create a list containing n items (either '+' or '*')
    items = ['+', '*', "|"]
    
    # Use itertools.product to generate all permutations of size n
    permutations = itertools.product(items, repeat=n)
    
    # Convert each tuple into a string and return the list
    return [''.join(p) for p in permutations]

def line_without_newline(line):
    return line[:-1]

def apply_operators(operators, vals):
    current = vals[0]
    for i in range(len(operators)):
        if operators[i] == "+":
            current += vals[i + 1]
        elif operators[i] == "*":
            current *= vals[i + 1]
        else:
            left_half = str(current)
            current = int(left_half + str(vals[i + 1]))

    #print(f"{operators} on {vals} made {current}!")
    return current

def can_make_num(target, vals):
    possible_operators = generate_permutations(len(vals) - 1)
    for operators in possible_operators:
        result_of_operators = apply_operators(operators, vals)
        if result_of_operators == target:
            print(f"{operators} on {vals} made {target}!")
            return result_of_operators
    return 0

def handle(line):
    if(line == ""):
        return 0
    key = int(line.split(": ")[0])
    vals = [int(x) for x in (line.split(": ")[1].split())]
    input[key] = vals
    return 1

sum = 0
lastline='a'
for line in sys.stdin:
    if(line[:-1] == '' and lastline == ''):
        print("should be ending stdin")
        break
    else:
        handle(line_without_newline(line))
        lastline = line[:-1]

for key in input:
    sum += can_make_num(key, input[key])

print(sum)