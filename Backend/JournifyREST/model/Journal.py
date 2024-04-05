from mongoengine import Document, StringField, EmbeddedDocumentField, ListField, LongField
from model.Question import Question

class Journal(Document):
    spotify_id = StringField(required=True)
    email = StringField(required=True)
    date = LongField(required=True)
    emotion = StringField(required=True)
    questions = ListField(
        EmbeddedDocumentField(document_type=Question)
    )
