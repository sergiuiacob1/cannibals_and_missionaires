buildPossibleStates()
    initialState = ([state for state in states if state.c1 ==
                     c and state.m1 == m and state.pb == 1])[0]
    print(f'Initial state: {initialState}')
    transitionsDone = backtrackingStrategy(initialState)
    if transitionsDone is not None:
        for transition in transitionsDone:
            print(transition)