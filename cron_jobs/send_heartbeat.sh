#!/usr/bin/env bash
set -euo pipefail
# turn on debugging—each command will be echoed into heartbeat.log
export PS4='+ $(date "+%Y-%m-%dT%H:%M:%S")\011 '

# 1) cd into the collector dir
cd "/home/jana/Documents/CollectorDiscord/knowledgecollector" || exit 1

# 2) load .env if it exists
if [ -f ".env" ]; then
  # shellcheck disable=SC1091
  source .env
fi

# 3) build payload
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
PAYLOAD="{\"content\":\"⏱ Cron heartbeat at ${TIMESTAMP}\"}"

# 4) call curl by absolute path
#    adjust `/usr/bin/curl` if your system's curl lives elsewhere
/usr/bin/curl -X POST \
  -H "Content-Type: application/json" \
  -d "${PAYLOAD}" \
  "${DISCORD_WEBHOOK_URL}"
