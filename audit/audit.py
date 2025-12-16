from datetime import datetime

def log_action(user, action, details=""):
    with open("audit.log", "a", encoding="utf-8") as f:
        f.write(
            f"{datetime.now()} | {user} | {action} | {details}\n"
        )
