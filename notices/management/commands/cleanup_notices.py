# notices/management/commands/cleanup_notices.py
from django.core.management.base import BaseCommand
from notices.models import Notice
from django.utils import timezone

class Command(BaseCommand):
    help = 'Finds and deletes all expired notices from the database.'

    def handle(self, *args, **options):
        now = timezone.now()
        # Find all notices that have an expiry date and that date is in the past
        expired_notices = Notice.objects.filter(expiry_date__isnull=False, expiry_date__lte=now)
        
        count = expired_notices.count()
        
        if count > 0:
            expired_notices.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} expired notice(s).'))
        else:
            self.stdout.write(self.style.SUCCESS('No expired notices to delete.'))