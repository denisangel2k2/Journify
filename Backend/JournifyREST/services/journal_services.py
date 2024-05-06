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
            random_index = random.randint(0, len(questions) - 1)
            generated_questions.append(
                Question(question=questions[random_index], answer="not set", emotion="not set", index=i, img=""))

        journal = Journal(email=email,
                          spotify_id=spotify_id,
                          date=datetime.datetime.now().timestamp(),
                          emotion='not set',
                          questions=generated_questions
                          )

        journal.save()
        return journal

    def getAverageEmotion(self, email, spotify_id):
        journal = Journal.objects(email=email, spotify_id=spotify_id).order_by('-date').exclude('id').first()
        emotions = []
        for question in journal.questions:
            emotions.append(question.emotion)
        # compute emotion with occurences
        occurancesEmotions = {
            'Happy': emotions.count('Happy'),
            'Sad': emotions.count('Sad'),
            'Energetic': emotions.count('Energetic'),
            'Calm': emotions.count('Calm')
        }
        maxEmotion = max(occurancesEmotions, key=occurancesEmotions.get)

        return occurancesEmotions, maxEmotion

    def getAllEmotions(self,email,spotify_id):
        journals= Journal.objects(email=email, spotify_id=spotify_id).exclude('id')
        emotions=[]
        for journal in journals:
            for question in journal.questions:
                emotions.append(question.emotion)

        occurancesEmotions = {
            'Happy': emotions.count('Happy'),
            'Sad': emotions.count('Sad'),
            'Energetic': emotions.count('Energetic'),
            'Calm': emotions.count('Calm')
        }
        return occurancesEmotions


