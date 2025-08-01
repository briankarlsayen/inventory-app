from mongoengine import Document, StringField, IntField, BooleanField, DateTimeField, ReferenceField, FloatField
from datetime import datetime, timezone
import bcrypt

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

class User(Document):
    name = StringField(required=True, max_length=255)
    username = StringField(required=True, max_length=255)
    password = StringField(required=True, max_length=255)
    role = IntField(default=2, choices=[1,2])
    is_active = BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def is_authenticated(self):
        return True  # or return self.authenticated if you track it manually
    
    def set_password(self, raw_password):
        """Hash & set the password."""
        hashed = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        self.password = hashed.decode('utf-8')

    def check_password(self, raw_password):
        """Verify the password."""
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

class Stock(Document):
    type=StringField(required=True, max_length=10, default="entry") # entry | usage
    item = ReferenceField(Item, required=True)
    quantity = IntField()
    remarks = StringField(required=False, max_length=255)
    usage_type = StringField(required=False, max_length=50) # sale | waste | internal use
    is_active=BooleanField(default=True)
    date = DateTimeField(default=datetime.now(timezone.utc))
    created_at = DateTimeField(default=datetime.now(timezone.utc))
    updated_at = DateTimeField(default=datetime.now(timezone.utc))

class Logs(Document):
    method = StringField(required=True, max_length=10)
    path = StringField()
    query_params = StringField()
    body = StringField()
    remote_addr = StringField()
    status_code = IntField()
    response_body = StringField()
    started_at = DateTimeField(default=datetime.now(timezone.utc))
    finished_at = DateTimeField()
    duration_ms = FloatField()