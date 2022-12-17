# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
import functools
import heapq
import math
import json

from typing import List, Tuple

def manhattanDistance(coord1, coord2):
    return abs(coord1[0] - coord2[1]) + abs(coord1[1]-coord2[0])

def getAdjacent(coord):
    patterns = [(0,1), (0,-1), (1,0), (-1,0)]

    return [(coord[0] + p[0], coord[1] + p[1]) for p in patterns]


def isInBounds(coord, maxX, maxY):
    return not(coord[0] < 0 or coord[1] < 0 or coord[1] > maxY or coord[0] > maxX)


def getAdjacentInBounds(coord, maxX, maxY):
    inBounds = [x for x in getAdjacent(coord) if isInBounds(x, maxX, maxY)]
    reachable = []
    for x in inBounds:
        reachable.append(x)

    return reachable

rock0 = [(0,0), (1,0), (2,0),(3,0)]
rock1 = [(1,0), (0,-1), (1,-1), (2,-1), (1,-2)]
rock2 = [(2,0), (2,-1), (2,-2), (0,-2), (1,-2)]
rock3 = [(0,0), (0,-1), (0,-2),(0,-3)]
rock4 = [(0,0), (1,0), (0,-1), (1,-1)]
rocks = [rock0, rock1, rock2, rock3, rock4]
rockHeight = [1, 3, 3, 4, 2]

def rockCoordinates(originCoord, rockNum):
    return [(originCoord[0] + rock[0], originCoord[1] + rock[1]) for rock in rocks[rockNum]]

def moveDirection(coords, direction):
    if direction == '<':
        return [(coord[0] - 1, coord[1]) for coord in coords]
    elif direction == '>':
        return [(coord[0] + 1, coord[1]) for coord in coords]
    else:
        return [(coord[0], coord[1] - 1) for coord in coords]

def areAllInBounds(coords, maxX, maxY):
    return all([isInBounds(coord, maxX, maxY) for coord in coords])

def print_hi2():
    f = open('sample.txt', 'r')
    # f = open('input.txt', 'r')
    intera = iter(f)

    moves = []
    for line in intera:
        for char in line:
            moves.append(char)

    currentY = 0
    spaceOffGround = 3
    xOrigin = 3
    numRocks = 0
    maxRocks = 2022
    # maxRocks = 10
    currentRock = -1
    currentGasIndex = -1
    occupied = set([])

    def getNextGas():
        nonlocal currentGasIndex

        currentGasIndex += 1
        if currentGasIndex == len(moves) - 1:
            currentGasIndex = -1
        return moves[currentGasIndex]

    def getNextRock():
        nonlocal currentRock

        currentRock += 1
        if currentRock == len(rocks) - 1:
            currentRock = -1
        return currentRock

    def isInvalidCoordSpace(coord):
        return (coord in occupied) or not(isInBounds(coord, 7, math.inf))

    while numRocks <= maxRocks:
        # handle rock fall
        numRocks += 1
        rock = getNextRock()
        rockHeightOffset = rockHeight[rock]
        currentRockCoords = rockCoordinates((xOrigin, currentY + rockHeightOffset + spaceOffGround), rock)
        print('rock ', rock, ' starting at ', (xOrigin, currentY + rockHeightOffset + spaceOffGround ))
        moveRight = True

        while True:
            # print(currentRockCoords)
            if moveRight:
                gasDirection = getNextGas()
                # print('rock moving', 'right' if gasDirection == '>' else 'left')
                prospectiveMove = moveDirection(currentRockCoords, gasDirection)
                if not any([isInvalidCoordSpace(x) for x in prospectiveMove]):
                    currentRockCoords = prospectiveMove
                # else:
                    # print('but nothing happens')
            else:
                # print('rock moving down')
                prospectiveMove = moveDirection(currentRockCoords, 'v')
                if any([isInvalidCoordSpace(x) for x in prospectiveMove]):
                    # print('but nothing happens')
                    break
                else:
                    currentRockCoords = prospectiveMove
            moveRight = not moveRight

        # print('rock come to rest')
        for x in currentRockCoords:
            occupied.add(x)
        maxY = max(x[1] for x in currentRockCoords)
        currentY = maxY

    print(currentY)

if __name__ == '__main__':
    total = print_hi2()

# 2547 - sample