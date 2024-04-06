from model.Journal import Journal
from model.Question import Question
import datetime
from utils.data.questions import questions
import random


class JournalService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def getInstance(self):
        return self._instance
    def createJournal(self, email, spotify_id):
        generated_questions = []
        for i in range(12):
            random_index = random.randint(0, len(questions)-1)
            generated_questions.append(Question(question=questions[random_index], answer="not set", emotion="not set"))

        journal = Journal(email=email,
                          spotify_id=spotify_id,
                          date=datetime.datetime.now().timestamp(),
                          emotion='not set',
                          questions=generated_questions
                          )

        journal.save()
        return journal
