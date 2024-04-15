from mongoengine import EmbeddedDocument, StringField, IntField
class Question(EmbeddedDocument):
    question = StringField(required=True)
    answer = StringField(required=True)
    emotion = StringField(required=True)
    img = StringField(required=True)
    index = IntField(required=True)


