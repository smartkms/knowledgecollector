from redis import Redis
from rq import Queue
from parser import process_message

redis_conn = Redis(host="localhost", port=6379)
q = Queue(connection=redis_conn)

nek_msg = {
    "platform": "teams",
    "channel": "#general",
    "user": "u123",
    "text": "a smo ze zacel kej s projektom?",
    "timestamp": "2025-04-08T10:42:00Z",
}

job = q.enqueue(process_message, nek_msg)
print(f"Enqeueued job{job.id}")
