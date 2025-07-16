from shared.storage import client, ensure_bucket, upload_file, upload_stream, get_presigned_url
import io
from datetime import timedelta
import json
from shared.queue import redis_client, enqueue_message, dequeue_message, MESSAGE_QUEUE

# Configuration for test
TEST_BUCKET = "test-bucket"
TEST_FILE_PATH = "test.txt"
TEST_OBJECT_NAME = "test_folder/test.txt"
TEST_CONTENT = b"Hello, MinIO!"
TEST_STREAM_NAME = "stream_test.txt"
# Write a small local file for upload_file test
with open(TEST_FILE_PATH, "wb") as f:
    f.write(TEST_CONTENT)

# 1. Ensure bucket
print(f"Ensuring bucket '{TEST_BUCKET}' exists...")
ensure_bucket(TEST_BUCKET)

# 2. Test upload_file
print(f"Uploading local file '{TEST_FILE_PATH}' to '{TEST_BUCKET}/{TEST_OBJECT_NAME}'...")
upload_file(TEST_BUCKET, TEST_OBJECT_NAME, TEST_FILE_PATH, content_type="text/plain")

# 3. Test upload_stream
print(f"Uploading bytes stream as '{TEST_BUCKET}/{TEST_STREAM_NAME}'...")
stream = io.BytesIO(TEST_CONTENT)
upload_stream(TEST_BUCKET, TEST_STREAM_NAME, stream, length=len(TEST_CONTENT), content_type="text/plain")

# 4. List buckets and objects
print("Buckets available:")
for b in client.list_buckets():
    print(" -", b.name)

print(f"Objects in '{TEST_BUCKET}':")
objects = client.list_objects(TEST_BUCKET, recursive=True)
for obj in objects:
    print(" -", obj.object_name)

# 5. Test presigned URL
print("Generating presigned URL for stream object...")
url = get_presigned_url(TEST_BUCKET, TEST_STREAM_NAME, expires=timedelta(minutes=5))
print("Presigned URL:", url)


# Enqueue a message
test_payload = {"platform": "test", "text": "Hello, Queue!", "id": 123}
print("Enqueueing payload: ", test_payload)
enqueue_message(test_payload)

# 3) Check queue length via Redis client
length = redis_client.llen(MESSAGE_QUEUE)
print(f"Queue length after enqueue: {length}")

# 4) Dequeue it
print("Dequeuing payload…")
result = dequeue_message(timeout=2)
print("Dequeued payload:", result)

# 5) Confirm queue is empty
final_len = redis_client.llen(MESSAGE_QUEUE)
print(f"Queue length after dequeue: {final_len}")



