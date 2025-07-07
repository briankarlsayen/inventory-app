from mongoengine import Document, StringField, IntField, BooleanField, DateTimeField, ReferenceField
from datetime import datetime, timezone

class Category(Document):
    name = StringField(required=True, max_length=255)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now(timezone.utc))
    updated_at = DateTimeField(default=datetime.now(timezone.utc))

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now(timezone.utc)
        return super().save(*args, **kwargs)
    
class Item(Document):
    name = StringField(required=True, max_length=255)
    category = ReferenceField(Category, required=True)
    unit = StringField(max_length=50)
    reorder_level = IntField(default=0)
    is_shown = BooleanField(default=True)
    is_active = BooleanField(defaul=True)