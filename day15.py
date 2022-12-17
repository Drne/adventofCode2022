# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
import heapq
import math
from collections import defaultdict
from typing import List, Tuple

alphabet = 'abcdefghijklmnopqrstuvwxyz'


def manhattanDistance(coord1, coord2):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])


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


def manhattanDistance(coord1, coord2):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])


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


impossibleSpots = set([])
beacons = set([])
ranges = defaultdict(lambda: [])


def print_hi2():
    # f = open('sample.txt', 'r')
    f = open('input.txt', 'r')
    intera = iter(f)

    maxSize = 4000000
    # maxSize = 20

    for line in intera:
        line = line.split(' ')
        sensorX = int(line[2][2:-1])
        sensorY = int(line[3][2:-1])

        beaconX = int(line[8][2:-1])
        beaconY = int(line[9][2:])

        sOrigin = (sensorX, sensorY)
        toVisit = [sOrigin]
        visited = set()

        beacons.add((beaconX, beaconY))
        beacons.add(sOrigin)

        print('starting search of ', sensorX, sensorY)

        distanceBetween = manhattanDistance((sensorX, sensorY), (beaconX, beaconY))
        farthestLeft = sOrigin[0] - distanceBetween
        farthestRightX = sOrigin[0] + distanceBetween
        highestY = sOrigin[1] + distanceBetween
        lowestY = sOrigin[1] - distanceBetween
        if not (lowestY > maxSize or farthestLeft > maxSize or highestY < 0 or farthestRightX < 0):
            cappedX = min(farthestRightX, maxSize)
            cappedY = min(highestY, maxSize)
            floorX = max(farthestLeft, 0)
            floorY = max(lowestY, 0)
            for y in range(floorY, cappedY+1):
                xRange = (distanceBetween - abs(sOrigin[1] - y))
                leftX = (sOrigin[0] - xRange, sOrigin[0] + xRange)
                if leftX[0] <= maxSize and leftX[1] >= 0:
                    ranges[y].append((max(leftX[0], 0), (min(leftX[1], maxSize))))

    for y in ranges:
        content = ranges[y]
        content.sort()

        currentLow = 0
        for pair in content:
            if pair[0] >= maxSize:
                break
            if pair[0] - 1 <= currentLow:
                currentLow = max(currentLow, pair[1])
            else:
                print('found it!')
                print(y, pair, content)
                print((pair[0] - 1) * maxSize + y)
                break

if __name__ == '__main__':
    total = print_hi2()
