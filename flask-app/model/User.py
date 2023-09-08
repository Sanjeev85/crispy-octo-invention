from datetime import datetime
from mongoengine import Document, StringField, EmailField, DateTimeField

class User(Document):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    name = StringField(required=True)
    profile_pic = StringField()
    created_at = DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return self.username
    
