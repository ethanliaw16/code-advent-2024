import sys
from functools import cmp_to_key

rules_dict = {}
input = []
input_2 = []
def handle(line):
    if(line == ""):
        return 0
    if "|" in line:
        input.append(line.split("|"))
        rule_pair = line.split("|")
        if int(rule_pair[0]) in rules_dict:
            rules_dict[int(rule_pair[0])].append(int(rule_pair[1]))
        else:
            rules_dict[int(rule_pair[0])] = [int(rule_pair[1])]
    elif "," in line: 
        input_2.append([int(x) for x in line.split(",")])
    return 1

def without_nth_item(n, lst):
    return lst[:n] + lst[n+1:]

def line_without_newline(line):
    return line[:-1]

def is_ordered(list):
    #print(f"checking {list}")
    answer_if_in_order = list[int(len(list) / 2)]
    current = list[0]
    for i in range(len(list) - 1):
        to_compare = list[i + 1]
        if(to_compare in rules_dict):
            #print(f"found rule {to_compare}-> {rules_dict[to_compare]}")
            if current in rules_dict[to_compare]:
                #print(f"{list} not in order because of rule {to_compare} -> {rules_dict[to_compare]}")
                return 0
        current = to_compare
    return answer_if_in_order

sum = 0
lastline='a'
for line in sys.stdin:
    if(line[:-1] == '' and lastline == ''):
        print("should be ending stdin")
        break
    else:
        sum += handle(line_without_newline(line))
        lastline = line[:-1]

def compare(num_1, num_2):
    if num_1 in rules_dict:
        if num_2 in rules_dict[num_1]:
            return -1
    return 1
     

i = 0

distances = 0

#for y in range(len(input)):
#    for x in range(len(input[0])):
#        i += num_xmas(y, x, input, height, width)

i = 0
j = 0

unordered  = []
for list in input_2:
    result = is_ordered(list)
    i += is_ordered(list)
    if result == 0:
        unordered.append(list)

for list in unordered:
    sorted_list = sorted(list, key=cmp_to_key(compare))
    j += sorted_list[int(len(sorted_list) / 2)]

print(f"{j}")
    