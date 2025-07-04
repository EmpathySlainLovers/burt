#!/data/data/com.termux/files/usr/bin/bash

cd ~/burt
echo "🤖 Welcome to Burt! Type 'help' for commands, 'exit' to quit."
while true; do
  echo -n "You: "
  read -r line
  if [[ "$line" == "exit" ]]; then
    echo "👋 Bye!"
    break
  fi
  python burt.py "$line"
done
