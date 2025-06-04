#!/usr/bin/env bash
set -euo pipefail

# 1) Change into your project directory (one quoted arg only!)
cd "/home/jana/Documents/CollectorDiscord/knowledgecollector" || exit 1

# 2) Load environment variables, if you have an .env file
if [ -f ".env" ]; then
  source .env
fi

# 3) Run the collector (no additional args means full paging loop)
#    Make sure `which uv` prints /home/jana/.local/bin/uv (or adjust as needed)
"/home/jana/.local/bin/uv" run -m src.discord.main
