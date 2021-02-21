import numpy as np
import queue

col = 3
row = 3
count = 0


def neighbour(x, y, col):
    allNeighbours = np.array([[x-1, y], [x+1, y], [x, y-1], [x, y+1]])
    notNeighbour = np.where((allNeighbours == -1) | (allNeighbours == col))

    if len(notNeighbour[0]) == 2:
        allNeighbours = np.delete(allNeighbours, notNeighbour[0][0], 0)
        allNeighbours = np.delete(allNeighbours, notNeighbour[0][1]-1, 0)
    elif len(notNeighbour[0]) == 1:
        allNeighbours = np.delete(allNeighbours, notNeighbour[0][0], 0)

    return allNeighbours


def heuristic(maze, target, count):
    for i in range(col):
        for j in range(row):
            if(maze[i][j] != target[i][j]):
                count += 1
    count = count - 1
    return count


def main():
    heuristicList = list()
    mazeList = list()
    visited = list()

    root = np.array([
        [2, 8, 3],
        [1, 6, 4],
        [7, -1, 5]
    ])
    target = np.array([
        [1, 2, 3],
        [8, -1, 4],
        [7, 6, 5]
    ])
    maze = np.empty_like(root)

    q = queue.PriorityQueue()
    firstHeuristic = np.inf
    empty = np.where(root == -1)
    x = int(empty[1])
    y = int(empty[0])
    neighbours = neighbour(x, y, col)
    maze[:] = root
    for i in range(len(neighbours)):
        cost = 1
        mazeX = neighbours[0][1]
        mazeY = neighbours[0][0]

        visit = np.where(visited == maze[y][x])
        if len(visit[0]) == 0:
            maze[mazeX][mazeY] = root[y][x]
            maze[y][x] = root[mazeX][mazeY]
            visited.append(maze[y][x])

            print(maze[y][x], '\n')
            print(maze, '\n')
            neighbours = neighbour(mazeY, mazeX, col)
            newHeuristc = heuristic(maze, target, count)
            newHeuristc = newHeuristc + cost
            heuristicList.append(newHeuristc)
            mazeList.append(maze)
        else:
            if visited[int(visit[0])] != maze[y][x]:
                maze[mazeX][mazeY] = root[y][x]
                maze[y][x] = root[mazeX][mazeY]
                visited.append(maze[y][x])

                print(maze[y][x], '\n')
                print(maze, '\n')
                neighbours = neighbour(mazeY, mazeX, col)
                newHeuristc = heuristic(maze, target, count)
                newHeuristc = newHeuristc + cost
                heuristicList.append(newHeuristc)
                mazeList.append(maze)
        # print(mazeList)
    # print(heuristicList)
    min = np.min(heuristicList)
    posMin = np.where(heuristicList == min)
    # print(posMin[0])


main()
