from redis import Redis
from rq import Worker, Queue

listen = "default"
redis_conn = Redis(host="redis", port=6379)

if __name__ == "__main__":
    q = Queue(name=listen, connection=redis_conn)
    worker = Worker([q], connection=redis_conn)
    worker.work()
