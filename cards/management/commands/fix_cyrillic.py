"""
Management command to fix Cyrillic encoding in reference data.
Deletes and re-inserts data with proper UTF-8 encoding.
"""

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Fix Cyrillic encoding in reference data by re-inserting with proper UTF-8'

    def handle(self, *args, **options):
        # Check if there are vehicles
        from cards.models import Vehicle

        vehicle_count = Vehicle.objects.count()
        if vehicle_count > 0:
            self.stdout.write(
                'WARNING: Found {} vehicle(s). They will be deleted.'.format(vehicle_count)
            )
            confirm = input('Continue? Type "yes" to confirm: ')
            if confirm.lower() != 'yes':
                self.stdout.write('Aborted.')
                return

            Vehicle.objects.all().delete()
            self.stdout.write('Deleted all vehicles.')

        # Data with Cyrillic text - Python will store them as proper UTF-8 strings
        reference_data = {
            'cards_brandmodel': [
                'Lada',
                'Volga',
                'GAZ',
                'Ural',
                'KamAZ',
                'Java',
                'MAZ',
                'Volvo',
                'Mercedes',
                'Scania',
                'MAN',
                'Isuzu',
                'ZIL',
            ],
            'cards_color': [
                'Black',
                'White',
                'Red',
                'Blue',
                'Yellow',
                'Green',
                'Silver',
                'Gray',
                'Navy',
            ],
            'cards_vehicletype': [
                'Car',
                'Truck',
                'Bus',
                'Special',
                'Trailer',
            ],
            'cards_category': ['A', 'B', 'C', 'D', 'E'],
            'cards_fueltype': [
                'Gasoline',
                'Diesel',
                'Gas',
                'Hybrid',
                'Electric',
            ],
            'cards_bodytype': [
                'Sedan',
                'Coupe',
                'Hatchback',
                'Station Wagon',
                'SUV',
                'Crossover',
                'Minivan',
                'Pickup',
                'Van',
            ],
        }

        with connection.cursor() as cursor:
            # Delete all reference data
            self.stdout.write('Deleting old data...')
            cursor.execute('DELETE FROM cards_vehicle CASCADE')
            cursor.execute('DELETE FROM cards_brandmodel')
            cursor.execute('DELETE FROM cards_color')
            cursor.execute('DELETE FROM cards_vehicletype')
            cursor.execute('DELETE FROM cards_category')
            cursor.execute('DELETE FROM cards_fueltype')
            cursor.execute('DELETE FROM cards_bodytype')

            # Re-insert data
            for table, data_list in reference_data.items():
                self.stdout.write('Inserting into {}...'.format(table))
                for name in data_list:
                    cursor.execute(
                        'INSERT INTO {} (name) VALUES (%s)'.format(table),
                        [name]
                    )
                    self.stdout.write('  Added: {}'.format(name))

        self.stdout.write(self.style.SUCCESS('All reference data has been fixed!'))
