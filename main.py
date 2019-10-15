import random

c = 3
m = 3
cb = 2
randomStrategyIterations = 10
noOfTransitionsWithoutSuccess = 100


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
        return (self.c1 <= self.m1 or self.m1 == 0) and (self.c2 <= self.m2 or self.m2 == 0) and (self.c1 + self.c2 == c and self.m1 + self.m2 == m)

    def __str__(self):
        return f'm1: {self.m1}, c1: {self.c1}, m2: {self.m2}, c2: {self.c2}, pb: {self.pb}'

    def __eq__(self, other):
        return self.c1 == other.c1 and self.m1 == other.m1 and self.c2 == other.c2 and self.m2 == other.c2 and self.pb == other.pb and self.visited == other.visited


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

    tranzition = Transition(0, 0)

    if State.pb == 1:
        cannibals = State.c1
        missionaires = State.m1
    else:
        cannibals = State.c2
        missionaires = State.m2

    if cannibals >= cb:
        cr = random.randint(0, cb)
        if cr == cb:
            tranzition.c = cr
            tranzition.m = cb-cr
            return tranzition
        elif cr == 0:
            if missionaires > cb:
                tranzition.c = 0
                tranzition.m = cb-cr
                return tranzition
            if missionaires >= 1 and missionaires <= cb:
                tranzition.c = 0
                tranzition.m = missionaires
                return tranzition
        else:
            tranzition.c = cr
            if missionaires >= cb-cr:
                tranzition.m = cb - cr
                return tranzition
            else:
                tranzition.m = missionaires

    if cannibals < cb and cannibals > 0:
        cr = random.randint(0, cannibals)
        if cr == 0:
            if missionaires >= cb:
                tranzition.c = 0
                tranzition.m = cb-cr
                return tranzition
            if missionaires >= 1 and missionaires <= cb:
                tranzition.c = 0
                tranzition.m = missionaires
                return tranzition
        else:
            tranzition.c = cr
            if missionaires >= cb-cr:
                tranzition.m = cb - cr
                return tranzition
            else:
                tranzition.m = missionaires

    if cannibals == 0:
        if missionaires <= cb and missionaires > 0:
            cr = random.randint(1, missionaires)
            tranzition.c = 0
            tranzition.m = cr
            return tranzition
        if missionaires > cb:
            cr = random.randint(1, cb)
            tranzition.c = 0
            tranzition.m = cr
            return tranzition


def randomStrategy():
    for i in range(randomStrategyIterations):
        currentState = getInitialState()
        for j in range(noOfTransitionsWithoutSuccess):
            tran = getRandomTransition(currentState)

            if isTransitionValid(tran) == 1:
                currentState = makeTransition(currentState, tran)

            elif currentState.isFinal() == True:
                print("Rezolvat: ", currentState.c1, currentState.m1,
                      currentState.c2, currentState.m2)
                break
        print("Moment", i, ":", currentState.c1,
              currentState.m1, currentState.c2, currentState.m2)

    if currentState.isFinal() == False:
        print("Nu s-a gasit nicio rezolvare !")


def backtrackingStrategy(state, transitionsDone=[], done=[False]):
    global states

    state.visited = True

    if state.isFinal():
        print(f'Reached a final state: {state}')
        done[0] = True
        return transitionsDone
    if done[0] == True:
        return transitionsDone

    for newState in states:
        if newState.visited == True:
            continue
        transition = buildTransitionBetweenStates(state, newState)
        if isTransitionValid(transition):
            transitionsDone.append(transition)
            backtrackingStrategy(newState, transitionsDone, done)
            if (done[0] == True):
                return transitionsDone
            transitionsDone = transitionsDone[:-1]
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


def main():
    global states
    # randomStrategy()

    states = buildPossibleStates()
    initialState = ([state for state in states if state.c1 ==
                     c and state.m1 == m and state.pb == 1])[0]
    print(f'Initial state: {initialState}')
    transitionsDone = backtrackingStrategy(initialState)
    if transitionsDone is not None:
        for transition in transitionsDone:
            print(transition)


main()
