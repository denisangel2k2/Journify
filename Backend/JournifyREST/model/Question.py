from mongoengine import EmbeddedDocument, StringField
class Question(EmbeddedDocument):
    question = StringField(required=True)
    answer = StringField(required=True)
    emotion = StringField(required=True)

