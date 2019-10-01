#include<iostream>
#include<stack>
using namespace std;

int team_ID;
int match_ID;
int dx[0, 1, 0, -1], dy[-1, 0, 1, 0];


struct Board {

	int points = data['points'];
	int tiled  = data['tiled'];
	int height = points.size();
	int width  = points[0].size();

	/*
	self.agents = [
		[
			0 for x in range(data['width'])
		] for y in range(data['height'])
	]
		for team in data['teams']:
		for agent in team['agents'] :
			self.agents[agent['y'] - 1][agent['x'] - 1] = agent['agentID']
	*/

	void dfs(self, team_ID) {
		
		int score = 0;
		bool used[100][100] = { false };
		stack<pair<int, int> > sta;

		for (int x = 0; x < width; x++) {
			for (int y = 0; y < height; y++) {
				enclosed = true;
				cnt = 0;
				sta.push(make_pair(x, y));

				while (!sta.empty()) {
					int nowx = sta.top().first;
					int nowy = sta.top().second;
					sta.pop();

					if (!used[nowy][nowx]) {
						used[nowy][nowx] = true;

						if (tiled[nowy][nowx] != team_ID) {
							cnt += abs(points[nowy][nowx]);

							for (int next = 0; next < 4; next++) {
								int newx = nowx + dx[next], newy = nowy + dy[next];

								if (newx < 0 || newx >= width || newy < 0 || newy >= height)
									enclosed = false;
								else
									sta.push(make_pair(newx, newy));
							}
						}
					}
				}
				if (enclosed)score += cnt;
			}
		}
		return score;
	}
};

struct Agent {
	private:
		int team_ID  = team_ID;
		int agent_ID = agent_ID;
		int x = x;
		int y = y;
		/*ˆÓ–¡‚í‚©‚ç‚ñ‚ñ‚ñ‚ñ‚ñ*/
};

struct BeamSerch {
	private:
		int height = data['height'];
		int width  = data['width'];
		int points = data['points'];
		int tiled  = data['tiled'];
		int our_agents = [];
		int opp_agents = [];


		for (int team = 0; team < data['team'].size(); team++) {
			for (int agent = 0; agent < team['agents']; agent++) {

			}
		}


		void eval() {

		}
		
		void search() {

		}
};


int main() {
	
	cin >> team_ID >> match_ID;

	while (1) {
		
	}

}