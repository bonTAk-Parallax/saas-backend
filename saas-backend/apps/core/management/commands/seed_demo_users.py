
# apps/core/management/commands/seed_demo_users.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

# Adjust these imports to your actual app structure
from apps.organization.models import Organization
from apps.user.models import UserProfile

User = get_user_model()


class Command(BaseCommand):
    help = "Seed demo users with correctly-configured org + role for local testing."

    @transaction.atomic
    def handle(self, *args, **options):
        org, _ = Organization.objects.get_or_create(name="Alpha")

        demo_users = [
            {
                "email": "owner@alpha.test",
                "password": "demo-pass-owner-1",
                "role": "owner",  # must match a key in ROLE_SCOPES
            },
            {
                "email": "member@alpha.test",
                "password": "demo-pass-member-1",
                "role": "member",  # a role with fewer scopes, e.g. read-only
            },
        ]

        for u in demo_users:
            user, created = User.objects.get_or_create(
                email=u["email"], defaults={"username": u["email"]}
            )
            user.set_password(u["password"])
            user.save()

            profile, _ = UserProfile.objects.get_or_create(
                user=user,\
                defaults={
                "organization": org,
                "role": u["role"],
                },
            )
            profile.organization = org
            profile.role = u["role"]
            profile.save()

            status = "created" if created else "updated"
            self.stdout.write(self.style.SUCCESS(f"{status}: {u['email']} / {u['password']} (role={u['role']})"))

        self.stdout.write(self.style.WARNING(
            "\nCompare these against your manually-created admin: "
            "check that admin's profile.role is actually set to a key that exists in ROLE_SCOPES. "
            "If it's blank/None, that's your 403."
        ))
