import redis
import json
from shared.config import SETTINGS

redis_client = redis.Redis(host=SETTINGS.REDIS_HOST, port=SETTINGS.REDIS_PORT)

JOB_QUEUE = "job_queue"
MESSAGE_QUEUE = "message_queue"

def enqueue_job(job_payload: dict):
    redis_client.rpush(JOB_QUEUE, json.dumps(job_payload))


def dequeue_job(timeout=5):
    item = redis_client.blpop(JOB_QUEUE, timeout=timeout)
    if not item:
        return None
    return json.loads(item[1])


def enqueue_message_ids(message_ids: list[str]):
    """
    Push a list of message IDs onto the message queue.
    """
    # Store as a JSON array, e.g. ['id1', 'id2']
    payload = json.dumps(message_ids)
    redis_client.rpush(MESSAGE_QUEUE, payload)

def dequeue_message_ids(timeout: int = 5) -> list[str] | None:
    """
    Block for up to `timeout` seconds and return the list of message IDs, or None if empty.
    """
    item = redis_client.blpop(MESSAGE_QUEUE, timeout=timeout)
    if not item:
        return None
    # item is (queue_name, payload_bytes)
    _, payload_bytes = item
    # Parse JSON array into Python list of strings
    message_ids = json.loads(payload_bytes)
    return message_ids
