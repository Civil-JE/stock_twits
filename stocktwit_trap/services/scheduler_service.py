from datetime import datetime
from stocktwit_trap import tasks


class SchedulerService:
    def __init__(self, scheduler=None):
        self.scheduler = scheduler

    def schedule_twit_rip(self, symbols):
        self.scheduler.schedule(
            scheduled_time=datetime.now(),
            func=tasks.get_twit_messages,
            args=[symbols],
            interval=180
        )

    def delete_queue(self, queue):
        # Reaaalllly make sure the queue isn't full of stuff so you don't get locked out of the API.
        # Probably a better way to do this, but fuck if I know.
        queue.empty()
        for job in self.scheduler.get_jobs():
            self.scheduler.cancel(job)
