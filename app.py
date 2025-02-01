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
                    data={"subject": player["fullName"], "det_prob_threshold": 0.5},
                )
                # remove the local file
                os.remove(f"{player['id']}.png")


get_players_list()


def get_twhl_data():
    response = requests.get(
        "https://lscluster.hockeytech.com/feed/index.php?feed=statviewfeed&view=players&season=5&team=all&position=skaters&rookies=0&statsType=standard&rosterstatus=undefined&site_id=0&first=0&limit=300&sort=points&league_id=1&lang=en&division=-1&conference=-1&key=446521baf8c38984&client_code=pwhl&league_id=1&callback=angular.callbacks._5"
    )

    res = response.text.replace("angular.callbacks._5(", "")
    res = res[:-1]
    all_players = json.loads(res)
    # for all players download the image and send it to the recognition service from this url https://assets.leaguestat.com/pwhl/120x160/53.jpg
    for player in all_players[0]["sections"][0]["data"]:
        print(player["prop"]["name"]["seoName"])
        response = requests.get(
            f"https://assets.leaguestat.com/pwhl/120x160/{player['prop']['name']['playerLink']}.jpg"
        )
        with open(f"{player['prop']['name']['playerLink']}.jpg", "wb") as f:
            f.write(response.content)
        # send image to the recognition service
        response = requests.post(
            "http://localhost:8000/api/v1/recognition/faces",
            headers={"x-api-key": "701865aa-8119-4ea9-850f-a3581f65292e"},
            files={"file": open(f"{player['prop']['name']['playerLink']}.jpg", "rb")},
            data={
                "subject": player["prop"]["name"]["seoName"],
                "det_prob_threshold": 0.5,
            },
        )
        # remove the local file
        os.remove(f"{player['prop']['name']['playerLink']}.jpg")


get_twhl_data()
