import time
import subprocess as sp
import json
from copy import copy
from random import randint

PATH  = 'localhost:8081/matches/'

class Board: 
    def __init__(self, data):
        self.points = data['points']
        self.tiled  = data['tiled']

        self.height = len(self.points)
        self.width  = len(self.points[0])

        self.agents = [
            [
                0 for x in range(data['width'])
            ] for y in range(data['height'])
        ]
        for team in data['teams']:
            for agent in team['agents']:
                self.agents[agent['y'] - 1][agent['x'] - 1] = agent['agentID']

    def bfs(self, team_ID): # チームごとに幅優先探索 引数: 探索するチームのID
        score = 0  # 点数初期化
        stack = [] # スタック
        used = [[False for x in range(self.width)] for y in range(self.height)] # 訪問済みか保存するやつ

        for x in range(self.width): # 盤面ループして各マスからbfs
            for y in range(self.height):
                is_enclosed = True   # 囲まれてるかのフラグ
                cnt = 0              # その領域の点数
                stack.append((x, y)) # スタックに追加

                while len(stack) > 0: # スタックになんか入ってる間
                    nowx, nowy = stack.pop() # c++だとtopとってpopだけどpythonは同時にできちゃう

                    if used[nowy][nowx] is False: # 訪問済みでなければ
                        used[nowy][nowx] = True

                        if self.tiled[nowy][nowx] != team_ID: # 自チームのタイルが無ければ
                            cnt += abs(self.points[nowy][nowx]) # スコア加算

                            for dx, dy in zip([0, 1, 0, -1], [-1, 0, 1, 0]): # 四方向探索 zipは引数の配列から値を一つずつ持ってきます
                                newx, newy = nowx + dx, nowy + dy # nowとnewわかりづらい すまん
                                if newx < 0 or newx >= self.width or newy < 0 or newy >= self.height:
                                    is_enclosed = False # 盤面端に到達したら囲まれてないのでフラグをFalseに
                                else:
                                    stack.append((newx, newy)) # スタックに追加

                if is_enclosed: # 領域を全部探索して囲まれていることがわかったらスコア加算
                    score += cnt

        return score

class Agent:
    def __init__(self, team_ID, agent_ID, x, y):
        self.team_ID  = team_ID
        self.agent_ID = agent_ID

        self.x = x
        self.y = y

    def get_type(self, tiled):
        return 'move' if tiled[self.y + self.dy][self.x + self.dx] in (0, self.team_ID) else 'remove'

    def set_action(self, action):
        self.dx = action % 3 - 1
        action //= 3
        self.dy = action % 3 - 1

    def action(self, tiled):
        return {
            'agentID': self.agent_ID,
            'dx': self.dx,
            'dy': self.dy,
            'type': self.get_type(tiled)
        }
    
class MinMax:
    def __init__(self, data, our_ID):
        self.height = data['height']
        self.width  = data['width']
        
        self.points = data['points']
        self.tiled  = data['tiled']

        self.our_agents = []
        self.opp_agents = []

        for team in data['teams']:
            for agent in team['agents']:
                agent_object = Agent(
                    team['teamID'],
                    agent['agentID'],
                    agent['x'],
                    agent['y']
                )

                if team['teamID'] == our_ID:
                    self.our_agents.append(agent_object)
                else:
                    self.opp_agents.append(agent_object)

    def eval(self, our_agents, opp_agents):
        return randint(-100, 100)

    def search(self, our_agents, opp_agents, depth):
        our_agents_tmp = copy(our_agents)
        opp_agents_tmp = copy(opp_agents)

        if depth == 0:
            return self.eval(our_agents, opp_agents), 0

        best_score = -float('inf')
        best = 0

        for next_action in range(9 ** (2 * len(our_agents))):
            tmp = next_action
            for agent in our_agents_tmp:
                agent.set_action(tmp % 9)
                tmp //= 9
            for agent in opp_agents_tmp:
                agent.set_action(tmp % 9)
                tmp //= 9
            
            score = self.search(our_agents_tmp, opp_agents_tmp, depth - 1)[0]

            if best_score < score:
                best_score = score
                best = next_action

        return best_score, best            

    def get_action(self):

        # {
        #   "actions": [
        #       {
        #           "agentID": 2,
        #           "dx": 1, 
        #           "dy": 1,
        #           "type": "move"
        #       },
        #       {
        #           "agentID": 3,
        #           "dx": 1,
        #           "dy": 1,
        #           "type": "move"
        #       }
        #   ]
        # }

        action = {'actions': []}

        best = self.search(self.our_agents, self.opp_agents, 1)[1]

        for agent in self.our_agents:
            agent.set_action(best % 9)
            action['actions'].append(agent.action(self.tiled))
            best //= 9

        return json.dumps(action)
