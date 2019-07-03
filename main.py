from maze import Maze
from utils import *
from numpy import Infinity

if __name__ == '__main__':
    γ = 0.9

    maze = Maze()

    π = create_policy_s(maze)

    # Value Iteration

    Θ = 0.00000000001
    V = create_value_funtion(maze)

    iterations_number = 0

    while True:
        iterations_number += 1
        Δ = 0  
        for state in maze.all_states():
            if not maze.is_terminal(state):
                v = V[state]
    
                actions = maze._actions[state]
                p = 1 / len(actions)
    
                for action in actions:
                    maze.set_state(state)
                    r = maze.move(action)
                    calculation = p * (r + γ * V[maze.current_state()])
                    if V[state] < calculation:
                        V[state] = calculation 
                    Δ = max(Δ, abs(v - V[state]))
        if Δ < Θ:
            print("Δ:",Δ)
            print("Number of iterations:", iterations_number)
            break

    for state in maze.all_states():
        maze.set_state(state)
        if not maze.is_game_over():

            actions = maze._actions[state]
            p = 1 / len(actions)

            max_v = -Infinity
            max_a = ''

            for action in actions:
                maze.set_state(state)
                r = maze.move(action)
                calculation = p * (r + γ * V[maze.current_state()])
                if max_v < calculation:
                    max_v = calculation
                    max_a = action
            π[state] = max_a

    for i in range(maze.size_x):
        line = ''
        for j in range(maze.size_y):
            if (j, i) == maze.start:
                print(' \033[91m'+ π[(j,i)], end='')
            elif (j, i) == maze.end:
                print(' \033[94m#', end='')
            else:
                if π.get((j, i), 'X') == 'X':
                    print(' \033[92mX', end='')
                else:
                    print(' \033[95m' + π[(j,i)], end='')
        print()
