#include<map>
#include<string>

#define PATH  "localhost:8081/matches/"

class Agent{
public:
    int team_ID, agent_ID, dx, dy;

    std::map<std::string, std::string> action(int **tiled){
        std::map<std::string, std::string> action;
        action["agentID"] = std::to_string(this->agent_ID);
        action["dx"]      = std::to_string(this->dx);
        action["dy"]      = std::to_string(this->dy);
        action["type"]    = get_type(tiled);

        return action;
    }

private:
    int x, y;

    Agent(int team_ID, int agent_ID, int x, int y){
        this->team_ID  = team_ID;
        this->agent_ID = agent_ID;

        this->x = x;
        this->y = y;
    }

    std::string get_type(int **tiled){
        return tiled[this->y + this->dy][this->x + this->dx] == 0 || tiled[this->y + this->dy][this->x + this->dx] == this->team_ID ? "move" : "remove";
    };

    void set_action(int action){
        this->dx = action % 3 - 1;
        this->dy = action / 3 % 3 - 1;
    }
};

class MatchData{

};

class MinMax{
public:
    MinMax(MatchData data, int our_ID){
        
    }
};
    
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
