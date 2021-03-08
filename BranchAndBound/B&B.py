import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy

G = nx.Graph()

G.add_edge("A", "B")
G.add_edge("A", "C")
G.add_edge("A", "D")
G.add_edge("A", "E")
G.add_edge("B", "C")
G.add_edge("B", "D")
G.add_edge("B", "E")
G.add_edge("C", "D")
G.add_edge("C", "E")
G.add_edge("D", "E")
G.add_edge("E", "D")

pos = {'A': (1, 5), 'B': (3, 5), 'C': (0, 2), 'D': (4, 2), 'E': (2, 0)}

infinite = np.inf
COL = 5
ROW = 5
adjList = np.array([[infinite, 20, 30, 10, 11],
                    [15, infinite, 16, 4, 2],
                    [3, 5, infinite, 2, 4],
                    [19, 6, 18, infinite, 3],
                    [16, 4, 7, 16, infinite]])


class Node:
    def __init__(self, current, previous, cost, move):
        self.current = current
        self.previous = previous
        self.cost = cost
        self.move = move


def redu(matrix):
    rowMin = np.amin(matrix.current, axis=1)

    for i in range(COL):
        matrix.current[i, :] = np.subtract(
            matrix.current[i][:], rowMin[i])

    colMin = np.amin(matrix.current, axis=0)

    for i in range(COL):
        matrix.current[:, i] = np.subtract(
            matrix.current[:, i], colMin[i])
    bG = np.sum(rowMin + colMin)
    return rowMin, colMin, bG


def BnB(adjList):
    cont = 0
    for i in range(COL):
        if((adjList[:, i] == 0).any() or (adjList[:, i] == infinite).any() and (adjList[i, :] == 0).any() or (adjList[i, :] == infinite).any()):
            cont += 1
    if(cont == COL):
        print("Matrix reduced")
        return True
    else:
        return False


def bestN(matrix):
    bestFn = 0
    firstIt = True
    for node in matrix.values():
        # If there bestFn is greater than f(n) of the current node or is just the first iteration
        if firstIt or node.cost < bestFn:
            firstIt = False
            best = node
            bestFn = best.cost
    return best


def main(start):

    matrix = {str(start): Node(start, start, 0, '')}
    bestNodeV = {}
    c = 0
    j = 0
    bestList = []
    while True:

        bestNode = bestN(matrix)
        bestNodeV[str(bestNode.current)] = bestNode

        minMax = redu(bestNode)

        b = np.sum(minMax[0] + minMax[1])

        for i in range(COL-1):
            adjList = deepcopy(bestNode.current)
            adjList[c, :] = infinite
            adjList[:, i+1] = infinite
            adjList[j+1][c] = infinite
            reduced = BnB(adjList)
            if(reduced == True):
                cost = bestNode.current[c][j+1] + b + minMax[2]
                bestList.append(Node(adjList, bestNode.previous, cost, 'yes'))
                j += 1
            else:
                redu(adjList)
                cost = bestNode[c][j+1] + b + minMax[2]


main(adjList)
# nodes
nx.draw_networkx_nodes(G, pos, node_size=700)

# edges
nx.draw_networkx_edges(G, pos, width=2)


# labels
nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

plt.axis("off")
plt.show()
