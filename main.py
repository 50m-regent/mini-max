import time
import subprocess as sp
import json
from minmax import MinMax

PATH  = 'localhost:8081/matches/'
TOKEN = '16426a3fa4a20eb959718a945ba79b4cb0492798b7ea88f072b8ae6efb02ee8b'

def send(match_id, action):
    sp.run([
        'curl',
        '-H',
        'Authorization: ' + TOKEN,
        '-H',
        'Content-Type: application/json',
        '-X',
        'POST',
        'http://' + PATH + match_id + '/action',
        '-d',
        action
    ])

def main():
    team_ID  = int(input('Team ID<< '))
    match_ID = input('Match ID<< ')

    while True:
        data = json.loads(sp.check_output([
            'curl',
            '-H',
            'Authorization: ' + TOKEN,
            'http://' + PATH + match_ID
        ]).decode())
        # print(data)

        minmax = MinMax(data, team_ID)
        send(match_ID, minmax.get_action())

        time.sleep(3)

if __name__ == '__main__':
    main()