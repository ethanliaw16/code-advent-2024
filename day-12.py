import sys

#Something I was considering after gpt suggested it. 
#however  I forgot to convey in the prompt that a field is not necessarily convex so Convexhull doesn't work. 
#from scipy.spatial import ConvexHull

input = []
visited = []
fields = []

#To get the Fields: for each square on the plot, find the next square that hasn't yet been visited or assigned to a field,
# and make it its own new field. Take each of its valid (in-bounds and unused) neighbors and queue them up to add to the field
# and subsequently queue up its neighbors and so on. Field is completed when the queue of neighbors runs empty. 

#Area is just the size of the list of points representing the field.
#To get the perimeter, take every point in the field, and look at its N,S,E,W neighbors. 
#For each neighbor, if the neighbor is OB or not the same veg as the field then add 1 to the perimeter. 

#To get the number of sides, take vertical and horizontal slices of the field. For each slice,
#Check how many contiguous segments are present on that row/column which consist of the field's edge squares 
# An edge square is (any square who yielded more than 0 in the perimeter  calculation earlier)
#The total count of segments formed by edge squares that lie on all horizontal and vertical slices is the number of sides for the field.

#Caveat with this method: You need to be able to account for a square being both a left- and right- edge for vertical slice,
#and both a top- or bottom- edge for a horizontal slice. At first I couldn't think of a way to check which that it was
#without writing something really crude and messy. Eventually, I resorted to eliminating that  possibility by scaling the original 
# map size up by 3x. With the scaled up Map, a single square that had two edges previously now becomes a 3x3 region, so the 
# edge cannot be both top/bottom or right/left.  Additionally,  there are no more 1-length segments, so you only need to consider 
#segments lying on the slice that are greater than 1. *This is mind-numbingly slow and definitely not the right way to go about 
#reconciling a problem as small as this.
#
#The final solve uses the originally scaled map, and for each field keeps a dictionary to handle the edges.
#Keys are the direction relative to the point that the fence is positioned, i.e. Top, bottom, left, right. Values are lists 
#of the field's edge points which have the neighbor property. 
# 
# So in the example below, the the square at "a" results in the entry {"Top"->[1,2]} since it is a border from its top side.
##.01234
#0......
#1..AaA.
#2..AAA.
#3..AAA.
#4......

#Using the dictionary mapping what kind of edge each point is, run through each horizontal and vertical slice twice, 
#We collect segments that lie on that row/column for both the left/right edges and the top/right edges independently. 

big_input = []

#for iteration purposes. used 600 due to needing to use this for the scaled up map.
def field_max_min(field):
    min_x = 600
    max_x = 0
    min_y = 600
    max_y = 0
    for point in field:
        min_x = min(min_x, point[1])
        max_x = max(max_x, point[1])
        min_y = min(min_y, point[0])
        max_y = max(max_y, point[0])
    return [min_y, min_x, max_y, max_x]

def get_vert_segments(points, edge_dict, column):
    used_left = []
    used_right = []
    num_segments = 0
    for point in points:
        if point not in used_left:
            if point[1] == column and point in edge_dict["left"]:
                point_up = [point[0] - 1, point[1]]
                point_down = [point[0] + 1, point[1]]
                used_left.append(point)
                up_seg = []
                down_seg = []
                while point_up in points and point_up not in used_left and point_up in edge_dict["left"]:
                    up_seg.append(point_up)
                    used_left.append(point_up)
                    point_up = [point_up[0] - 1, point_up[1]]
                while point_down in points and point_down not in used_left and point_down in edge_dict["left"]:
                    down_seg.append(point_down)
                    used_left.append(point_down)
                    point_down = [point_down[0] + 1, point_down[1]]
                seg = up_seg + [point] + down_seg
                if len(seg) > 0:
                    #print(f"left seg {seg}")
                    num_segments += 1

        if point not in used_right:
            if point[1] == column and point in edge_dict["right"]:
                point_up = [point[0] - 1, point[1]]
                point_down = [point[0] + 1, point[1]]
                used_right.append(point)
                up_seg = []
                down_seg = []
                while point_up in points and point_up not in used_right and point_up in edge_dict["right"]:
                    up_seg.append(point_up)
                    used_right.append(point_up)
                    point_up = [point_up[0] - 1, point_up[1]]
                while point_down in points and point_down not in used_right and point_down in edge_dict["right"]:
                    down_seg.append(point_down)
                    used_right.append(point_down)
                    point_down = [point_down[0] + 1, point_down[1]]
                seg = up_seg + [point] + down_seg
                if len(seg) > 0:
                    #print(f"right seg {seg}")
                    num_segments += 1
    return num_segments

