#!/usr/bin/env python3
from shared.db import insert_message, get_message
from shared.queue import enqueue_message_ids, dequeue_message_ids, redis_client, MESSAGE_QUEUE

def main():
    # 1) Clear the queue
    redis_client.delete(MESSAGE_QUEUE)
    print("Cleared message queue.")

    # 2) Insert a dummy message into MongoDB
    dummy = {
        "platform": "test",
        "text": "Hello, Shared Utils!",
        "attachments": [],
        "fetched_at": None
    }
    msg_id = insert_message(dummy)
    print("Inserted message with ID:", msg_id)

    # 3) Retrieve it back from the DB
    retrieved = get_message(msg_id)
    print("Retrieved from DB:", retrieved)

    # 4) Enqueue that ID
    enqueue_message_ids([msg_id])
    print("Enqueued message ID list:", [msg_id])

    # 5) Check Redis length
    length = redis_client.llen(MESSAGE_QUEUE)
    print("Queue length after enqueue:", length)

    # 6) Dequeue the list of IDs
    popped = dequeue_message_ids(timeout=2)
    print("Dequeued message IDs:", popped)

    # 7) Verify queue is empty
    final_len = redis_client.llen(MESSAGE_QUEUE)
    print("Queue length after dequeue:", final_len)

if __name__ == "__main__":
    main()

