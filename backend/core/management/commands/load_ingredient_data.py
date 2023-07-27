from csv import DictReader

from django.core.management import BaseCommand
from loguru import logger

from recipes.models import Ingredient

db_model = Ingredient
model_name = 'ingredient'
file_name = 'ingredients.csv'
file_path = 'data/' + file_name

ALREDY_LOADED_ERROR_MESSAGE = f"""
If you need to reload the {model_name} data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):

    help = f'Loads data from {file_path} to database.'

    def handle(self, *args, **options):
        if db_model.objects.exists():
            logger.warning(f'Data for model {db_model} is already loaded.')
            logger.info(ALREDY_LOADED_ERROR_MESSAGE)
            return

        logger.info(f'Loading {db_model} data to database')

        try:
            with open(file_path, mode="r", encoding="utf-8-sig") as csv_file:

                for row in DictReader(csv_file):
                    data = db_model(
                        name=row['name'],
                        measurement_unit=row['measurement_unit']
                    )
                    data.save()

            logger.info(f'Saved {model_name} data')

        except Exception as e:
            logger.error(e)