def get_horizontal_segments(points, edge_dict, row):
    used_top = []
    used_bottom = []
    num_segments = 0
    for point in points:
        if point not in used_top:
            if point[0] == row and point in edge_dict["top"]:
                point_left = [point[0], point[1] - 1]
                point_right = [point[0], point[1] + 1]
                used_top.append(point)
                left_seg = []
                right_seg = []
                while point_left in points and not point_left in used_top and point_left in edge_dict["top"]:
                    left_seg.append(point_left)
                    used_top.append(point_left)
                    point_left = [point_left[0], point_left[1] - 1]
                while point_right in points and not point_right in used_top and point_right in edge_dict["top"]:
                    right_seg.append(point_right)
                    used_top.append(point_right)
                    point_right = [point_right[0], point_right[1] + 1]
                seg = [point] + left_seg + right_seg
                if len(seg) > 0:
                    #print(f"top seg {seg}")
                    num_segments += 1

        if point not in used_bottom:
            if point[0] == row and point in edge_dict["bottom"]:
                point_left = [point[0], point[1] - 1]
                point_right = [point[0], point[1] + 1]
                used_bottom.append(point)
                left_seg = []
                right_seg = []
                while point_left in points and not point_left in used_bottom and point_left in edge_dict["bottom"]:
                    left_seg.append(point_left)
                    used_bottom.append(point_left)
                    point_left = [point_left[0], point_left[1] - 1]
                while point_right in points and not point_right in used_bottom and point_right in edge_dict["bottom"]:
                    right_seg.append(point_right)
                    used_bottom.append(point_right)
                    point_right = [point_right[0], point_right[1] + 1]
                seg = [point] + left_seg + right_seg
                if len(seg) > 0:
                    #print(f"bottom seg {seg}")
                    num_segments += 1

    return num_segments


def without_nth_item(n, lst):
    return lst[:n] + lst[n+1:]

def line_without_newline(line):
    return line[:-1]

def handle(line):
    if(line == ""):
        return 0
    input_row = []
    big_input_row = []
    for x in line:
        input_row.append(x)
        big_input_row += [x, x, x]
    
    input.append(input_row)
    big_input.append(big_input_row)
    big_input.append(big_input_row)
    big_input.append(big_input_row)
    return 1

lastline='a'
for line in sys.stdin:
    if(line[:-1] == '' and lastline == ''):
        print("should be ending stdin")
        break
    else:
        handle(line_without_newline(line))
        lastline = line[:-1]

max_row = len(input) - 1
max_col = len(input[0]) - 1

def in_bounds(row, col):
    return row >= 0 and col >= 0 and row <= max_row and col <= max_row

def get_adjacent(row, col):
    return [[row - 1, col],
            [row + 1, col],
            [row, col -1],
            [row, col + 1]]

def get_field(row, col):
    veg = input[row][col]
    to_check = [[row, col]]
    field = []
    while len(to_check) > 0:
        current = to_check.pop(0)
        if input[current[0]][current[1]] == veg and not current in field:
            field.append(current)
            visited.append(current)
            current_adj = get_adjacent(current[0],current[1])
            for point in current_adj:
                if point not in field and in_bounds(point[0], point[1]):
                    to_check.append(point)
    return field

num_to_direction = {0:"top", 1:"right", 2:"bottom", 3:"left"}

def get_perimeter(field):
    edges = {"top": [], "right": [], "bottom":[], "left":[]}
    perimeter = 0
    point_in_field = field[0]
    veg = input[point_in_field[0]][point_in_field[1]]
    for point in field:
        unit_perimeter = 0
        border_units = []
        top = [point[0] - 1, point[1]]
        right = [point[0], point[1] + 1]
        bottom = [point[0] + 1, point[1]]
        left = [point[0], point[1] - 1]

        if not in_bounds(top[0], top[1]) or input[top[0]][top[1]] != veg:
            edges["top"].append(point)
            perimeter += 1
        
        if not in_bounds(right[0], right[1]) or input[right[0]][right[1]] != veg:
            edges["right"].append(point)
            perimeter += 1

        if not in_bounds(bottom[0], bottom[1]) or input[bottom[0]][bottom[1]] != veg:
            edges["bottom"].append(point)
            perimeter += 1

        if not in_bounds(left[0], left[1]) or input[left[0]][left[1]] != veg:
            edges["left"].append(point)
            perimeter += 1
    
    edge_squares = [point for point in field if len(get_edge(point, edges)) > 0]
    dims = field_max_min(edge_squares)
    row_min = dims[0]
    row_max = dims[2]
    col_min = dims[1]
    col_max = dims[3]
    num_sides_for_field = 0
    i = row_min

    while i <= row_max:
        num_sides_for_field += get_horizontal_segments(edge_squares, edges, i)
        i += 1
    j = col_min
    while j <= col_max:
        num_sides_for_field += get_vert_segments(edge_squares, edges, j)
        j += 1
    return [perimeter, num_sides_for_field]

def get_edge(point, edges):
    edge = []
    if point in edges["top"]:
        edge.append("top")
    if point in edges["right"]:
        edge.append("right")
    if point in edges["bottom"]:
        edge.append("bottom")
    if point in edges["left"]:
        edge.append("left")
    return edge

#Initial attempt to do edge cases fast -> any field made by a set of colinear points is always a quadrilateral
def co_linear(field):
    vertical = True
    i = 0
    while i < len(field) - 1 and vertical:
        if field[i][0] != field[i + 1][0]:
            vertical = False
        i += 1
    horizontal = True
    i = 0
    while i < len(field) - 1 and horizontal:
        if field[i][1] != field[i + 1][1]:
            horizontal = False
        i += 1
    return vertical or horizontal
    

    return [next[0] - current[0], next[1] - current[1]]

