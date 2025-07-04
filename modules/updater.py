import os
import requests
import json

def check_for_updates(current_version):
    # Simulate pulling version info (replace with Git or server call later)
    remote_version = "0.2"
    if remote_version != current_version:
        print(f"New version available: {remote_version}")
        return remote_version
    print("Burt is up to date.")
    return None

def apply_update():
    print("Pretending to apply update... (TODO: git pull or overwrite files)")

def self_update():
    config_path = "config.json"
    with open(config_path, "r") as f:
        config = json.load(f)

    if config.get("auto_update", False):
        new_version = check_for_updates(config["version"])
        if new_version:
            apply_update()
            config["version"] = new_version
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
