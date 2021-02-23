import numpy as np
import queue

col = 3
row = 3
count = 0
minH = 20
posMin = 0
temp = []
posMinList = []
minList = []
heuristicList = []


root = np.array([
    [-1, 8, 3],
    [2, 6, 4],
    [1, 7, 5]
])
target = np.array([
    [1, 2, 3],
    [8, -1, 4],
    [7, 6, 5]
])
neighbours = np.array([])
x = 0
y = 0


def heuristic(maze, target, count):
    for i in range(col):
        for j in range(row):
            if(maze[i][j] != target[i][j]):
                count += 1
            if(maze[i][j] == -1 & target[i][j] == -1):
                count += 1
    count = count - 1
    return count


temp = np.empty_like(root)
temp[:] = root
maze = np.empty_like(root)
maze[:] = temp
parent = np.empty_like(root)
parent[:] = maze

q = queue.PriorityQueue()
newHeuristc = heuristic(temp, target, count)
move = np.array([])


def neighbour(x, y, col):
    allNeighbours = np.array([[x-1, y], [x+1, y], [x, y-1], [x, y+1]])
    notNeighbour = np.where((allNeighbours == -1) | (allNeighbours == col))

    if len(notNeighbour[0]) == 2:
        allNeighbours = np.delete(allNeighbours, notNeighbour[0][0], 0)
        allNeighbours = np.delete(allNeighbours, notNeighbour[0][1]-1, 0)
    elif len(notNeighbour[0]) == 1:
        allNeighbours = np.delete(allNeighbours, notNeighbour[0][0], 0)

    return allNeighbours


def expand(temp, cost):
    global neighbours, x, y, maze, newHeuristc, minH, posMin, move
    empty = np.where(temp == -1)
    x = int(empty[1])
    y = int(empty[0])
    neighbours = neighbour(x, y, col)

    if move.size > 0:
        sizeN = len(neighbours)
        for i in range(len(neighbours)):
            if len(neighbours) == sizeN:
                if((move[0] == neighbours[i]).all()):
                    neighbours = np.delete(neighbours, i, 0)
    for i in range(len(neighbours)):
        maze[:] = temp
        mazeX = neighbours[i][1]
        mazeY = neighbours[i][0]
        maze[mazeX][mazeY] = temp[y][x]
        maze[y][x] = temp[mazeX][mazeY]
        newHeuristc = heuristic(maze, target, count) + cost
        heuristicList.append(newHeuristc)

    maze[:] = temp
    minH = np.min(heuristicList)
    posMin = np.where(heuristicList == minH)


def main():
    global move, minH, posMin, heuristicList, neighbours, x, y
    cost = 0
    firstHeuristic = heuristic(maze, target, count)
    if(firstHeuristic == 0):
        exit(0)
    while minH-cost != 0:
        cost += 1
        if(cost == 1):
            move = np.array([[x-1, y-1]])
        else:
            move = np.array([[x, y]])
        expand(temp, cost)
        print(maze, '\n')

        while (posMin[0].size > 1):
            oldNeighbors = neighbours
            parent[:] = temp
            maze[:] = temp
            tempPosMin = posMin
            for i in range(tempPosMin[0].size):
                heuristicList = []
                empty = np.where(temp == -1)
                j = int(empty[1])
                k = int(empty[0])
                mazeX = oldNeighbors[int(tempPosMin[0][i])][1]
                mazeY = oldNeighbors[int(tempPosMin[0][i])][0]
                temp[mazeX][mazeY] = maze[k][j]
                temp[k][j] = maze[mazeX][mazeY]
                if(i == 0):
                    move = np.array([[j, k]])
                expand(temp, cost)
                minH = np.min(heuristicList)
                posMin = np.where(heuristicList == minH)
                for i in range(posMin[0].size):
                    if (posMin[0].size > 1):
                        minList.append(int(heuristicList[int(posMin[0][i])]))
                    else:
                        minList.append(int(heuristicList[int(posMin[i])]))
                posMinList.append(posMin[0][0])
                heuristicList = []
                temp[:] = parent
                maze[:] = parent

            minH = np.min(minList)
            posMin = np.where(minList == minH)
            posNeigh = tempPosMin[0][int(posMin[0][0])]
            mazeX = oldNeighbors[posNeigh][1]
            mazeY = oldNeighbors[posNeigh][0]
            temp[mazeX][mazeY] = maze[k][j]
            temp[k][j] = maze[mazeX][mazeY]

        else:
            heuristicList = []
            mazeX = neighbours[int(posMin[0])][1]
            mazeY = neighbours[int(posMin[0])][0]
            temp[mazeX][mazeY] = maze[y][x]
            temp[y][x] = maze[mazeX][mazeY]

    maze[:] = temp
    print(maze, '\n')
    print('The cost is: ', cost)


main()
