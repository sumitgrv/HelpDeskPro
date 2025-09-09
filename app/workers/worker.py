from .queue import queue, redis_conn
from rq import Worker
from ..utils.logging import logger

if __name__ == "__main__":
    logger.info("Starting RQ worker for queue 'helpdeskpro'")
    w = Worker([queue], connection=redis_conn)
    w.work(with_scheduler=True)
