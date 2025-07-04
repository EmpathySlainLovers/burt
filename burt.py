kfrom memory.memory import remember, recall
from modules.updater import self_update

print("🔁 Checking for updates...")
self_update()

remember("mission", "take over the phone")
print("Burt's mission is:", recall("mission"))
