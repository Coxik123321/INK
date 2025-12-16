import json

with open("security/roles.json") as f:
    ROLES = json.load(f)

def check_access(role, action):
    return action in ROLES.get(role, [])
