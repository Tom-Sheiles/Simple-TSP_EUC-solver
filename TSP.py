import sys, math,time
import GUI as GUI

# open file in root directory with the same name and handle as provided in 'name'
# returns list of all lines in the file split at the newline character
def consoleFileHandle(name):
    with open(name) as tspfile:
        line = tspfile.readlines()
    return line


# returns the maximum time the program should run for before terminating, receives input from the console
def consoleTimeHandle():
    maxtime = sys.argv[2]
    return maxtime

# function for initial greedy search solution.
# greedy searches begin at a starting position and move to the next closest node.
#  Often leads to less than optimal solutions
# returns a 2d list with the found solution
def greedySearch(cities):
    lowestCity = cities[1]
    lowestDistance = abs(cities[1][1] - cities[2][1] + cities[1][2] - cities[2][2])
    totalDistance = 0
    tour = [0] * (len(cities) - 6)
    returnTour = [0] * (len(cities) - 7)
    tour[0] = 1
    returnTour[0] = cities[1]

# algorithm for simple greedy search solution
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


# Standard Euclidean distance formula that calculates the distance between two points.
# the total of all distances is added and returned as a floating point number. the last node is connected back to the
# first in order to create a complete tour.
# tour refers to a 2d list of points.
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


# function swaps the position of nodes and returns as a new list leaving the original unaltered.
def swapTour(tour, i, j):
    newTour = tour[0:i]
    newTour.extend(reversed(tour[i:j + 1]))
    newTour.extend(tour[j+1:])
    return newTour


# takes a greedy solution as input and improves upon it by swapping two nodes and returning if an improvement to the
# route is found.
# after a more efficient route is found, it is returned and the function called again
# returns a 2d containing the improved solution
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


# outputs to standard out the name of input file, the most optimal route found within the time and the order of the
#  nodes
def printTourToConsole(tour):
    print(name, "\n", "Shortest found tour length: ", totalDistance(tour), "\n", "Tour:")
    for x in range(0, len(tour)):
            print(int(tour[x][0]))


name = sys.argv[1]
# the input method for the file and the max size are determined by the function,
#  for different assignment methods, call different functions
tspLines = consoleFileHandle(name)
maxTime = consoleTimeHandle()
startTime = time.time()
cities = [0] * len(tspLines)
tour = list()
step = 0

# for every city in the input with the correct formatting, convert to a list of integers
# cities[x][y] where x is index in the list and y is the city number[0] x coord[1] and y coord[2]
# assigning the cities begins at 1 to map the index and the city number evenly
j = 1
for i in range(6, len(tspLines) - 1):
    try:
        cities[j] = [int(s) for s in tspLines[i].split()]
    except ValueError:
        cities[j] = [float(s) for s in tspLines[i].split()]
    j += 1

# tour refers to a list of the input cities arranged into some solution
tour = greedySearch(cities)

# while the time the program has been running for is less than the maximum allowed running time,
# continue to look for solutions
while time.time() < (startTime + int(maxTime)):
    step += 1
    tour = greedyTwoOptSolver(tour)


printTourToConsole(tour)
