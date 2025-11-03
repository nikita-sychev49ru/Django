from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "load data from fixture to the database"

    def handle(self, *args, **options):
        # очищаем базу данных
        Product.objects.all().delete()
        Category.objects.all().delete()
        # загрузка данных из фикстуры
        call_command("loaddata", "catalog_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
