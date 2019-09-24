import time
import subprocess as sp
import json

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

def evaluate(board, our_ID, opp_ID):
    points = {
        0: {
            'tile': 0
        },
        our_ID: {
            'area': board.bfs(our_ID),
            'tile': 0
        },
        opp_ID: {
            'area': board.bfs(opp_ID),
            'tile': 0
        }
    }

    for y, row in enumerate(board.tiled):
        for x, cell in enumerate(row):
            points[cell]['tile'] += board.points[y][x]

    return sum(points[our_ID].values()) - sum(points[opp_ID].values())

def main():
    our_ID   = input('Team ID<< ')
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

        for team in data['teams']:
            if team['teamID'] != our_ID:
                opp_ID = team['teamID']

        board = Board(data)
        print(evaluate(board, our_ID, opp_ID))

if __name__ == '__main__':
    data = {
        "width": 6,
        "height": 4,
        "points": [
            [
            2, -4, 0, 0, -4, 2
            ],
            [
            5, -1, 1, 1, -1, 5
            ],
            [
            5, -1, 1, 1, -1, 5
            ],
            [
            2, -4, 0, 0, -4, 2
            ]
        ],
        "startedAtUnixTime": 0,
        "turn": 0,
        "tiled": [
            [
            0, 0, 6, 0, 0, 0
            ],
            [
            5, 6, 0, 6, 0, 0
            ],
            [
            0, 0, 6, 0, 0, 6
            ],
            [
            0, 0, 0, 5, 0, 0
            ]
        ],
        "teams": [
            {
            "teamID": 5,
            "agents": [
                {
                "agentID": 9,
                "x": 6,
                "y": 4
                },
                {
                "agentID": 10,
                "x": 1,
                "y": 1
                }
            ],
            "tilePoint": 5,
            "areaPoint": 0
            },
            {
            "teamID": 6,
            "agents": [
                {
                "agentID": 11,
                "x": 3,
                "y": 1
                },
                {
                "agentID": 12,
                "x": 6,
                "y": 3
                }
            ],
            "tilePoint": 5,
            "areaPoint": 0
            }
        ],
        "actions": []
    }

    board = Board(data)

    print(evaluate(board, 5, 6))
