# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
import heapq
import math

from typing import List, Tuple

alphabet = 'abcdefghijklmnopqrstuvwxyz'


def manhattanDistance(coord1, coord2):
    return abs(coord1[0] - coord2[1]) + abs(coord1[1] - coord2[0])


def isAccessible(currentElevation, targetElevation):
    return alphabet.index(currentElevation) - alphabet.index(targetElevation) <= 1


def getAdjacent(coord):
    patterns = []
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            patterns.append((x, y))

    return [(coord[0] + p[0], coord[1] + p[1]) for p in patterns]


maze = []


def isInBounds(coord):
    return not (coord[0] < 0 or coord[1] < 0 or coord[1] >= len(maze) or coord[0] >= len(maze[0]))


def getAdjacentInBounds(coord):
    inBounds = [x for x in getAdjacent(coord) if isInBounds(x)]
    reachable = []
    for x in inBounds:
        reachable.append(x)

    return reachable


def getPointsBetweenPoints(coord1, coord2):
    points = []

    if coord1[0] == coord2[0]:
        yDiff = coord1[1] - coord2[1]
        if yDiff > 0:
            for i in range(yDiff):
                points.append((coord1[0], coord1[1] - i))
        else:
            for i in range(yDiff, 0):
                points.append((coord1[0], coord1[1] - i))

    else:
        xDiff = coord1[0] - coord2[0]
        if xDiff > 0:
            for i in range(xDiff):
                points.append((coord1[0] - i, coord1[1]))
        else:
            for i in range(xDiff, 0):
                points.append((coord1[0] - i, coord1[1]))

    return points


instructions = []


def print_hi2():
    # f = open('sample.txt', 'r')
    f = open('input.txt', 'r')
    intera = iter(f)

    largestY = 0
    largestX = 0
    smallestX = math.inf

    for line in intera:
        line = line.replace('\n', '')
        instruction = line.split(' -> ')
        instruction = [x.split(',') for x in instruction]
        instruction = [(int(x[0]), int(x[1])) for x in instruction]
        for x in instruction:
            if x[1] > largestY:
                largestY = x[1]
            if x[0] > largestX:
                largestX = x[0]
            if x[0] < smallestX:
                smallestX = x[0]

        instructions.append(instruction)

    xRange = largestX - smallestX
    sandSource = (xRange - (largestX - 500) + 250, 0)
    print(xRange)
    for y in range(largestY + 1):
        maze.append(['.' for _ in range(xRange + 1 + 500)])

    maze.append(['.' for _ in range(xRange + 1 + 500)])
    maze.append(['#' for _ in range(xRange + 1 + 500)])

    maze[sandSource[1]][sandSource[0]] = '+'

    print('genning')
    for instruc in instructions:
        for inx, coord in enumerate(instruc):
            if inx == len(instruc) - 1:
                break

            nextIn = instruc[inx + 1]

            parsedCoord1 = (coord[0] - smallestX + 250, coord[1])
            parsedCoord2 = (nextIn[0] - smallestX + 250, nextIn[1])

            points = getPointsBetweenPoints(parsedCoord1, parsedCoord2)

            for point in [parsedCoord2, parsedCoord1] + points:
                maze[point[1]][point[0]] = '#'

    def moveSand(currentCoord):
        inBoundsCoords = getAdjacentInBounds(currentCoord)
        belowCoord = (currentCoord[0], currentCoord[1] + 1)
        if belowCoord not in inBoundsCoords:
            return False

        belowSpace = maze[belowCoord[1]][belowCoord[0]]

        if belowSpace == '.':
            maze[currentCoord[1]][currentCoord[0]] = '.'
            maze[belowCoord[1]][belowCoord[0]] = 'o'
            return belowCoord

        bottomLeft = (currentCoord[0] - 1, currentCoord[1] + 1)
        if bottomLeft not in inBoundsCoords:
            return False

        belowSpace = maze[bottomLeft[1]][bottomLeft[0]]
        if belowSpace == '.':
            maze[currentCoord[1]][currentCoord[0]] = '.'
            maze[bottomLeft[1]][bottomLeft[0]] = 'o'
            return bottomLeft

        bottomRight = (currentCoord[0] + 1, currentCoord[1] + 1)
        if bottomRight not in inBoundsCoords:
            return False

        belowSpace = maze[bottomRight[1]][bottomRight[0]]
        if belowSpace == '.':
            maze[currentCoord[1]][currentCoord[0]] = '.'
            maze[bottomRight[1]][bottomRight[0]] = 'o'
            return bottomRight

        return True

    addedSand = 0
    def addSand():
        maze[sandSource[1]][sandSource[0]] = 'o'
        return sandSource

    sandLoc = addSand()
    while True:
        if sandLoc != False and sandLoc != True:
            sandLoc = moveSand(sandLoc)
        elif sandLoc == True and maze[sandSource[1]][sandSource[0]] == 'o':
            break
        else:
            addedSand += 1
            sandLoc = addSand()

    for x in maze:
        print(x)

    print(addedSand)

if __name__ == '__main__':
    total = print_hi2()
