import time
import subprocess as sp
import json

PATH  = 'localhost:8081/matches/'

class Board:
    def __init__(self, data):
        self.points = data['points']
        self.tiled  = data['tiled']

        self.agents = [[0 for x in range(data['width'])] for y in range(data['height'])]
        for team in data['teams']:
            for agent in team['agents']:
                self.agents[agent['y'] - 1][agent['x'] - 1] = agent['agentID']

def evaluate(board):
    

def main():
    team_ID  = input('Team ID<< ')
    match_ID = input('Match ID<< ')
    token    = input('Token<< ')

    while True:
        time.sleep(1)
        data = json.loads(sp.check_output([
            'curl',
            '-H',
            'Authorization: ' + token,
            'http://' + PATH + match_ID
        ]).decode())
        
        board = Board(data)
        print(board.agents)
        print(evaluate(board))

if __name__ == '__main__':
    main()
