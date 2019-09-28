import numpy as np
import math
import time
from random import *


class AntColonySystem:
    numAnts = 10
    numIterations = 100
    a = 0.1  # alpha
    b = 2  # beta
    q0 = 0.9

    def __init__(self, size, cityLocations):
        self.size = size
        self.cityLocations = cityLocations
        self.costs = self.createCostMatrix(cityLocations)
        self.bestTour = None
        self.bestTourLength = math.inf
        self.tau = 1 / (self.lengthNearestNeighbour() * self.size)
        self.pheromone = self.tau * np.ones((self.size, self.size))

    def findSolution(self):
        T1 = time.perf_counter()
        location = np.zeros(self.numAnts, np.int32)
        startingpoint = np.zeros(self.numAnts, np.int32)

        for ant in range(self.numAnts):
            startingpoint[ant] = location[ant] = randint(0, self.size - 1)

        for i in range(self.numIterations):
            visited = np.zeros((self.numAnts, self.size), dtype=bool)
            tours = [np.zeros((self.size, self.size), np.int8) for ant in range(self.numAnts)]
            distances = np.zeros(self.numAnts)
            for ant in range(self.numAnts):
                visited[ant][location[ant]] = True

            for step in range(self.size):
                for ant in range(self.numAnts):
                    current = location[ant]
                    if step != self.size - 1:
                        next = self.nextCity(ant, location[ant], visited[ant])
                    else:
                        next = startingpoint[ant]
                    location[ant] = next
                    visited[ant][next] = True
                    tours[ant][current][next] = tours[ant][next][current] = 1
                    distances[ant] += self.costs[current][next]
                    self.localTrailUpdate(current, next)
            shortestLength = min(distances)
            if shortestLength < self.bestTourLength:
                self.bestTourLength = shortestLength
                self.bestTour = tours[np.argmin(distances)]
            self.globalTrailUpdate()
        T2 = time.perf_counter()
        print('Melhor percurso encontrado: ', self.bestTourList())
        print('Tem um tamanho de: ', self.bestTourLength )
        print('Encontrado em ', T2 - T1, ' segundos')

    def createCostMatrix(self, cityLocations):
        result = np.zeros((self.size, self.size))
        for i in range(self.size):
            for j in range(self.size):
                result[i][j] = self.distance(i, j)
        return result

    def distance(self, i, j):
        return math.sqrt(
            math.pow(self.cityLocations[j][0]-self.cityLocations[i][0], 2) +
            math.pow(self.cityLocations[j][1]-self.cityLocations[i][1], 2))

    def closestNotVisited(self, loc, visited):
        minimum = math.inf
        result = None
        for city in range(self.size):
            if (not visited[city]) and (self.costs[loc][city] < minimum):
                minimum = self.costs[loc][city]
                result = city
        return result

    def localTrailUpdate(self, i, j):
        self.pheromone[j][i] = self.pheromone[i][j] = (1-self.a) * self.pheromone[i][j] + self.a * self.tau

    def globalTrailUpdate(self):
        for i in range(self.size):
            for j in range(i + 1, self.size):
                self.pheromone[i][j] = self.pheromone[j][i] = (1-self.a)*self.pheromone[i][j] + self.a * self.bestTour[i][j] / self.bestTourLength

    def nextCity(self, ant, loc, visited):
        result = None
        q = np.random.random_sample()
        if q <= self.q0:
            max = -math.inf
            for city in range(self.size):
                if not visited[city]:
                    f = self.attraction(loc, city)
                    if f > max:
                        max = f
                        result = city
            if max != 0:
                return result
            else:
                return self.closestNotVisited(loc, visited)
        else:
            sum = 0
            for city in range(self.size):
                if not visited[city]:
                    sum += self.attraction(loc, city)
            if sum == 0:
                return self.closestNotVisited(loc, visited)
            else:
                R = np.random.random_sample()
                s = 0
                for city in range(self.size):
                    if not visited[city]:
                        s += self.attraction(loc, city) / sum
                        if s > R:
                            return city

    def attraction(self, i, j):
        if i != j:
            return self.pheromone[i][j] / (math.pow(self.costs[i][j], self.b))
        else:
            return 0

    def lengthNearestNeighbour(self):
        start = randint(0, self.size-1)
        current = start
        visited = np.zeros(self.size, dtype=bool)
        tour = [current]
        length = 0
        for i in range(self.size-1):
            visited[current] = True
            minimum = math.inf
            closest = None
            for i in range(self.size):
                if (not visited[i]) and (self.costs[current][i] < minimum):
                    minimum = self.costs[current][i]
                    closest = i
            tour.append(closest)
            length += minimum
            current = closest
        tour.append(start)
        length += self.costs[current][start]
        return length

    def bestTourList(self):
        current = 0
        previous = 0
        tour = [0]
        for i in range(self.size):
            next = 0
            while (self.bestTour[current][next] == 0) or (previous == next):
                next += 1
            tour.append(next)
            previous = current
            current = next
        return tour





