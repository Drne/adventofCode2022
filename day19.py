import re
import time

ore = 'ore'
clay = 'clay'
obsidian = 'obsidian'
geode = 'geode'

def print_hi2():
    f = open('day19Sample.txt', 'r')
    # f = open('input18.txt', 'r')
    intera = iter(f)

    blueprints = {}
    for line in intera:
        robotNum = int(line[10])
        line = line.replace('\n', '')
        periodPieces = line.split('.')
        cost = {}
        for robotInfo in periodPieces:
            if robotInfo:
                pieces = robotInfo.split('costs')
                robotType = pieces[0].split(' ')[-3]
                componentCosts = {}
                costString = pieces[1].strip()
                costPieces = costString.split('and')
                costPieces = [x.strip() for x in costPieces]
                for costP in costPieces:
                    costComponents = costP.split(' ')
                    componentCosts[costComponents[1]] = int(costComponents[0])
                cost[robotType] = componentCosts
        blueprints[robotNum] = cost

    def getPossibleTargets(blueprint, generating):
        target = []

        for robot in blueprint:
            if all([generating[resource] > 0 for resource in blueprint[robot]]):
                target.append(robot)

        target.reverse()
        return target

    def canAffordRobot(name, inventory, blueprint):
        costDict = blueprint[name]

        for material in costDict:
            if inventory[material] < costDict[material]:
                return False
        return True

    def makeRobot(name, inventory, generating, blueprint):
        costDict = blueprint[name]
        for material in costDict:
            inventory[material] -= costDict[material]
        generating[name] += 1

    def factoryStep(time, inventory, generating, target, blueprint, targetList):
        if time <= 0:
            # print(targetList)
            return inventory[geode]

        robotToAdd = None

        if target is not None and canAffordRobot(target, inventory, blueprint):
            robotToAdd = target

        for resource in generating:
            inventory[resource] += generating[resource]

        if target is None:
            potentialTargets = getPossibleTargets(blueprint, generating)
            maxGeodes = []
            for valTarget in potentialTargets:
                maxGeode = factoryStep(time - 1, inventory.copy(), generating.copy(), valTarget, blueprint, [valTarget])
                maxGeodes.append(maxGeode)
            return max(maxGeodes)

        elif robotToAdd is None:
            return factoryStep(time-1, inventory, generating, target, blueprint, targetList)

        else:
            makeRobot(robotToAdd, inventory, generating, blueprint)
            nextTargets = getPossibleTargets(blueprint, generating)
            maxGeodes = []
            for validTarget in nextTargets:
                newTargetList = targetList[:]
                newTargetList.append(validTarget)
                maxGeode = factoryStep(time - 1, inventory.copy(), generating.copy(), validTarget, blueprint, newTargetList)
                maxGeodes.append(maxGeode)
            return max(maxGeodes)

    maxGeo = {}

    for blue in blueprints:
        print('next blueprint!', blue)
        maxTime = 24
        inventory = {ore: 0, clay: 0, obsidian: 0, geode: 0}
        generating = {ore: 1, clay: 0, obsidian: 0, geode: 0}
        target = None
        blueprint = blueprints[blue]
        number = blue
        maxGeodes = factoryStep(maxTime, inventory, generating, target, blueprint, [])
        maxGeo[number] = maxGeodes

    print(maxGeo)





if __name__ == '__main__':
    timeNow = time.time()
    total = print_hi2()
    print(time.time() - timeNow)
