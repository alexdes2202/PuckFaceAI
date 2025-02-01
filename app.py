import requests
import json
import os


def get_data():
    response = requests.get(
        "https://api.nhle.com/stats/rest/en/skater/summary?cayenneExp=seasonId=20242025"
    )
    return json.loads(response.text)


def get_players_list():

    teams_data = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/teams"
    response = requests.get(teams_data)
    teams = json.loads(response.text)
    # print(teams["sports"][0]["leagues"][0]["teams"][0]["team"]["id"])
    for team in teams["sports"][0]["leagues"][0]["teams"]:
        team_id = team["team"]["id"]
        team_name = team["team"]["displayName"]
        print(f"Team: {team_name}")
        response = requests.get(
            f"https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/teams/{team_id}/roster"
        )
        teamInfo = json.loads(response.text)
        print(teamInfo["athletes"])
        for players in teamInfo["athletes"]:
            for player in players["items"]:
                print(f"Player: {player['id']}")
                # get player image and save it to the local file
                response = requests.get(
                    f"https://a.espncdn.com/combiner/i?img=/i/headshots/nhl/players/full/{player['id']}.png&w=200&h=150&cb=1"
                )
                with open(f"{player['id']}.png", "wb") as f:
                    f.write(response.content)
                # send image to the recognition service
                response = requests.post(
                    "http://localhost:8000/api/v1/recognition/faces",
                    headers={"x-api-key": "701865aa-8119-4ea9-850f-a3581f65292e"},
                    files={"file": open(f"{player['id']}.png", "rb")},
                    data={"subject": player["displayName"], "det_prob_threshold": 0.5},
                )
                # remove the local file
                os.remove(f"{player['id']}.png")


get_players_list()
