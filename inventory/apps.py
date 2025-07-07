from django.apps import AppConfig
import mongoengine

class InventoryConfig(AppConfig):
    name = 'inventory'

    def ready(self):
        mongoengine.connect(
            db='inventorydb',   # your db name
            host='mongodb://localhost:27017/inventorydb'
        )

