from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates default admin user admin/admin if it does not exist'

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('Admin user already exists'))
            return

        user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        user.profile.role = 'admin'
        user.profile.nickname = 'admin'
        user.profile.slug = 'admin'
        user.profile.is_banned = False
        user.profile.banned_reason = ''
        user.profile.save()

        self.stdout.write(self.style.SUCCESS('Created admin/admin'))
