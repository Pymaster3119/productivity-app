import requests
import configparser

config = configparser.ConfigParser()
config.read('appsetings.cfg')

TOKEN = config.get('Clickup', 'token', fallback=None)
headers = {"Authorization": TOKEN, "Content-Type": "application/json"}

# Step 1: Get teams
team_resp = requests.get("https://api.clickup.com/api/v2/team", headers=headers)
team_resp.raise_for_status()
teams = team_resp.json()["teams"]

for team in teams:
    team_id = team["id"]
    print(f"Team: {team['name']} (ID: {team_id})")

    # Step 2: Get spaces in the team
    spaces_resp = requests.get(f"https://api.clickup.com/api/v2/team/{team_id}/space", headers=headers)
    spaces_resp.raise_for_status()
    spaces = spaces_resp.json()["spaces"]

    for space in spaces:
        space_id = space["id"]
        print(f"  Space: {space['name']} (ID: {space_id})")

        # Step 3: Get lists in the space
        lists_resp = requests.get(f"https://api.clickup.com/api/v2/space/{space_id}/list", headers=headers)
        lists_resp.raise_for_status()
        lists = lists_resp.json()["lists"]

        for lst in lists:
            print(f"    List: {lst['name']} (ID: {lst['id']})")
            # Step 4: Get tasks in the list
            tasks_resp = requests.get(f"https://api.clickup.com/api/v2/list/{lst['id']}/task", headers=headers)
            tasks_resp.raise_for_status()
            tasks = tasks_resp.json().get("tasks", [])

            for task in tasks:
                print(f"      Task: {task['name']} (ID: {task['id']})")