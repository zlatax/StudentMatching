from mongoengine import Document
from mongoengine import DateTimeField, StringField, ReferenceField, ListField

class Student(Document):
    username=StringField(max_length=50, required=True)
    email=StringField(max_length=50, required=True, unique=True)
    institution=StringField(max_length=50, required=True)
    