
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create a Django app inside the apps/ directory."

    def add_arguments(self, parser):
        parser.add_argument("app_name")

    def handle(self, *args, **options):
        app_name = options["app_name"]

        if not app_name.isidentifier():
            raise CommandError(
                f"'{app_name}' is not a valid Python/Django app name."
            )

        base_dir = Path.cwd()
        app_dir = base_dir / "apps" / app_name

        if app_dir.exists():
            raise CommandError(
                f"App '{app_name}' already exists."
            )

        app_dir.mkdir(parents=True)

        migrations_dir = app_dir / "migrations"
        migrations_dir.mkdir()

        package_dirs = [
            "models",
            "views",
            "serializers",
        ]

        for directory in package_dirs:
            package_dir = app_dir / directory
            package_dir.mkdir()
            (package_dir / "__init__.py").touch()

        files = [
            "__init__.py",
            "admin.py",
            "urls.py",
            "signals.py",
            "tests.py",
        ]

        for filename in files:
            (app_dir / filename).touch()

        (migrations_dir / "__init__.py").touch()

        template_path = (
            base_dir
            / "apps"
            / "core"
            / "templates"
            / "apps.py.tpl"
        )

        if not template_path.exists():
            raise CommandError(
                f"Template not found: {template_path}"
            )

        class_name = "".join(
            part.capitalize()
            for part in app_name.split("_")
        )

        app_path = f"apps.{app_name}"

        template = template_path.read_text()

        apps_py = (
            template
            .replace("{{ class_name }}", class_name)
            .replace("{{ app_path }}", app_path)
        )

        (app_dir / "apps.py").write_text(apps_py)

        settings_path = base_dir / "config" / "settings.py"

        if not settings_path.exists():
            raise CommandError(
                f"settings.py not found: {settings_path}"
            )

        settings = settings_path.read_text()

        app_config = f'"{app_path}.apps.{class_name}Config",'

        if app_config in settings:
            raise CommandError(
                f"App '{app_name}' is already registered."
            )

        marker = "LOCAL_APPS = ["

        if marker not in settings:
            raise CommandError(
                "LOCAL_APPS not found in settings.py"
            )

        settings = settings.replace(
            marker,
            f"{marker}\n    {app_config}",
            1,
        )

        settings_path.write_text(settings)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created app '{app_name}' "
                f"at {app_path}"
            )
        )

