import time
import threading

from django.core.management.base import BaseCommand
from django.conf import settings

from questions.tasks import update_most_active_users, update_popular_tags


class Command(BaseCommand):
    help = 'Runs a custom simple scheduler for periodic tasks'

    def handle(self, *args, **options):
        self.stdout.write("Starting scheduler...")
        interval = settings.CACHE_TTL // 2

        def run_periodically(task, interval_seconds):
            while True:
                try:
                    task.enqueue()
                except Exception as e:
                    self.stderr.write(f"Error in task {task}: {e}")
                time.sleep(interval_seconds)

        t1 = threading.Thread(target=run_periodically, args=(update_most_active_users, interval))
        t2 = threading.Thread(target=run_periodically, args=(update_popular_tags, interval))

        t1.daemon = True
        t2.daemon = True

        t1.start()
        t2.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stdout.write("Stopping scheduler...")
