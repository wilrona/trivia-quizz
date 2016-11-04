__author__ = 'Ronald'


from google.appengine.ext import ndb


class Parametre(ndb.Model):
    nbr_participation = ndb.IntegerProperty()
    nbr_question = ndb.IntegerProperty()
    date_event = ndb.DateProperty()