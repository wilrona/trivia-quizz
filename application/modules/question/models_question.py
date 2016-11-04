__author__ = 'Ronald'

from google.appengine.ext import ndb


class Question(ndb.Model):
    libelle = ndb.TextProperty()
    num = ndb.IntegerProperty()

    def nbr_reponse(self):
        repon = Reponse.query(
            Reponse.question == self.key
        ).count()
        return repon

    def list_reponse(self):
        repon = Reponse.query(
            Reponse.question == self.key
        )
        return repon

    def correct(self):
        reponse = False
        for list in self.list_reponse():
            if list.correct:
                reponse = True
        return reponse


class Reponse(ndb.Model):
    libelle = ndb.TextProperty()
    correct = ndb.BooleanProperty(default=False)
    question = ndb.KeyProperty(kind=Question)
