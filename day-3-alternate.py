
def get_instruction(line):
    if not "," in line:
        return [0,0]
    if len(line.split(",")) > 2:
        return [0,0]
    nums = line.split(",")
    if not (nums[0].isdigit() and nums[1].isdigit()):
        return [0,0]
    return[int(nums[0]), int(nums[1])]

with open('day-3-input.txt', 'r') as file:
    # Read the entire contents of the file as a string
    input = file.read()
    #input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    #input = small_input
    enabled = True
    result = 0
    
    tokenized_by_paren = [x.split(")")[0][1:] for x in input.split("mul")]
    
    for line in tokenized_by_paren:
        instruction = get_instruction(line)
        result += instruction[0] * instruction[1]
    
    result_2 = 0
    tokenized_by_do_dont = [x.split("don't()")[0] for x in input.split("do()")]
    for set in tokenized_by_do_dont:
        set_by_paren = [x.split(")")[0][1:] for x in set.split("mul")]
        for line in set_by_paren:
            instruction = get_instruction(line)
            result_2 += instruction[0] * instruction[1]
    print(f"input length {len(input)}")
    print(result) 
    print(result_2)