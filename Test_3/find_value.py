


def value_count(data,value):
    count=0
    for row in data:
        for item in row:
            if item==value:
                count+=1

    return count

def value_positions(data,value):
    positions=[]
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x]==value:
                positions.append((y,x))


    return positions




