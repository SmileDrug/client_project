from mongoengine import *

class admin(DynamicDocument):
    username = StringField(unique=True)
    password = StringField()
