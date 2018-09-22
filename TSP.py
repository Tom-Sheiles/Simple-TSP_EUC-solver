import sys, math,time
import mysql.connector
import GUI as GUI


def consoleFileHandle(name):
    with open(name) as tspfile:
        line = tspfile.readlines()
    return line


def consoleTimeHandle():
    maxtime = sys.argv[2]
    return maxtime


def greedySearch(cities):
    lowestCity = cities[1]
    lowestDistance = abs(cities[1][1] - cities[2][1] + cities[1][2] - cities[2][2])
    totalDistance = 0
    tour = [0] * (len(cities) - 6)
    returnTour = [0] * (len(cities) - 7)
    tour[0] = 1
    returnTour[0] = cities[1]


    for i in range(1, len(cities)):
        if cities[i] != 0:
            for j in range(2, len(cities)):
                if j in tour:
                    continue
                if cities[j] != 0:
                    x = abs(lowestCity[1] - cities[j][1])
                    y = abs(lowestCity[2] - cities[j][2])
                    distance = math.sqrt((x ** 2) + (y ** 2))
                    totalDistance += distance
                    if distance <= lowestDistance and distance != 0:
                        lowestDistance = distance
                        NextlowestCity = cities[j]
            lowestCity = NextlowestCity
            lowestDistance = sys.maxsize
            tour[i] = lowestCity[0]
            try:
                returnTour[i] = lowestCity
            except IndexError:
                continue

    return returnTour


def totalDistance(tour):
    total = 0
    for i in range(0, len(tour)):
        try:
            x = abs(tour[i][1] - tour[i+1][1]) ** 2
            y = abs(tour[i][2] - tour[i+1][2]) ** 2
            dist = math.sqrt(x+y)
            total += dist
        except IndexError:
            x = abs(tour[i][1] - tour[1][1]) ** 2
            y = abs(tour[i][2] - tour[1][2]) ** 2
            dist = math.sqrt(x + y)
            total += dist

    return total


def swapTour(tour, i, j):
    newTour = tour[0:i]
    newTour.extend(reversed(tour[i:j + 1]))
    newTour.extend(tour[j+1:])
    return newTour


def greedyTwoOptSolver(tour):
    currentTotal = totalDistance(tour)
    bestTour = tour

    for i in range(0, len(tour)):
        for j in range(i+1, len(tour) - 1):
            newTour = swapTour(bestTour, i, j)
            newDistance = totalDistance(newTour)
            if newDistance < currentTotal:
                bestTour = newTour
                currentTotal = newDistance
                return bestTour

    return bestTour


def printTourToConsole(tour):
    print(name, "\n", "Shortest found tour length: ", totalDistance(tour), "\n", "Tour:")
    for x in range(0, len(tour)):
            print(int(tour[x][0]))


user='s5132012'
password='XwxXSo4j'
database='s5132012db'
host='mysql.ict.griffith.edu.au'


name = sys.argv[1]
tspLines = consoleFileHandle(name)
maxTime = consoleTimeHandle()
startTime = time.time()
cities = [0] * len(tspLines)
tour = list()
step = 0

j = 1
for i in range(6, len(tspLines) - 1):
    try:
        cities[j] = [int(s) for s in tspLines[i].split()]
    except ValueError:
        cities[j] = [float(s) for s in tspLines[i].split()]
    j += 1

tour = greedySearch(cities)

while time.time() < (startTime + int(maxTime)):
    step += 1
    tour = greedyTwoOptSolver(tour)


printTourToConsole(tour)
