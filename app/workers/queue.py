from rq import Queue
from redis import Redis
from ..config import settings

redis_conn = Redis.from_url(settings.REDIS_URL)
queue = Queue(settings.RQ_QUEUE_NAME, connection=redis_conn, default_timeout=600)
