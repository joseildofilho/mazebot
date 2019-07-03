from random import choice, random

def create_policy_s(maze):
    return {state:choice(maze._actions[state]) for state in maze._actions}

def create_value_funtion(maze):
    V = {}
    for state in maze.all_states():
        if maze.is_terminal(state):
            V.update({state:0})
        else:
            V.update({state:0})
    return V
