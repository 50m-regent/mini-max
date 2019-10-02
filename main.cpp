#include<string>
#include<iostream>
#include"json.hpp"

#define PATH "localhost:8081/matches/"
#define TOKEN "16426a3fa4a20eb959718a945ba79b4cb0492798b7ea88f072b8ae6efb02ee8b"

void send(int match_id, std::string action){
    std::string command = "curl -H 'Authorization: 16426a3fa4a20eb959718a945ba79b4cb0492798b7ea88f072b8ae6efb02ee8b' -H Content-Type: application/json -X POST 'http://localhost:8081/matches/" + std::to_string(match_id) + "/action' -d " + action;
    system(command.c_str());
}

int main(){
    int team_ID;
    std::string match_ID;
    std::cin>>team_ID>>match_ID;

    while(true){
        auto data = json11::Json::parse(R"({"test": 11})");
    }

    return 0;
}

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