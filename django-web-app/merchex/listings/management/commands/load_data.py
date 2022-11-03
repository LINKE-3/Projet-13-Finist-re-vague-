from django.core.management.base import BaseCommand, CommandError
from listings.models import Spot
from listings.data_config import PLAGE

class Command(BaseCommand):
    help = 'Populate our Plage Database with data from file'

    def handle(self, *args, **options):
        try:
            all_data = Spot.objects.all()
            all_data.delete()

        except:
            pass

        for plage in PLAGE:
            try:
                model_spot = Spot(name=plage, photo="0")
                model_spot.save()  
            except:
                continue
