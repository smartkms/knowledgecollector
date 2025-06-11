import time
from datetime import datetime
from shared.db import subs_coll  # direct access to subscriptions collection
from shared.queue import enqueue_job

LIMIT = 100


def run_scheduler():
    while True:
        now = datetime.utcnow()
        # Find all subscriptions where next_run ≤ now and active = true
        due_subs = subs_coll.find({"active": True, "next_run": {"$lte": now}}).limit(
            LIMIT
        )

        for sub in due_subs:
            job = {
                "subscription_id": str(sub["_id"]),
                "platform": sub["platform"],
                "server_id": sub["server_id"],
                "channel_id": sub.get("channel_id"),
                "requested_by": sub["user_id"],
                "timestamp": now.isoformat(),
            }
            enqueue_job(job)

            # Update last_run and next_run
            last_run = now
            # parse frequency, compute next_run
            import isodate

            freq_delta = isodate.parse_duration(sub["frequency"])
            next_run = last_run + freq_delta
            subs_coll.update_one(
                {"_id": sub["_id"]},
                {"$set": {"last_run": last_run, "next_run": next_run}},
            )

        time.sleep(60)  # sleep 1 minute


if __name__ == "__main__":
    run_scheduler()
