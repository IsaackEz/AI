import numpy as np
import random


class Node:  # Class containing the cost and the matrix of the current node
    def __init__(self, genes, fitness, percent):
        self.genes = genes
        self.fitness = fitness
        self.percent = percent


def printGen(population):
    for i in range(len(population)):
        print(population[i].genes, 'Fitness',
              population[i].fitness)  # Print the population


def genPopulation():
    populationList = []
    for i in range(totalPop):
        # Generate a random chromosome
        chromosome = np.random.randint(2, size=(genes))
        populationList.append(Node(
            chromosome, calcFitness(chromosome), 0))  # Add it to the population
    return populationList


def best(population):
    res = False
    for i in range(len(population)):  # Check if there is one chromosome with fitness 8
        if((population[i].genes == 1).all()):
            res = True
    return res


def calcFitness(population):
    # Get the fitness of each chromosome
    fitness = np.count_nonzero(population == 1)
    return fitness


def calcPercentage(population):
    totalFit = 0
    probability = []
    for i in range(len(population)):
        totalFit += population[i].fitness  # Total fitness of the population
    for i in range(len(population)):
        # Probability of each chromosome
        probability.append(population[i].fitness/totalFit)
    population[0].percent = probability[0]  # first probability = to same
    for i in range(len(population)-1):
        population[i+1].percent = probability[i+1] + \
            population[i].percent  # Cumulative probability
    return totalFit


def nextGen(population):
    newPopulation = []
    for i in range(int(totalPop/2)):
        bestParent = []
        i = 0
        for i in range(2):
            x = random.uniform(0, 1)  # Random number between 0 and 1
            # If the cumulative probability is greater or equal to x
            for i in range(len(population)):
                if(x <= population[i].percent):
                    bestParent.append(population[i])  # Select that chromosome
                    break
        # Select half of the genes (father)
        geneFather = bestParent[0].genes[0:4]
        # Select half of the genes (mother)
        geneMother = bestParent[1].genes[4:]
        newGene = np.append(geneFather, geneMother)  # Crossover
        newGene = mutation(newGene)  # Mutate
        # Add it to the new population
        newPopulation.append(Node(newGene, calcFitness(newGene), 0))
        # Select half of the genes (father)
        geneFather = bestParent[1].genes[4:]
        # Select half of the genes (mother)
        geneMother = bestParent[0].genes[0:4]
        newGene = np.append(geneFather, geneMother)  # Crossover
        newGene = mutation(newGene)  # Mutate
        # Addit to the new population
        newPopulation.append(Node(newGene, calcFitness(newGene), 0))
    return newPopulation


def mutation(newGene):
    x = random.uniform(0, 1)  # Random number between 0 and 1
    if (x < mutationRate):  # If mutationRate is greater than x
        newGene[np.random.randint(
            genes)] = 1  # Mutate
    return newGene


def main():
    res = False
    gen = 0
    population = genPopulation()  # Generate the first population
    print('Generation ', gen)  # Print the nmber of the generation
    printGen(population)  # Print the population
    while res == False:
        # Calculate the probability percent of beign chosen and cumulative probability
        calcPercentage(population)
        newPop = nextGen(population)  # Get the new population
        population = newPop
        gen += 1  # Increment the generation counter
        print('Generation ', gen)  # Print the nmber of the generation
        printGen(population)  # Print the population
        res = best(population)  # Check if the generation has fitness 8


if __name__ == '__main__':
    totalPop = 4
    genes = 8
    mutationRate = 0.3
    main()
