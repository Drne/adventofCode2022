# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
import functools
import heapq
import math
import json

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

    packetPairs = []
    for line in intera:
        pair = []
        if line != '\n':
            packetPairs.append(json.loads(line))

            line = intera.__next__()

            packetPairs.append(json.loads(line))
            # packetPairs.append(pair)

    def comparePackets(value, value2):
        print('comparing ', value, ' ', value2)
        if isinstance(value, int):
            if isinstance(value2, int):
                if (value == value2):
                    return 'keep checking'
                print('comparing ', value, ' ', value2)
                return value < value2
            else:
                print('comparing ', [value], value2)
                return comparePackets([value], value2)
        elif isinstance(value2, int):
            return comparePackets(value, [value2])

        for inx, val in enumerate(value):
            if (inx >= len(value2)):
                print('ran out of right values', value, value2)
                break
            val2 = value2[inx]
            comparison = comparePackets(val, val2)
            if (comparison == 'keep checking'):
                print('same ', val, ' ', val2)
                continue
            else:
                print(comparison, val, val2)
                return comparison

        if len(value2) < len(value):
            print('right value less than first ', value, value2)
            return False

        if len(value2) == len(value):
            print('keep checking', value, value2)
            return 'keep checking'

        print('left ran out!')
        return True


    totalRight = 0
    # for inx, packetPair in enumerate(packetPairs):
    #     if comparePackets(packetPair[0], packetPair[1]):
    #         print('good!')
    #         totalRight += inx + 1
    #     else:
    #         print('bad')

    def compare(x,y):
        return -1 if comparePackets(x, y) else 1
    sorte = sorted(packetPairs, key=functools.cmp_to_key(compare))
    print(sorte.index([[2]]))
    print(sorte.index([[6]]))
    print((sorte.index([[2]]) + 1) * (sorte.index([[6]]) + 1))

if __name__ == '__main__':
    total = print_hi2()

# 2405
# 5724