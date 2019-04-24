from django.core.management import call_command
from django_extensions.management.jobs import DailyJob


class Job(DailyJob):
    help = "job for failing pending transactions."
    def execute(self):
        call_command('remove_pending_transactions')
