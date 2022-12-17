import sys
import time


def print_hi2():
    # f = open('sample.txt', 'r')
    f = open('input.txt', 'r')
    intera = iter(f)
    adjacency = {}
    flowMap = {}
    start = 'AA'
    maxTime = 30

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

    def tunnelStep(timeLeft, location, flowRate, opened, path):
        if timeLeft <= 1 or len(opened) == len(goals):
            # print(flowRate, path, timeLeft)
            return (flowRate, path, timeLeft)

        bestFlows = [(0, [location])]
        targets = [g for g in adjacency[location] if g[0] not in opened and flowMap[goal] > 0 and g[1] < timeLeft]
        for targ in targets:
            openedCopy = opened.copy()
            openedCopy.add(targ[0])
            timeToOpen = targ[1] + 1
            pathCopy = path.copy()
            pathCopy.append(targ[0])
            bestFlows.append(tunnelStep(timeLeft - timeToOpen, targ[0], flowRate + flowMap[targ[0]] * (timeLeft - timeToOpen), openedCopy, pathCopy))

        return max(bestFlows, key=lambda x: x[0])

    timeNow = time.time()

    bestFlow = tunnelStep(30, 'AA', 0, set([]), [])
    print(time.time() - timeNow)
    print(bestFlow)
    # for x in adjacency:
    #     print(x, adjacency[x])

sys.setrecursionlimit(2000)
if __name__ == '__main__':
    total = print_hi2()
