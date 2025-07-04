import sys
import os
import json
import re
import subprocess
from pathlib import Path

MEMORY_FILE = os.path.expanduser("~/burt/burt_memory.json")
COMMANDS_FILE = os.path.expanduser("~/burt/commands.py")

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def remember(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)
    print(f"🧠 Remembered {key}: {value}")

def recall(key):
    memory = load_memory()
    print(memory.get(key, "I don't remember that yet."))

def forget(key):
    memory = load_memory()
    if key in memory:
        del memory[key]
        save_memory(memory)
        print(f"🗑️ Forgot {key}.")
    else:
        print("I didn't know that anyway.")

def ensure_commands_file():
    if not os.path.exists(COMMANDS_FILE):
        with open(COMMANDS_FILE, "w") as f:
            f.write("# Burt's learned commands live here!\n")

def learn(command_name, shell_command):
    ensure_commands_file()
    with open(COMMANDS_FILE, "a") as f:
        f.write(f"\ndef {command_name}():\n    os.system('''{shell_command}''')\n")
    print(f"🛠️ Learned a new command: '{command_name}' → {shell_command}")

def run_learned_command(command_name):
    ensure_commands_file()
    import importlib.util
    spec = importlib.util.spec_from_file_location("commands", COMMANDS_FILE)
    commands = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(commands)
    if hasattr(commands, command_name):
        getattr(commands, command_name)()
    else:
        print("I haven't learned the command '{}' yet.".format(command_name))

def upgrade_self(code_snippet):
    with open(__file__, "a") as f:
        f.write(f"\n# --- self-upgrade ---\n{code_snippet}\n")
    print("🔧 I have upgraded myself!")

def parse_nl_to_code(user_input):
    patterns = [
        (r"(take|capture|get) (a )?photo|open (the )?camera", "take_photo", "termux-camera-photo /sdcard/burt_photo_$(date +%s).jpg"),
        (r"battery status|check battery", "battery_status", "termux-battery-status"),
        (r"turn on wifi", "wifi_on", "termux-wifi-enable true"),
        (r"turn off wifi", "wifi_off", "termux-wifi-enable false"),
        (r"list files|show files", "list_files", "ls"),
        (r"show (my )?ip", "show_ip", "curl ifconfig.me"),
    ]
    for pat, name, cmd in patterns:
        if re.search(pat, user_input, re.IGNORECASE):
            return name, cmd
    return None, None

def fallback_llm_code(user_input):
    return "def custom_action():\n    print('This is a stub for: {}')\n".format(user_input)

def show_help():
    print("""
🤖 I am Burt. You can use these commands:

remember KEY VALUE      - Store a fact in memory
recall KEY              - Recall a fact from memory
forget KEY              - Forget a memory
learn COMMAND HOW_TO    - Teach me a new command (natural language)
run COMMAND             - Execute a learned command
upgrade CODE            - Add Python code to myself (be careful!)
help                    - Show this help message
exit                    - Quit
Or just talk to me!
""")

def chat_with_llama(user_input):
    llama_path = os.path.expanduser("~/burt/llama.cpp/build/bin/llama-cli")
    model_path = os.path.expanduser("~/burt/models/tinyllama.gguf")
    try:
        result = subprocess.check_output([llama_path, "-m", model_path, "-p", user_input], text=True)
        print(result.strip())
    except Exception as e:
        print("🤖 (LLM error):", e)

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    user_input = " ".join(sys.argv[1:]).strip()

    if user_input.lower() == "help":
        show_help()
        return

    if user_input.startswith("remember "):
        try:
            _, key, value = user_input.split(" ", 2)
            remember(key, value)
        except Exception:
            print("Usage: remember KEY VALUE")
        return

    if user_input.startswith("recall "):
        _, key = user_input.split(" ", 1)
        recall(key)
        return

    if user_input.startswith("forget "):
        _, key = user_input.split(" ", 1)
        forget(key)
        return

    if user_input.startswith("learn "):
        nl = user_input[6:]
        cname, scmd = parse_nl_to_code(nl)
        if cname:
            learn(cname, scmd)
        else:
            code = fallback_llm_code(nl)
            ensure_commands_file()
            with open(COMMANDS_FILE, "a") as f:
                f.write(f"\n{code}\n")
            print(f"🤔 I tried to learn from LLM/stub as '{nl}'.")
        return

    if user_input.startswith("run "):
        _, cname = user_input.split(" ", 1)
        run_learned_command(cname)
        return

    if user_input.startswith("upgrade "):
        code = user_input[8:]
        upgrade_self(code)
        return

    # If none of the commands matched, just chat!
    chat_with_llama(user_input)

if __name__ == "__main__":
    main()
