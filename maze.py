import requests

api_url = 'https://api.noopschallenge.com/mazebot/random?maxSize=10'

class Maze:
    def __init__(self):
        '''
            Class that implements the maze, it's very similar to the Gridword game.
        '''
        # Game config
        result         = requests.get(api_url).json()
        self.start     = tuple(result['startingPosition'])
        self.end       = tuple(result['endingPosition'])
        self.maze_path = result['mazePath']
        self.size_x    = len(result['map'])
        self.size_y    = len(result['map'][0])

        # Game variables
        self.x = 0
        self.y = 0
        self.restart()

        # Meta-game variables

        self._default_return = 10

        self.wall = 'X'

        # Game Creation

        self._actions = {}
        self._rewards = {}
        self._process_map(result['map'])

        # debug stuff
        self.__map = result['map']

    def current_state(self):
        '''
            Returns the current state
        '''
        return (self.x, self.y)

    def restart(self):
        '''
            Restart the player position to the start
        '''
        self.x = self.start[0]
        self.y = self.start[1]

    def set_state(self, state):
        '''
            Set a state to the enviroment
        '''
        self.x = state[0]
        self.y = state[1]

    def all_states(self):
        '''
            Return a set of all states, including the terminals
        '''
        return set(list(self._actions.keys()) + list(self._actions.keys()))
    
    def is_terminal(self, state):
        '''
            Tests if a state is terminal
        '''
        return state in self._rewards
    
    def move(self, action):
        '''
            Make a move and changes the envoriment, and returns the value of that
            state
        '''
        if self.is_possible_move(action) and not self.is_game_over():
            if   action == 'N':
                self.y -= 1
            elif action == 'S':
                self.y += 1
            elif action == 'W':
                self.x -= 1
            elif action == 'E':
                self.x += 1
        return self._rewards.get(self.current_state(), 0)

    def is_possible_move(self, move):
        '''
            Tests if is possible to make such a move
        '''
        return move in self._actions[self.current_state()]

    def is_game_over(self):
        '''
            Tests if the game is over
        '''
        return (self.x, self.y) == self.end

    def _process_map(self, maze):
        '''
            Creates the actions and the returns for the game
        '''
        self._create_rewards()
        self._create_actions(maze)

    def _create_rewards(self):
        self._rewards = {
                self.end   : self._default_return
                }

    def _create_actions(self, maze):
        for i, line in enumerate(maze):
            for j, cell in enumerate(line):
                if cell != self.wall:
                    possible_actions = ['N', 'E', 'S', 'W']
                    actions = []
                    neighbors = self._get_neighborhood(i, j, maze)
                    for possible, n in zip(possible_actions, neighbors):
                        if n and (n != self.wall):
                            actions.append(possible)
                    if actions:
                        self._actions[(j,i)] = actions

    def _get_neighborhood(self, i, j, matrix):
        '''
            Returns only the elements inside a matrix in a list.
            The List will be in this way:
            [N, E, S, W]
            if the position leads to an out of the bound, the list will be like:
            [None, E, S, None]
        '''
        ret = []
        # N
        aux = i - 1
        if aux >= 0 and matrix[aux][j] != self.wall:
            ret.append(matrix[aux][j])
        else:
            ret.append(None)

        # E
        aux = j + 1
        if aux < self.size_x and matrix[i][aux] != self.wall:
            ret.append(matrix[i][aux])
        else:
            ret.append(None)

        # S
        aux = i + 1
        if aux < self.size_y and matrix[aux][j] != self.wall:
            ret.append(matrix[aux][j])
        else:
            ret.append(None)

        # W
        aux = j - 1
        if aux >= 0 and matrix[i][aux] != self.wall:
            ret.append(matrix[i][aux])
        else:
            ret.append(None)

        return ret

if __name__ == '__main__':
    maze = Maze()

    
