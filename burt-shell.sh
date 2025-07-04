#!/data/data/com.termux/files/usr/bin/bash

# Burt's Shell – connects natural prompts to real-world powers

while true; do
  echo -n "[Caster >>] "
  read input

  if [[ $input == remember:* ]]; then
    item="${input#remember: }"
    echo "\"$item\"" >> ~/burt/memory.json
    echo "🧠 Remembered: $item"

  elif [[ $input == recall:* ]]; then
    grep -i "${input#recall: }" ~/burt/memory.json || echo "🤔 Nothing found."

  elif [[ $input == watch* ]]; then
    folder="${input#watch folder: }"
    echo "👁️ Watching $folder for changes..."
    inotifywait -m "$folder" &

  elif [[ $input == status:* ]]; then
    termux-battery-status
    termux-telephony-deviceinfo
    termux-sensor -l

  elif [[ $input == scan:* ]]; then
    echo "🧠 Initiating full system scan..."
    bash ~/burt/burt-powers.sh

  elif [[ $input == quit ]]; then
    echo "👋 Exiting Burt Shell..."
    break

  else
    echo "⚠️ Unknown command. Try: remember, recall, watch folder, status, scan, quit"
  fi
done