#Originally used for perimeter calculation. 
def is_edge(row, col, veg):
    if not in_bounds(row, col):
        return False
    for adj in get_adjacent(row, col):
        if not in_bounds(adj[0], adj[1]) or big_input[adj[0]][adj[1]] != veg:
            return True
    return False


#Iteration to get fields
for i in range(len(input)):
    for j in range(len(input[0])):
        if [i,j] not in visited:
            fields.append(get_field(i, j))

answer = 0
answer_2 = 0
for field in fields:
    border_calc = get_perimeter(field)
    answer += len(field) * border_calc[0]
    answer_2 += len(field) * border_calc[1]


#Everything past this point was either for trying other methods (walking the perimeter and counting direction changes)
#or for doing the initial approach on the big-scaled map. 
print(answer)
print(answer_2)

visited = []
big_fields = []
temp_input = input
input = big_input
max_row = len(input) - 1
max_col = len(input[0]) - 1


#Biggest time loss. Organizing the islands was done iteratively with queue so that stack depth wouldn't be an issue,
# but the 3x length and width made this take at least a minute or 2.  

#print(f"generating big fields")
#for i in range(len(input)):
#    for j in range(len(input[0])):
#        if [i, j] not in visited:
#            print(f"getting big field {input[i][j]}")
#            big_fields.append(get_field(i,j))

#print("\nBig fields:")
#for field in big_fields:
#    print(f"{field}\n")
#print("\n")            

#Needed to match the area of the small field to the number of sides on the big field, so used this to match them together.
def get_big_field(row, col):
    target_point = [row * 3, col * 3]
    return next((x for x in big_fields if target_point in x), None)

#Debugging the scaled up map
def print_big():
    for row in big_input:
        str = ""
        for ch in row:
            str+= ch
        print(str)

#def get_horizontal_segments(field, row):
#    used = []
#    num_segments = 0
#    for point in field:
#        if point not in used:
#            if point[0] == row:
#                used.append(point)
#                point_left = [point[0], point[1] - 1]
#                point_right = [point[0], point[1] + 1]
#                left_seg = []
#                right_seg = []
#                while point_left in field and point_left not in used:
#                    left_seg.append(point_left)
#                    #print(f"left seg is {left_seg} after adding")
#                    used.append(point_left)
#                    point_left = [point_left[0], point_left[1] - 1]
#                while point_right in field and point_right not in used:
#                    right_seg.append(point_right)
#                    #print(f"right seg is {right_seg} after adding")
#                    used.append(point_right)
#                    point_right = [point_right[0], point_right[1] + 1]
#                seg = left_seg + [point] + right_seg
#                if len(seg) > 1:
#                    #print(f"horizontal seg {seg}")
#                    num_segments += 1
#    return num_segments

#def get_vert_segments(field, column):
#    used = []
#    num_segments = 0
#    for point in field:
#        if point not in used:
#            if point[1] == column:
#                #travel up and down to occupy all 
#                point_up = [point[0] - 1, point[1]]
#                point_down = [point[0] + 1, point[1]]
#                used.append(point)
#                up_seg = []
#                down_seg = []
#                while point_up in field and point_up not in used:
#                    up_seg.append(point_up)
#                    used.append(point_up)
#                    point_up = [point_up[0] - 1, point_up[1]]
#                while point_down in field and point_down not in used:
#                    down_seg.append(point_down)
#                    used.append(point_down)
#                    point_down = [point_down[0] + 1, point_down[1]]
#                seg =  up_seg + [point] + down_seg
#                if len(seg) > 1:
#                    #print(f"vertical seg {seg}")
#                    num_segments += 1
#    return num_segments

#visited = []
#answer = 0
#print(len(fields))
#print(len(big_fields))
#for field in fields:
#    print(f"getting big field")
#    corresponding_big = get_big_field(field[0][0], field[0][1])
#    if corresponding_big is None:
#        print(f"couldn't find matching field for {field[0]}")
#        #print_big()
#    veg = big_input[corresponding_big[0][0]][corresponding_big[0][1]]
#    print(f"get edges for {veg}")
#    edges = [point for point in corresponding_big if is_edge(point[0], point[1], veg)]
#
#    dims = field_max_min(corresponding_big)
#    row_min = dims[0]
#    row_max = dims[2]
#    col_min = dims[1]
#    col_max = dims[3]
#    num_sides_for_field = 0
#    i = row_min
#    print(f"row max {row_max}")
#    print(f"get horizontals")
#    while i <= row_max:
#        num_sides_for_field += get_horizontal_segments(edges, i)
#        i += 1
#    
#    print(f"get verticals")
#    j = col_min
#    while j <= col_max:
#        num_sides_for_field += get_vert_segments(edges, j)
#        j += 1
#    print(f"{big_input[corresponding_big[0][0]][corresponding_big[0][1]]} has {num_sides_for_field} sides")
#    answer += len(field) * num_sides_for_field
#
#print(answer)


