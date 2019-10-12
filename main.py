# TODO validate transition
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


def getRandomTransition(State):

    tranzition = Transition(0,0)

    if State.pb == 1:
        cannibals = State.c1
        missionaires = State.m1
    else:
        cannibals = State.c2
        missionaires = State.m2

    if cannibals >= cb:
        cr =  random.randint(0,cb)
        if cr == cb:
            tranzition.c = cr
            tranzition.m = cb-cr
            return tranzition
        elif cr == 0:
            if missionaires > cb:
                tranzition.c = 0
                tranzition.m = cb-cr
                return tranzition
            if missionaires >=1 and missionaires <= cb:
                tranzition.c =0
                tranzition.m = missionaires
                return tranzition
        else:
            tranzition.c = cr
            if missionaires >= cb-cr:
                tranzition.m = cb -cr
                return tranzition
            else:
                tranzition.m = missionaires

    if cannibals < cb and cannibals > 0:
        cr =  random.randint(0,cannibals)
        if cr == 0:
            if missionaires >= cb:
                tranzition.c = 0
                tranzition.m = cb-cr
                return tranzition
            if missionaires >=1 and missionaires <= cb:
                tranzition.c =0
                tranzition.m = missionaires
                return tranzition
        else:
            tranzition.c = cr
            if missionaires >= cb-cr:
                tranzition.m = cb -cr
                return tranzition
            else:
                tranzition.m = missionaires
    
    if cannibals == 0:
        if missionaires <= cb and missionaires >0:
            cr = random.randint(1,missionaires)
            tranzition.c= 0
            tranzition.m=cr
            return tranzition
        if missionaires > cb:
            cr = random.randint(1,cb)
            tranzition.c= 0
            tranzition.m=cr
            return tranzition


def randomStrategy():
    for i in range(randomStrategyIterations):
        currentState = getInitialState()
        for j in range(noOfTransitionsWithoutSuccess):
            tran = getRandomTransition(currentState)

            if isTransitionValid(tran) == 1:
                currentState = makeTransition(currentState,tran)
            
            elif currentState.isFinal() == True:
                print ("Rezolvat: ",currentState.c1,currentState.m1,currentState.c2, currentState.m2)
                break
        print ("Moment ",i,": ",currentState.c1,currentState.m1,currentState.c2, currentState.m2)

    
    if currentState.isFinal() == False:
        print("Nu s-a gasit nicio rezolvare !")

def main():
    randomStrategy()

main()
