import sys


left = []
right = []
input = []

def handle(line):
    if(line == ""):
        return 0
    input.append([int(x) for x in line.split()])
    return 1

def is_increasing(list):
    last = list[0]
    for i in list[1:]:
        if i <= last:
            return False
        if abs(last - i) < 1 or abs(last - i) > 3:
            return False
        last = i
    return True

def is_valid(list):
    reversed_full = list[::-1]
    if(is_increasing(list) or is_increasing(reversed_full)):
        return True
    for i in range(len(list)):
        with_removed = without_nth_item(i, list)
        with_removed_reversed = with_removed[::-1]
        if is_increasing(with_removed) or is_increasing(with_removed_reversed):
            return True
    return False

def without_nth_item(n, lst):
    return lst[:n] + lst[n+1:]

def line_without_newline(line):
    return line[:-1]

sum = 0
lastline='a'
for line in sys.stdin:
    if(line[:-1] == '' and lastline == ''):
        print("should be ending stdin")
        break
    else:
        sum += handle(line_without_newline(line))
        lastline = line[:-1]

i = 0


def num_instances(target, list):
    return len([x for x in list if x == target])


distances = 0
for item in input:
    valid = is_valid(item)
    if(valid):
        distances += 1
print(distances)
    