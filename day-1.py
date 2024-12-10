import sys


left = []
right = []


def handle(line):
    if(line == ""):
        return 0
    split_input = line.split()
    left.append(int(split_input[0]))
    right.append(int(split_input[1]))
    return 1

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

good_input = []

def num_instances(target, list):
    return len([x for x in list if x == target])

left_1 = left
right_1 = right

left_1.sort()
right_1.sort()
answer = 0
for i in range(len(left)):
    answer += abs(left_1[i] - right_1[i])

print(answer)

for i in range(len(left)):
    good_input.append([left[i], right[i]])
    i += 1

distances = 0
for item in left:
    distances += item * num_instances(item, right) 
print(distances)
    