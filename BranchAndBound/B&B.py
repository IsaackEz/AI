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
refAdjList = np.array([[infinite, 20, 30, 10, 11],
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
    rowMin = np.amin(matrix, axis=1)
    rowMin[rowMin == infinite] = 0

    for i in range(COL):
        matrix[i, :] = np.subtract(
            matrix[i][:], rowMin[i])

    colMin = np.amin(matrix, axis=0)
    colMin[colMin == infinite] = 0

    for i in range(COL):
        matrix[:, i] = np.subtract(
            matrix[:, i], colMin[i])

    return rowMin, colMin


def BnB(adjList, visited):
    cont = 0
    for i in range(COL):
        if(((adjList[:, i] == 0).any() or (adjList[:, i] == infinite).all()) and ((adjList[i, :] == 0).any() or (adjList[i, :] == infinite).all())):
            cont += 1
    if(cont == COL):
        print("Matrix reduced")
        return True
    else:
        return False


def bestN(matrix):
    bestFn = 0
    ind = 0
    firstIt = True
    for node in matrix.values():
        # If there bestFn is greater than f(n) of the current node or is just the first iteration
        if firstIt or node.cost < bestFn:
            ind += 1
            firstIt = False
            best = node
            bestFn = best.cost
    return best, ind


def main(start):

    matrix = {str(start): Node(start, start, 0, 0)}
    c = 0
    bestList = []
    bestNodeV = {}
    visited = np.array([0, 0, 0, 0])
    nodesL = [0, 1, 2, 3, 4]
    while True:

        bestNode = bestN(matrix)
        minMax = redu(bestNode[0].current)
        if(c == 0):
            b = np.sum(minMax[0] + minMax[1])
            index = 0
        else:
            b = bestNode[0].cost
            for i in range(len(bestList)):
                if (bestList[i].cost == bestNode[0].cost):
                    index = i

        visited = np.insert(visited, 0, nodesL[index])
        bestNodeV[str(bestNode[0].current)] = bestNode[0]
        nodesL = (list(set(nodesL) - set(visited)))
        if(not nodesL):
            print("Finished")
            exit(0)
        bestList = []
        for j in range(len(nodesL)):
            adjList = deepcopy(bestNode[0].current)
            adjList[visited[0], :] = infinite
            adjList[:, nodesL[j]] = infinite
            adjList[nodesL[j]][visited[0]] = infinite
            adjList[nodesL[j]][visited[1]] = infinite
            reduced = BnB(adjList, visited)

            if(reduced == True):
                cost = bestNode[0].current[visited[0]][nodesL[j]] + b
                bestList.append(
                    Node(adjList, bestNode[0].previous, cost, visited[0]))

            else:
                minMax = redu(adjList)
                bG = np.sum(minMax[0] + minMax[1])
                cost = bestNode[0].current[visited[0]][nodesL[j]] + b + bG
                bestList.append(
                    Node(adjList, bestNode[0].previous, cost, visited[0]))
        matrix = {}
        for bestL in bestList:
            matrix[str(bestL.current)] = bestL
        c += 1


main(refAdjList)
# nodes
nx.draw_networkx_nodes(G, pos, node_size=700)

# edges
nx.draw_networkx_edges(G, pos, width=2)


# labels
nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

plt.axis("off")
plt.show()
