# myapp/management/commands/setup_roles.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from sprints.models import Sprint  # import your models

class Command(BaseCommand):
    help = 'Create default groups and assign permissions'

    def handle(self, *args, **kwargs):
        # 1. Create Sprint Manager group
        sprint_group, created = Group.objects.get_or_create(name="sprint_manager")
        if created:
            self.stdout.write("Created group: sprint_manager")
        else:
            self.stdout.write("Group already exists: sprint_manager")

        # 2. Fetch permissions
        content_type = ContentType.objects.get_for_model(Sprint)
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=[
                'add_sprint',
                'change_sprint',
                'delete_sprint',
            ]
        )

        # 3. Assign to group
        sprint_group.permissions.set(permissions)
        self.stdout.write("Assigned sprint permissions to sprint_manager")


        # 1. Create Sprint BA group
        sprint_group, created = Group.objects.get_or_create(name="sprint_BA")
        if created:
            self.stdout.write("Created group: sprint_BA")
        else:
            self.stdout.write("Group already exists: sprint_BA")

        # 2. Fetch permissions
        content_type = ContentType.objects.get_for_model(Sprint)
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=[
                'add_sprint',
                'change_sprint',
                'delete_sprint',
            ]
        )

        # 3. Assign to group
        sprint_group.permissions.set(permissions)
        self.stdout.write("Assigned sprint permissions to sprint_manager")