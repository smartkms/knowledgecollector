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


def enqueue_message(msg_payload: dict):
    redis_client.rpush(MESSAGE_QUEUE, json.dumps(msg_payload))


def dequeue_message(timeout=5):
    item = redis_client.blpop(MESSAGE_QUEUE, timeout=timeout)
    if not item:
        return None
    return json.loads(item[1])
