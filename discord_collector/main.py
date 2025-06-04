import asyncio
import os
import json
from datetime import datetime, timezone
from .discord_api import fetch_messages
from .config import CHANNEL_ID

async def main(limit: int = 50):
    state_file = "last_message_id.txt"
    after_id = None

    # ─── 1. If we've run before, load last seen ID ───
    if os.path.exists(state_file):
        with open(state_file, "r", encoding="utf-8") as f:
            val = f.read().strip()
            if val:
                after_id = val

    # ─── 2. Page through all new messages ───
    all_new = []
    cursor = after_id
    while True:
        batch = await fetch_messages(limit=limit, after_id=cursor)
        if not batch:
            break
        all_new.extend(batch)
        # advance cursor to the oldest message in this batch
        cursor = batch[-1]["id"]
        # if fewer than limit were returned, we're done
        if len(batch) < limit:
            break

    # ─── 3. Nothing new? ───
    if not all_new:
        print("No new messages.")
        return

    # ─── 4. Persist the newest ID for next run ───
    newest_id = str(max(int(m["id"]) for m in all_new))
    with open(state_file, "w", encoding="utf-8") as f:
        f.write(newest_id)

    # ─── 5. Normalize messages ───
    normalized = []
    for m in all_new:
        normalized.append({
            "createdDateTime": m["timestamp"],      # ISO timestamp
            "user": {
                "id": m["author"]["id"],
                "displayName": m["author"]["username"]
            },
            "body": m.get("content", "")
        })

    # ─── 6. Write to JSON ───
    now = datetime.now(timezone.utc)
    epoch_ms = str(int(now.timestamp() * 1000))
    ts_iso = now.isoformat(timespec="milliseconds")

    payload = {
        "typefield": "messages",
        "platform":  "discord",
        "id":         epoch_ms,
        "timestamp":  ts_iso,
        "content": {
            "channelId": CHANNEL_ID,
            "messages":  normalized
        }
    }

    filename = f"{epoch_ms}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(normalized)} messages to {filename}")

if __name__ == "__main__":
    import sys
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    asyncio.run(main(limit=lim))
