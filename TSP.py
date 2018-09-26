import sys, math, time, os
import mysql.connector

def consoleFileHandle(name):
    try:
        with open(name) as tspfile:
            line = tspfile.readlines()
    except FileNotFoundError:
        print("TSP File does not exist or cannot be opened")
        return 0

    return line


def consoleTimeHandle():
    maxtime = sys.argv[1]
    return maxtime


def databaseSolutionHandle(name):
    sql_Command = str("SELECT Name from Problem WHERE(Name = '" + name + "');")
    cursor.execute(sql_Command)
    name = cursor.fetchone()

    if name is None:
        print("Input problem does not exist in the database")
        sys.exit(1)

    sql_Command = ("SELECT NodeCoordinate from Nodes WHERE(ProblemName = '" + name[0] + "');")
    cursor.execute(sql_Command)
    nodes = cursor.fetchall()
    nodes = [x[0] for x in nodes]
    for x in range(0, 6):
        nodes.insert(x, 0)

    return nodes


def databaseEntityHandle():
    list = consoleFileHandle(sys.argv[3])
    cursor.execute("SELECT * from Problem where(Name = '" + name + "');")
    getName = (cursor.fetchone())

    if getName is not None:
        if getName[0] == name:
            print("Name Already exists in the database")
            sys.exit(1)

    comment = list[1][9:-1]
    problemType = list[4][18:-1]
    dimension = list[3][10:-1]

    if comment is None or problemType is None or dimension is None:
        print("One or more problem description fields could not be filled.")

    createTables = ("INSERT INTO Problem(Name) VALUES('" + sys.argv[1] + "');")
    cursor.execute(createTables)

    createTables = ("INSERT INTO Description(ProblemName, ProblemComment, ProblemType, Dimension) "
                    "VALUES('" + sys.argv[1] + "', '" + comment + "', '" + problemType + "', '" + dimension + "');")
    cursor.execute(createTables)

    for x in range(6, len(list) - 1):
        nodeIndex = list[x].split()[0]
        xCoord = list[x].split()[1]
        yCoord = list[x].split()[2]
        createTables = ("INSERT INTO Nodes(ProblemName,NodeCoordinate,ProblemIndex,XCoord,YCoord) "
                        "VALUES('" + sys.argv[1] + "'," + "'" + list[x] + "',"
                        + nodeIndex + "," + xCoord + "," + yCoord + ");")
        cursor.execute(createTables)

    connection.commit()



def dataBaseFileHandle(cmdLineCommand):
    if cmdLineCommand == 'ADD':
        databaseEntityHandle()
        print(name + " has been added to the database")
        sys.exit()
    elif cmdLineCommand == 'SOLVE':
        return int(sys.argv[3])
    elif cmdLineCommand == 'FETCH':
        sql_Command = "SELECT Name FROM Problem WHERE(Name = '" + name + "');"
        cursor.execute(sql_Command)
        dbName = cursor.fetchone()

        if dbName is None:
            print("Input solution could not be found")
            sys.exit(1)

        sql_Command = "SELECT OptimalSolution FROM Problem WHERE(Problem.name = '" + name + "');"

        cursor.execute(sql_Command)
        print("Optimal Solution for " + name + ": ")
        print(cursor.fetchone()[0])
        sys.exit()
    else:
        print("Command not recognised")
        sys.exit(1)


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


def greedySearch(cities):
    lowestCity = cities[1]
    lowestDistance = abs(cities[1][1] - cities[2][1] + cities[1][2] - cities[2][2])
    totalDistancef = 0
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
                    totalDistancef += distance
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

    n = str(totalDistance(returnTour))
    #sql_command = ("UPDATE Problem SET GreedySolution = " + n + " WHERE(Name = '" + name + "');")
    #cursor.execute(sql_command)
    #connection.commit()
    return returnTour


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


def printTourToConsole(tour, bestSolution):
    finalDistance = totalDistance(tour)

    if bestSolution is None:
        bestSolution = finalDistance
    if finalDistance <= bestSolution:
        cursor.execute("UPDATE Problem SET OptimalSolution = " + str(finalDistance) + " WHERE(Name = '" + name + "');")
        connection.commit()

    print(name, "\n", "Final tour length: ", finalDistance, "\n", "Tour:")
    for x in range(0, len(tour)):
            print(int(tour[x][0]))
            
def TourToString(tour):
    tourString = ""
    for x in range(0, len(tour)):
        tourString += str(tour[x][0])
        tourString += " "
        
    tourString += "-1"    
    return tourString

def generateCities(tspLines):
    cities = [0] * len(tspLines)
    j = 1
    for i in range(6, len(tspLines) - 1):
        try:
            cities[j] = [int(s) for s in tspLines[i].split()]
        except ValueError:
            cities[j] = [float(s) for s in tspLines[i].split()]
        j += 1
    return cities


def old():
    name = 'name'
    command = 'command'
    
    try: 
        connection = mysql.connector.connect(host = 'mysql.ict.griffith.edu.au',
                                             database = 's5132012db',
                                             user = 's5132012',
                                             password = 'XwxXSo4j')
    except:
        print("Cannot Connect to Database")
        input("Press enter to exit")
    
    if connection.is_connected():
        print('Connected to the database')
        
    cursor = connection.cursor()
    
    #uptohere
    maxTime = dataBaseFileHandle(command)
    cursor.execute("SELECT OptimalSolution FROM Problem WHERE(Name = '" + name + "');")
    bestSolution = cursor.fetchone()[0]
    
    
    tspLines = databaseSolutionHandle(name)
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
    
    
    printTourToConsole(tour, bestSolution)
