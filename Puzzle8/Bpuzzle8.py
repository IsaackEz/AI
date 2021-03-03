import numpy as np
from copy import deepcopy

COL = 5
ROW = 5

START = [[0, 0, 0, 0, 0],
         [0, 1, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0]]

END = [[0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0],
       [0, 0, 0, 1, 0]]

best = {}

void = 1
for i in range(len(END)):
    if void in END[i]:
        posGoal = (i, END[i].index(void))


class Node:
    def __init__(self, current, previous, cost, heuristic, move):
        self.current = current
        self.previous = previous
        self.cost = cost
        self.heuristic = heuristic
        self.move = move

    def f(self):  # f(n)
        return self.cost + self.heuristic


def printPath(bestVisited):  # Print the final path
    node = bestVisited[str(END)]
    path = []

    while node.move:  # While that position moved
        path.append(node.current)
        node = bestVisited[str(node.previous)]
    path.append(node.current)
    path.reverse()
    for i in range(len(path)):
        print(path[i][0])
        print(path[i][1])
        print(path[i][2])
        print(path[i][3])
        print(path[i][4], '\n')


def heuristicF(current):
    count = 0
    posEmpty = pos(current)
    x = posEmpty[0]  # Saving it as coordinates(x,y)
    y = posEmpty[1]
    xE = posGoal[0]
    yE = posGoal[1]
    count = abs(x-yE) + abs(xE-y)
    return count


def pos(current):  # Look for the position of the current node
    void = 1
    for i in range(len(current)):
        if void in current[i]:
            return (i, current[i].index(void))


def expand(bestPuzzle):  # Take the best puzzle yet
    neighboursList = []  # List where we append all the neighbours that we find
    # Get the position of the empty slot (0)
    posEmpty = pos(bestPuzzle.current)
    x = posEmpty[0]  # Saving it as coordinates(x,y)
    y = posEmpty[1]

    # Look all the neighbours that the empty has
    allNeighbours = np.array([[x-1, y], [x+1, y], [x, y-1], [x, y+1]])
    # If there is overflow take their position
    notNeighbour = np.where((allNeighbours == -1) | (allNeighbours == COL))
    if len(notNeighbour[0]) == 2:  # If there is 2 neigbours overflowed
        # Delete the one on position 0 0
        allNeighbours = np.delete(allNeighbours, notNeighbour[0][0], 0)
        # Bc we delete one, we said -1 to adjust the position
        allNeighbours = np.delete(allNeighbours, notNeighbour[0][1]-1, 0)
    elif len(notNeighbour[0]) == 1:  # If there is 1 neigbour overflowed
        allNeighbours = np.delete(
            allNeighbours, notNeighbour[0][0], 0)  # Delete it

    for i in range(len(allNeighbours)):  # Loop through all the neighbours
        currentX = allNeighbours[i][0]  # Save the first neighbour
        currentY = allNeighbours[i][1]
        newNeighbour = deepcopy(bestPuzzle.current)  # Copy the current best
        # Pass the number that the best has to the neighbour (we move)
        newNeighbour[x][y] = bestPuzzle.current[currentX][currentY]
        newNeighbour[currentX][currentY] = 1  # Finish the move
        neighboursList.append(Node(
            newNeighbour, bestPuzzle.current, bestPuzzle.cost + 1, heuristicF(newNeighbour), 'yes'))  # Append that node to the list, marked as 'yes' because we move
    return neighboursList


def bestNode(puzzle):  # Get the bestNode yet
    bestFn = 0
    firstIt = True
    for node in puzzle.values():
        if firstIt or node.f() < bestFn:  # If there bestFn is greater than f(n) of the current node or is just the first iteration
            firstIt = False
            best = node
            bestFn = best.f()
    return best


def main(start):  # Main function
    # Set the puzzle to the starting node
    puzzle = {str(start): Node(start, start, 0, heuristicF(start), '')}
    bestVisited = {}  # Dictionary of the best nodes visited
    while True:

        bestPuzzle = bestNode(puzzle)  # Getting the bestPuzzle yet
        # Saving it to bestVisited
        bestVisited[str(bestPuzzle.current)] = bestPuzzle

        if (bestPuzzle.current == END):  # If we got a solution
            print('Cost: ', bestPuzzle.cost, '\n')  # Print the cost
            return printPath(bestVisited)  # Print the path

        neighbours = expand(bestPuzzle)  # Call the expand function
        for neighbour in neighbours:  # Loop through the neighbours
            # If that neighbour is already on the list continue
            if (str(neighbour.current) in bestVisited.keys() or str(neighbour.current) in puzzle.keys() and puzzle[str(neighbour.current)].f() < neighbour.f()):
                continue
            # Add to puzzle the iterated neighbour
            puzzle[str(neighbour.current)] = neighbour
        del puzzle[str(bestPuzzle.current)]  # Delete the current best


main(START)
