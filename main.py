import random
import math
import time

c = 3
m = 3
cb = 2
randomStrategyIterations = 10
noOfTransitionsWithoutSuccess = 100
maxTreeDepth = 999


class State:
    def __init__(self, c1, m1, c2, m2, pb):
        self.c1 = c1
        self.m1 = m1
        self.c2 = c2
        self.m2 = m2
        self.pb = pb
        self.visited = False

    def isFinal(self):
        return self.c1 == 0 and self.m1 == 0

    def isValid(self):
        if self.pb == 1 and (self.c1 + self.m1 <= 0):
            return False
        if self.pb == 2 and (self.c2 + self.m2 <= 0):
            return False
        return (self.c1 <= self.m1 or self.m1 == 0) and (self.c2 <= self.m2 or self.m2 == 0) and (self.c1 + self.c2 == c and self.m1 + self.m2 == m)

    def __str__(self):
        return f'c1: {self.c1}, m1: {self.m1}, c2: {self.c2}, m2: {self.m2}, pb: {self.pb}'

    def __eq__(self, other):
        return self.c1 == other.c1 and self.m1 == other.m1 and self.c2 == other.c2 and self.m2 == other.m2 and self.pb == other.pb


class Transition:
    def __init__(self, c, m):
        self.c = c
        self.m = m

    def __str__(self):
        return f'c: {self.c}, m: {self.m}'

    def __eq__(self, other):
        return self.c == other.c and self.m == other.m


def getInitialState():
    return State(c, m, 0, 0, 1)


def isTransitionValid(transition):
    if transition is None:
        return False
    if transition.c > transition.m and transition.m > 0:
        return False
    if transition.c == 0 and transition.m == 0:
        return False
    if transition.c + transition.m > cb:
        return False
    if transition.c < 0 or transition.m < 0:
        return False
    return True


def makeTransition(state, transition):
    if state.pb == 1:
        return State(state.c1 - transition.c, state.m1 - transition.m, state.c2 + transition.c, state.m2 + transition.m, 2)
    return State(state.c1 + transition.c, state.m1 + transition.m, state.c2 - transition.c, state.m2 - transition.m, 1)


def getRandomTransition(State):
    if State.pb == 1:
        cannibals = State.c1
        missionaires = State.m1
    else:
        cannibals = State.c2
        missionaires = State.m2

    cr = random.randint(0, min(cannibals, cb))
    if cr > min(missionaires, cb - cr):
        return Transition(cr, 0)
    mr = random.randint(cr, min(missionaires, cb-cr))
    return Transition(cr, mr)


def randomStrategy():
    states = buildPossibleStates()

    for i in range(randomStrategyIterations):
        # print(f'Iteration {i}...')
        # Iau o referinta direct catre acel obiect din states
        # O noua iteratie, setez toate visited pe False
        for state in states:
            state.visited = False
        currentState = ([state for state in states if state.c1 ==
                         c and state.m1 == m and state.pb == 1])[0]
        currentState.visited = True
        statesTraversed = [currentState]
        for _ in range(noOfTransitionsWithoutSuccess):
            # Aleg o stare random
            transition = getRandomTransition(currentState)
            resultingState = makeTransition(currentState, transition)
            if resultingState.isValid() == False:
                continue

            stateInStatesList = [
                state for state in states if state == resultingState]
            stateInStatesList = stateInStatesList[0]
            stateInStatesList.visited = True
            statesTraversed.append(stateInStatesList)
            currentState = stateInStatesList

            if currentState.isFinal() == True:
                return statesTraversed

    return None


def backtrackingStrategy(state, statesTraversed=[], done=[False]):
    global states

    state.visited = True

    if state.isFinal():
        done[0] = True
        return statesTraversed

    for newState in states:
        if newState.visited == True:
            continue
        transition = buildTransitionBetweenStates(state, newState)
        if isTransitionValid(transition):
            statesTraversed.append(newState)
            backtrackingStrategy(newState, statesTraversed, done)
            if (done[0] == True):
                return statesTraversed
            statesTraversed.pop(len(statesTraversed) - 1)
            newState.visited = False


def buildTransitionBetweenStates(state1, state2):
    """
    Builds a transition that gets us from `state1` to `state2`
    """
    if state1.pb == state2.pb:
        # between the states, the boat's position must change
        return None
    if state1.pb == 1:
        # I brought cannibals and missionaries on the second island
        return Transition(state2.c2 - state1.c2, state2.m2 - state1.m2)
    # else, I brought cannibals and missionaries on the first island
    return Transition(state2.c1 - state1.c1, state2.m1 - state1.m1)


def buildPossibleStates():
    states = []
    for c1 in range(0, c + 1):
        for m1 in range(0, m + 1):
            for c2 in range(0, c + 1):
                for m2 in range(0, m + 1):
                    for pb in [1, 2]:
                        state = State(c1, m1, c2, m2, pb)
                        if state.isValid():
                            states.append(state)
    return states


def buildEdgesBetweenStates(states):
    M = [None] * len(states)

    for index0, s0 in enumerate(states):
        for index1, s1 in enumerate(states):
            transition = buildTransitionBetweenStates(s0, s1)
            if isTransitionValid(transition):
                if M[index0] is not None:
                    M[index0].append(index1)
                else:
                    M[index0] = [index1]
    return M


def solveWithBacktrackingStrategy():
    global states
    states = buildPossibleStates()
    initialState = ([state for state in states if state.c1 ==
                     c and state.m1 == m and state.pb == 1])[0]
    statesTraversed = backtrackingStrategy(initialState, [initialState])
    if statesTraversed is not None and statesTraversed[-1].isFinal():
        return statesTraversed

    return None


