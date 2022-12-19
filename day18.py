# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
import functools
import heapq
import math
import json
import time

from typing import List, Tuple
from collections import defaultdict
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def manhattanDistance(coord1, coord2):
    return abs(coord1[0] - coord2[1]) + abs(coord1[1]-coord2[0])

def isAccessible(currentElevation, targetElevation):
    return alphabet.index(currentElevation) - alphabet.index(targetElevation) <= 1


def getAdjacent(coord):
    patterns = [(0,1), (0,-1), (1,0), (-1,0)]

    return [(coord[0] + p[0], coord[1] + p[1]) for p in patterns]


maze = []

def isInBounds(coord, maxCoord, minCoord):
    return not(coord[0] < minCoord[0] or coord[1] < minCoord[1] or coord[2] < minCoord[2] or coord[0] >= maxCoord[0] or coord[1] >= maxCoord[1] or coord[2] >= maxCoord[2])

def getAdjacentInBounds(coord):
    inBounds = [x for x in getAdjacent(coord) if isInBounds(x)]
    currentPosChar = maze[coord[1]][coord[0]]
    reachable = []
    for x in inBounds:
        targetSpaceChar = maze[x[1]][x[0]]
        if isAccessible(currentPosChar, targetSpaceChar):
            reachable.append(x)

    return reachable


def getAdjacentCubes(cubeCoord, diagonal=False):
    pattern = [(1,0,0), (-1,0,0), (0,1,0), (0,-1, 0), (0,0,1), (0,0,-1)]
    if diagonal:
        pattern += [(1,1,0), (1, -1, 0), (-1,1,0),(-1,-1,0),(1, 0, 1), (1, 0, -1), (-1, 0, 1), (-1, 0, -1), (0, 1, 1), (0, 1, -1), (0, -1, 1), (0, -1, -1)]
    adjCoords = []
    for pattern in pattern:
        adjCoords.append((cubeCoord[0] + pattern[0], cubeCoord[1] + pattern[1], cubeCoord[2] + pattern[2]))
    return adjCoords

def print_hi2():
    # f = open('sample.txt', 'r')
    f = open('input18.txt', 'r')
    intera = iter(f)

    adjaccentSides = defaultdict(lambda: 0)

    for line in intera:
        pieces = [int(x) for x in line.split(',')]

        x, y, z = pieces

        adjacentCubes = getAdjacentCubes((x,y,z))

        adjaccentSides[(x,y,z)] = 0

        for cube in adjacentCubes:
            if cube in adjaccentSides:
                adjaccentSides[cube] += 1
                adjaccentSides[(x,y,z)] += 1

    maxX = max([x[0] for x in adjaccentSides]) + 2
    maxY = max([x[1] for x in adjaccentSides]) + 2
    maxZ = max([x[2] for x in adjaccentSides]) + 2

    minX = min([x[0] for x in adjaccentSides]) - 2
    minY = min([x[1] for x in adjaccentSides]) - 2
    minZ = min([x[2] for x in adjaccentSides]) - 2


    toVisit = [(minX, minY, minZ)]
    visited = set([])
    exteriorSides = 0

    while len(toVisit) != 0:
        nextToVisit = toVisit.pop(0)
        visited.add(nextToVisit)
        # print(len(toVisit), len(visited))

        adjacentCubes = getAdjacentCubes(nextToVisit)

        for adjCube in adjacentCubes:
            if adjCube in adjaccentSides:
                exteriorSides += 1
            elif adjCube not in visited and adjCube not in toVisit and isInBounds(adjCube, (maxX, maxY, maxZ), (minX, minY, minZ)):
                toVisit.append(adjCube)

    openSides = 0
    for cube in adjaccentSides:
        if adjaccentSides[cube] < 6:
            openSides += 6 - adjaccentSides[cube]

    print(openSides)
    print(exteriorSides)



if __name__ == '__main__':
    timeNow = time.time()
    total = print_hi2()
    print(time.time() - timeNow)
