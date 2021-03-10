import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy


class Node:  # Class containing the cost and the matrix of the current node
    def __init__(self, current, cost):
        self.current = current
        self.cost = cost


def redu(matrix):
    rowMin = np.amin(matrix, axis=1)  # Get the min of the rows
    # If the entire row is infinite, set to zero
    rowMin[rowMin == infinite] = 0

    for i in range(COL):
        matrix[i, :] = np.subtract(  # Substract the min with the matrix
            matrix[i][:], rowMin[i])

    colMin = np.amin(matrix, axis=0)  # Get the max of the columns
    # If the entire column is infinite, set to zero
    colMin[colMin == infinite] = 0

    for i in range(COL):
        matrix[:, i] = np.subtract(  # Substract the min with the matrix
            matrix[:, i], colMin[i])

    return rowMin, colMin


def BnB(adjList):
    cont = 0
    for i in range(COL):  # Checks if the matrix is reduced
        if(((adjList[:, i] == 0).any() or (adjList[:, i] == infinite).all()) and ((adjList[i, :] == 0).any() or (adjList[i, :] == infinite).all())):
            cont += 1
    if(cont == COL):  # if all columns and rows have a 0 True, else False
        return True
    else:
        return False


def bestN(matrix):
    bestFn = 0
    firstIt = True
    for node in matrix.values():
        if firstIt or node.cost < bestFn:  # Get the best node of the list we got
            firstIt = False
            best = node
            bestFn = best.cost
    return best


def getPath(visited):
    path = []
    label = []
    for i in range(COL):
        path.append(visited[i])  # Get the path from the visited list
    path.reverse()  # Reverse the path

    for i in range(len(path)):  # Set the corresponding letter to each position
        if path[i] == 0:
            label.append('A')
        elif path[i] == 1:
            label.append('B')
        elif path[i] == 2:
            label.append('C')
        elif path[i] == 3:
            label.append('D')
        elif path[i] == 4:
            label.append('E')
    return label


def main(start):

    matrix = {str(start): Node(start, 0)}  # First matrix
    first = True  # First iteration
    bestList = []
    visited = np.array([0, 0, 0, 0])
    nodesL = [0, 1, 2, 3, 4]
    while True:
        bestNode = bestN(matrix)  # Asign to bestNode the lowest cost
        minMax = redu(bestNode.current)  # Reduce the best
        if(first):  # If is the first iteration
            b = np.sum(minMax[0] + minMax[1])  # b is the sum of max and min
            index = 0
        else:
            b = bestNode.cost  # b will be the cost of the new best
            for i in range(len(bestList)):
                # if the cost is the same ass the one on the list
                if (bestList[i].cost == bestNode.cost):
                    index = i  # Get the index

        # Set the position as visited in the first position
        visited = np.insert(visited, 0, nodesL[index])
        # remove the visited from the list
        nodesL = (list(set(nodesL) - set(visited)))
        if(not nodesL):  # If is empty
            path = getPath(visited)  # Get the path
            return path
        bestList = []
        for j in range(len(nodesL)):
            # Copy the current best to adjList
            adjList = deepcopy(bestNode.current)
            # Set the entire row of the node visited to infinite
            adjList[visited[0], :] = infinite
            # Set the entire column of the 'neighbor' to infinite
            adjList[:, nodesL[j]] = infinite
            # Set the cell of the visited node and the neighbor to infinite
            adjList[nodesL[j]][visited[0]] = infinite
            # Set the previous cell to infinite
            adjList[nodesL[j]][visited[1]] = infinite
            reduced = BnB(adjList)  # Reduce the matrix

            if(reduced == True):  # If it is reduced
                # Set the cost without bG
                cost = bestNode.current[visited[0]][nodesL[j]] + b
                bestList.append(
                    Node(adjList, cost, ))  # Append the node with its cost

            else:
                minMax = redu(adjList)  # Else reduce it again
                # Set bG to the cost from that reuctions
                bG = np.sum(minMax[0] + minMax[1])
                # Set the cost with bG
                cost = bestNode.current[visited[0]][nodesL[j]] + b + bG
                bestList.append(
                    Node(adjList, cost))  # Append the node with its cost
        matrix = {}
        for bestL in bestList:
            matrix[str(bestL.current)] = bestL  # Add the ndoes to matrix
        first = False  # Set first iteration to false


if __name__ == '__main__':

    # Initialize graph with networkx
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

    path = main(refAdjList)
    print('Shortest path from A: ', path)

    esmall = []
    for i in range(len(path)-1):
        # esmall will be the dotted line of the path
        esmall.append((path[i], path[i+1]))

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)

    # edges
    nx.draw_networkx_edges(G, pos, alpha=0.5, width=6)
    nx.draw_networkx_edges(
        G, pos, edgelist=esmall, width=10, alpha=1, edge_color="r", style="dotted"
    )

    # labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

    plt.axis("off")
    plt.show()
