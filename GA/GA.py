import numpy as np
from copy import deepcopy
import random


class Node:  # Class containing the cost and the matrix of the current node
    def __init__(self, genes, fitness, percent):
        self.genes = genes
        self.fitness = fitness
        self.percent = percent


totalPop = 4
genes = 8
mutationRate = 0.3


def printGen(population):
    for i in range(len(population)):
        print(population[i].genes, 'Fitness', population[i].fitness)


def genPopulation():
    populationList = []
    for i in range(totalPop):
        chromosome = np.random.randint(2, size=(genes))
        populationList.append(Node(
            chromosome, calcFitness(chromosome), 0))
    return populationList


def best(population):
    res = False
    for i in range(len(population)):
        if((population[i].genes == 1).all()):
            res = True
    return res


def calcFitness(population):
    fitness = np.count_nonzero(population == 1)
    return fitness


def calcPercentage(population):
    totalFit = 0
    probability = []
    for i in range(len(population)):
        totalFit += population[i].fitness
    for i in range(len(population)):
        probability.append(population[i].fitness/totalFit)
    population[0].percent = probability[0]
    for i in range(len(population)-1):
        population[i+1].percent = probability[i+1] + population[i].percent
    return totalFit


def nextGen(population):
    newPopulation = []
    for i in range(int(totalPop/2)):
        bestParent = []
        i = 0
        for i in range(2):
            x = random.uniform(0, 1)
            for i in range(len(population)):
                if(x <= population[i].percent):
                    bestParent.append(population[i])
                    break

        geneFather = bestParent[0].genes[0:4]
        geneMother = bestParent[1].genes[4:]
        newGene = np.append(geneFather, geneMother)
        newGene = mutation(newGene)
        newPopulation.append(Node(newGene, calcFitness(newGene), 0))
        geneFather = bestParent[1].genes[4:]
        geneMother = bestParent[0].genes[0:4]
        newGene = np.append(geneFather, geneMother)
        newGene = mutation(newGene)
        newPopulation.append(Node(newGene, calcFitness(newGene), 0))
    return newPopulation


def mutation(newGene):
    x = random.uniform(0, 1)
    if (x < mutationRate):
        newGene[np.random.randint(
            genes)] = 1
    return newGene


def main():
    res = False
    gen = 0
    population = genPopulation()
    print(gen, ' Generation')
    printGen(population)
    while res == False:
        total = calcPercentage(population)
        newPop = nextGen(population)
        population = newPop
        gen += 1
        print(gen, ' Generation')
        printGen(population)
        res = best(population)


if __name__ == '__main__':
    main()
