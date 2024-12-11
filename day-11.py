import sys

input = []

pair_mappings = {}

def apply_rule(num):
    if num == 0:
        return [1]
    if len(str(num)) % 2 == 0:
            
        left_num = -1
        right_num = -1
        str_num = str(num)
        left_num = int(str_num[:int(len(str_num)/2)])
        right_num = int(str_num[int(len(str_num)/2):])
        #if(num == 24 or num == 20):
        #    print(f"found {num}, its left and right are {left_num} and {right_num}")
        return [left_num, right_num]
    #if num == 1:
    #    print(f"Found {num}, multiply by 2024")
    return [num * 2024]

def debug_stones(stone_counts):
    stones = []
    for count in stone_counts:
        if stone_counts[count] > 0:
            if count == 1:
                print(f"1 was present in the final expansion, it had: {stone_counts[count]}")
            for n in range(stone_counts[count]):
                stones.append(count)
    print(stone_counts)
    print(stones)

def get_resulting_from_stone_iter(start_stone, num_iter):
    stone_counts = {start_stone:1}
    for i in range(num_iter):
        new_stone_counts = {}
        stone_counts_copy = stone_counts.copy()
        for stone in stone_counts.keys():
            num_of_current_stone = stone_counts[stone]
            if num_of_current_stone > 0:
                stone_results = apply_rule(stone)
                for rule_result in stone_results:
                    if rule_result in new_stone_counts:
                        new_stone_counts[rule_result] += num_of_current_stone
                    else:
                        new_stone_counts[rule_result] = num_of_current_stone
        stone_counts = new_stone_counts
        #debug_stones(stone_counts_copy)
    return sum(stone_counts_copy.values())
    

def handle(line):
    if line != "":
        input.append([int(x) for x in line.split()])
    
for line in sys.stdin:
    if(line[:-1] == '' and lastline == ''):
        print("should be ending stdin")
        break
    else:
        handle(line[:-1])
        lastline = line[:-1]


print(input[0])

current_stones = input[0]

for i in range(25):
    new_stones = []
    for stone in current_stones:
        new_stones += apply_rule(stone)
    current_stones = new_stones

print(len(current_stones))

answer = 0
stones_2 = input[0]
for stone in stones_2:
        answer += get_resulting_from_stone_iter(stone, 76)
    

#for key in pair_mappings:
#    print(f"{key} {pair_mappings[key]}")
#print(len(pair_mappings))
print(answer)