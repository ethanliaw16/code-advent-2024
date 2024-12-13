import sys

input = []
current_machine_input = {"Ax":0, "Ay":0}

def handle(line):
    input.append(line)
        #if "Button A" in line:
        #    coords = [int(x) for x in line.split("A: ")[1].replace("X","").replace("Y","").replace("+","").split(", ")]
        #    current_machine_input["Ax"] = coords[0]
        #    current_machine_input["Ay"] = coords[1]
        #if "Button B" in line:
        #    coords = [int(x) for x in line.split("B: ")[1].replace("X","").replace("Y","").replace("+","").split(", ")]
        #    current_machine_input["Bx"] = coords[0]
        #    current_machine_input["By"] = coords[1]
        #elif "Prize: " in line:
        #    coords = [int(x) for x in line.split("Prize: ")[1].replace("X","").replace("Y","").replace("=","")]
        #    current_machine_input["PrizeX"] = coords[0]
        #    current_machine_input["PrizeY"] = coords[1]
    
        
sum = 0
lastline='a'
for line in sys.stdin:
    if(line[:-1] == '' and lastline == ''):
        print("should be ending stdin")
        break
    else:
        handle(line[:-1])
        lastline = line[:-1]

machines = []
for line in input:
    if "Button A" in line:
        coords = [int(x) for x in line.split("A: ")[1].replace("X","").replace("Y","").replace("+","").split(", ")]
        current_machine_input["Ax"] = coords[0]
        current_machine_input["Ay"] = coords[1]
    if "Button B" in line:
        coords = [int(x) for x in line.split("B: ")[1].replace("X","").replace("Y","").replace("+","").split(", ")]
        current_machine_input["Bx"] = coords[0]
        current_machine_input["By"] = coords[1]
    if "Prize: " in line:
        coords = [int(x) for x in line.split("Prize: ")[1].replace("X","").replace("Y","").replace("=","").split(", ")]
        current_machine_input["PrizeX"] = coords[0]
        current_machine_input["PrizeY"] = coords[1]
    if line == "":
        machines.append(current_machine_input)
        current_machine_input = {}

def get_result(num_a, num_b, machine):
    x = num_a * machine["Ax"] + num_b * machine["Bx"]
    y = num_a * machine["Ay"] + num_b * machine["By"]
    return [x,y]

answer = 0
for machine in machines:
    b = (machine["PrizeY"] * machine["Ax"] - machine["PrizeX"] * machine["Ay"]) / (machine["By"] * machine["Ax"] - machine["Bx"] * machine["Ay"])
    a = (machine["PrizeX"] - b * machine["Bx"]) / machine["Ax"]
    if(a == int(a) and b == int(b)):
        answer += 3 * int(a) + int(b)
    

print(answer)

answer = 0
for machine in machines:
    machine["PrizeX"] += 10000000000000
    machine["PrizeY"] += 10000000000000
    b = (machine["PrizeY"] * machine["Ax"] - machine["PrizeX"] * machine["Ay"]) / (machine["By"] * machine["Ax"] - machine["Bx"] * machine["Ay"])
    a = (machine["PrizeX"] - b * machine["Bx"]) / machine["Ax"]
    #print(f"expected nums are A {a} and B {b}")
    if(a == int(a) and b == int(b)):
        answer += 3 * int(a) + int(b)
print(answer)

