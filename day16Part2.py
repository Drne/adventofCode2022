import sys
import time

def print_hi2():
    # f = open('sample.txt', 'r')
    f = open('input.txt', 'r')
    intera = iter(f)
    adjacency = {}
    flowMap = {}

    for line in intera:
        pieces = line.split(' ')
        name: str = pieces[1]
        flow = int(pieces[4][5:-1])
        connections = pieces[9:]
        connections = [x.replace(',', '') for x in connections]
        connections = [x.replace('\n', '') for x in connections]
        flowMap[name] = flow
        adjacency[name] = [(conn, 1) for conn in connections]

    bestFlow = 0
    goals = [x for x in flowMap if flowMap[x] > 0]
    zeroes = [x for x in flowMap if flowMap[x] == 0]

    def getNewAdjs(location, baseCost, visited):
        # for each neighbor:
        # if goal, add base to adjacent
        # if zero, add adjacents generated from that to adj
        newAdj = []
        for neighbor in adjacency[location]:
            if neighbor[0] not in visited:
                if neighbor[0] in zeroes:
                    adjs = getNewAdjs(neighbor[0], baseCost + 1, visited.union({neighbor[0]}))
                    newAdj = newAdj + adjs
                else:
                    newAdj.append((neighbor[0], baseCost))

        return newAdj

    newAdj = {}
    for goal in goals + zeroes:
        newAdj[goal] = list(set(getNewAdjs(goal, 1, {goal})))

    adjacency = newAdj

    newThings = {}
    for goal in goals:
        visited = {goal}
        newAds = []
        cost = {}
        for adj in adjacency[goal]:
            cost[adj[0]] = adj[1]
        toVisit = [x[0] for x in adjacency[goal]]
        while len(toVisit) != 0:
            visiting = toVisit.pop(0)
            visited.add(visiting)
            visitCost = cost[visiting]
            for neigh in adjacency[visiting]:
                if neigh[0] not in visited and neigh[0] not in toVisit:
                    neighVisitCost = visitCost + neigh[1]
                    cost[neigh[0]] = neighVisitCost
                    newAds.append((neigh[0], neighVisitCost))
                    toVisit.append(neigh[0])

        newThings[goal] = newAds + adjacency[goal]
    print('done!')
    for x in adjacency:
        if x in zeroes:
            newThings[x] = adjacency[x]
    adjacency = newThings

    def tunnelStep(flowRate, opened, path, elePath):
        whenHumanCanActAgain = 26 if len(path) == 0 else path[-1][1]
        whenElepahantCanActAgain = 26 if len(elePath) == 0 else elePath[-1][1]

        timeLeft = min(whenHumanCanActAgain, whenElepahantCanActAgain)
        if timeLeft <= 1 or len(opened) == len(goals):
            # print(flowRate, path, timeLeft)
            return (flowRate, path, elePath, timeLeft)

        currentHumanLocale = path[-1][0]
        currentElephantLocale = elePath[-1][0]
        location = currentHumanLocale if whenHumanCanActAgain >= whenElepahantCanActAgain else currentElephantLocale
        bestFlows = [(0, [location])]
        targets = [g for g in adjacency[location] if g[0] not in opened and flowMap[goal] > 0 and g[1] < timeLeft]
        for targ in targets:
            openedCopy = opened.copy()
            openedCopy.add(targ[0])
            timeToOpen = targ[1] + 1

            if whenHumanCanActAgain >= whenElepahantCanActAgain:
                timeLeft = 30 if len(path) == 0 else path[-1][1]
                pathCopy = path.copy()
                pathCopy.append((targ[0], timeLeft - timeToOpen))
                bestFlows.append(tunnelStep(flowRate + flowMap[targ[0]] * (timeLeft - timeToOpen), openedCopy, pathCopy, elePath))
            else:
                timeLeft = 30 if len(elePath) == 0 else elePath[-1][1]
                pathCopy = elePath.copy()
                pathCopy.append((targ[0], timeLeft - timeToOpen))
                bestFlows.append(tunnelStep(flowRate + flowMap[targ[0]] * (timeLeft - timeToOpen), openedCopy, path, pathCopy))

        return max(bestFlows, key=lambda x: x[0])

    tm = time.time()
    bestFlow = tunnelStep(0, set([]), [('AA', 26)], [('AA', 26)])
    print(bestFlow)
    print(time.time() - tm)
    # for x in adjacency:
    #     print(x, adjacency[x])

# 1820 - too low

sys.setrecursionlimit(2000)
if __name__ == '__main__':
    total = print_hi2()
