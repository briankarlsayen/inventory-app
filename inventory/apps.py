from django.apps import AppConfig
import mongoengine
import os


class InventoryConfig(AppConfig):
    name = 'inventory'

    def ready(self):
        mongoengine.connect(
            db=os.getenv('DB_NAME'),   # your db name
            host=os.getenv('DB_URL')
        )

