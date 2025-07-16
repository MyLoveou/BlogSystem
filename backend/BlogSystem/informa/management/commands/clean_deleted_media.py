from django.core.management.base import BaseCommand
from models import DeletedMedia

class Command(BaseCommand):
    help = '清除回收站中过期的文件'

    def handle(self, *args, **options):
        DeletedMedia.clean_expired(days=30)
        self.stdout.write(self.style.SUCCESS('成功清除过期文件'))