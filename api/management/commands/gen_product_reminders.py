from django.core.management import BaseCommand
from api.models import BatchWarning

class Command(BaseCommand):
    help = "Create product reminders for expiring batches"

    def handle(self, *args, **options):
        BatchWarning.generate_all_warnings()
