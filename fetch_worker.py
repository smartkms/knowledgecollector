from shared.queue import dequeue_job
from discord_collector.fetch import fetch_discord
from onedrive_collector.fetch import fetch_onedrive
from shared.db import subs_coll


def run_fetch_worker():
    while True:
        job = dequeue_job(timeout=10)
        if not job:
            continue  # no job, loop again

        sub_id = job["subscription_id"]
        sub = subs_coll.find_one({"_id": sub_id, "active": True})
        if not sub:
            continue  # subscription was deleted/disabled

        platform = job["platform"]
        if platform == "discord":
            fetch_discord(
                server_id=sub["server_id"],
                channel_id=sub["channel_id"],
                subscription_id=sub_id,
                requested_by=sub["user_id"],
            )
        elif platform == "onedrive":
            # Assume `credentials.refresh_token` is stored inside `sub["credentials"]`
            fetch_onedrive(
                folder_id=sub["server_id"],
                subscription_id=sub_id,
                requested_by=sub["user_id"],
                refresh_token=sub["credentials"].get("refresh_token"),
            )
        # else: handle other platforms if added


if __name__ == "__main__":
    run_fetch_worker()
