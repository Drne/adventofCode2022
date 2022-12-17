# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
import heapq
import math

from typing import List, Tuple

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def manhattanDistance(coord1, coord2):
    return abs(coord1[0] - coord2[1]) + abs(coord1[1]-coord2[0])

def isAccessible(currentElevation, targetElevation):
    return alphabet.index(currentElevation) - alphabet.index(targetElevation) <= 1


def getAdjacent(coord):
    patterns = [(0,1), (0,-1), (1,0), (-1,0)]

    return [(coord[0] + p[0], coord[1] + p[1]) for p in patterns]


maze = []

def isInBounds(coord):
    return not(coord[0] < 0 or coord[1] < 0 or coord[1] >= len(maze) or coord[0] >= len(maze[0]))

def getAdjacentInBounds(coord):
    inBounds = [x for x in getAdjacent(coord) if isInBounds(x)]
    currentPosChar = maze[coord[1]][coord[0]]
    reachable = []
    for x in inBounds:
        targetSpaceChar = maze[x[1]][x[0]]
        if isAccessible(currentPosChar, targetSpaceChar):
            reachable.append(x)

    return reachable


def print_hi2():
    # f = open('sample.txt', 'r')
    f = open('input.txt', 'r')
    intera = iter(f)

    currentPosition = None
    targetPosition = None

    for line in intera:
        line = line.replace('\n', '')
        if 'S' in line:
            currentPosition = (line.index('S'), len(maze))
            line = line.replace('S', 'a')

        if 'E' in line:
            targetPosition = (line.index('E'), len(maze))
            line = line.replace('E', 'z')

        maze.append(line)

    def calcPrio(coord):
        char = maze[coord[1]][coord[0]]
        return 26 - alphabet.index(char) - manhattanDistance(coord, targetPosition)

    visited = {targetPosition}
    toVisit = [(j, 1) for j in getAdjacentInBounds(targetPosition) if j not in visited]

    elemsInMaz = len(maze[0]) * len(maze)

    while len(toVisit) != 0:
        # if (len(visited) % 10 == 0):
        #     print(len(visited) / elemsInMaz * 100)
        visting = toVisit.pop(0)
        visited.add(visting[0])

        coord = visting[0]
        charInMaze = maze[coord[1]][coord[0]]
        if charInMaze == 'a':
            print(visting[0], visting[1])
            break

        for y in [(x, visting[1] + 1) for x in getAdjacentInBounds(visting[0]) if x not in visited and (x, visting[1] + 1) not in toVisit]:
            toVisit.append(y)

if __name__ == '__main__':
    total = print_hi2()

