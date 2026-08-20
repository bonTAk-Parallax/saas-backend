
import django_rq
from rq import Retry

def queue_task(func_path, *args, **kwargs):
    queue = django_rq.get_queue('default')
    return queue.enqueue(
        func_path, *args,
        retry=Retry(max=3, interval=[10, 30, 60]),  
        job_timeout=360,
        **kwargs,
    )