def solveWithIDDFSStrategy():
    global states, M
    states = buildPossibleStates()
    M = buildEdgesBetweenStates(states)
    indexOfInitialState = ([index for (index, state) in enumerate(states) if state.c1 ==
                            c and state.m1 == m and state.pb == 1])[0]

    states[indexOfInitialState].visited = True
    for i in range(1, maxTreeDepth):
        statesTraversed = [indexOfInitialState]
        DLS(i, indexOfInitialState, statesTraversed)
        if states[statesTraversed[-1]].isFinal():
            return statesTraversed

    return None


def DLS(limit, stateIndex, statesTraversed, done=[False]):
    global states, M

    if states[stateIndex].isFinal():
        done[0] = True
        print(f'IDDFS needs a limit of {-limit}')
        return

    # if limit == 0:
    #     return

    for neighbourIndex in M[stateIndex]:
        if states[neighbourIndex].visited == False:
            states[neighbourIndex].visited = True
            statesTraversed.append(neighbourIndex)
            DLS(limit - 1, neighbourIndex, statesTraversed, done)

            if done[0] == True:
                return

            states[neighbourIndex].visited = False
            statesTraversed.pop(len(statesTraversed) - 1)


def heuristic(state, finalState=State(0, 0, c, m, 2)):
    return (state.c1 + state.m1)//cb + (state.c1 + state.m1)//(cb*2)
    # return 0
    # if state.pb == 1:
    #     return state.c1 + state.m1 - 1
    # return state.c1 + state.m1
    return state.c2 + state.m2


def astarStrategy():
    states = buildPossibleStates()
    M = buildEdgesBetweenStates(states)
    indexOfFinalState = ([index for (index, state) in enumerate(states) if state.c2 ==
                          c and state.m2 == m and state.pb == 2])[0]
    d = [math.inf] * len(states)
    indexOfInitialState = ([index for (index, state) in enumerate(states) if state.c1 ==
                            c and state.m1 == m and state.pb == 1])[0]
    d[indexOfInitialState] = 0
    Q = [indexOfInitialState]
    indexStateIsInQ = [False] * len(states)
    indexStateIsInQ[indexOfInitialState] = True

    while len(Q) > 0:
        # scot urmatorul element din coada
        currentStateIndex = Q.pop()
        indexStateIsInQ[currentStateIndex] = False

        # if d[indexOfFinalState] != math.inf:
        #     break

        for neighbourIndex in M[currentStateIndex]:
            # fac update la vecini
            if d[currentStateIndex] + 1 < d[neighbourIndex]:
                d[neighbourIndex] = d[currentStateIndex] + 1
                if indexStateIsInQ[neighbourIndex] == False:
                    # Nu il am in coada, deci il pun
                    Q.append(neighbourIndex)
                    indexStateIsInQ[neighbourIndex] = True

        # sortez Q
        sorted(Q, key=lambda x: d[x] + heuristic(states[x]))
        # min heap pentru bonus

    if d[indexOfFinalState] != math.inf:
        # print(f'Am gasit o rezolvare cu lungime {d[indexOfFinalState]}')
        # print('A fost traseu, mai exact:')
        traseu = [indexOfFinalState]
        currentStateIndex = indexOfFinalState

        while d[currentStateIndex] > 0:
            for neighbourIndex in M[currentStateIndex]:
                if d[currentStateIndex] == d[neighbourIndex] + 1:
                    traseu.append(neighbourIndex)
                    currentStateIndex = neighbourIndex
                    break
        # for index in traseu[::-1]:
        #     print(states[index])
        # print(f'Am trecut print {len(traseu)} stari')
        # print(traseu[::-1])
        statesTraversed = list(map(lambda x: states[x], traseu[::-1]))
        return statesTraversed
    else:
        # print('A* did not find a solution :(')
        return None


def timeFunction(function):
    start = time.time()
    states = function()
    if states is not None:
        length = len(states)
        print(f'{function.__name__} found a solution with a length of {length}')
        # for state in states:
        #     print(state)
    else:
        print(f'{function.__name__} did not find a solution')
        length = None
    end = time.time()
    # print (f'Execution took {(end-start)*1000} milliseconds')
    return end-start, length


def main():
    global c, m
    noOfIterations = 10

    functions = [randomStrategy, solveWithBacktrackingStrategy,
                 solveWithIDDFSStrategy, astarStrategy]
    # functions = [solveWithBacktrackingStrategy]
    times = {}
    lengths = {}
    noOfSolutionsFound = {}
    for function in functions:
        times[function] = 0
        lengths[function] = 0
        noOfSolutionsFound[function] = 0

    for i in range(0, noOfIterations):
        m = random.randint(3, 15)
        c = random.randint(3, m)
        cb = random.randint(2, 5)
        # c, m, cb = 7, 14, 4

        for function in functions:
            functionTime, functionLength = timeFunction(function)
            times[function] += functionTime
            if functionLength is not None:
                # a gasit solutie
                lengths[function] += functionLength
                noOfSolutionsFound[function] += 1

    print('\n\n')
    for function in functions:
        print(
            f'{function.__name__} found {noOfSolutionsFound[function]}/{noOfIterations} solutions')
        print(
            f'{function.__name__} took on average, {times[function] * 1000 / noOfIterations} milliseconds')
        if noOfSolutionsFound[function] == 0:
            print(f'{function.__name__} did not find any solution at all :(')
        else:
            print(
                f'{function.__name__} had an average length of {lengths[function] / noOfSolutionsFound[function]}')
        print('')


main()
