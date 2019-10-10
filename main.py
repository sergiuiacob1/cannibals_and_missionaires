# TODO validate transitions

c = 3
m = 3
cb = 2


class State:
    def __init__(self, c1, m1, c2, m2, pb):
        self.c1 = c1
        self.m1 = m1
        self.c2 = c2
        self.m2 = m2
        self.pb = pb
        self.visited = False


class Transition:
    def __init__(self, c, m):
        self.c = c
        self.m = m


def getInitialState():
    return State(c, m, 0, 0, 1)


def isTransitionValid(transition):
    return transition.c <= transition.m


def makeTransition(state, transition):
    if state.pb == 1:
        return State(state.c1 - transition.c, state.m1 - transition.m, state.c2 + transition.c, state.m2 + transition.m, 2)
    return State(state.c1 + transition.c, state.m1 + transition.m, state.c2 - transition.c, state.m2 - transition.m, 1)
