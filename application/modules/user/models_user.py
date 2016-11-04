__author__ = 'wilrona'

from google.appengine.ext import ndb


class Users(ndb.Model):

    date_create = ndb.DateTimeProperty(auto_now_add=True)

    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    matricule = ndb.StringProperty()

    logged = ndb.BooleanProperty(default=False)
    is_enabled = ndb.BooleanProperty(default=False)

    def is_active(self):
        return self.is_enabled

    def is_authenticated(self):
        return self.logged

    def is_anonymous(self):
        return False

    def full_name(self):
        full_name = ''+str(self.first_name)+' '+str(self.last_name)
        return full_name

    def nbr_participation(self):
        part = Participation.query(
            Participation.user == self.key
        ).count()
        return part


class Participation(ndb.Model):
    nbr_reponse = ndb.StringProperty()
    pourcentage = ndb.FloatProperty()
    user = ndb.KeyProperty(kind=Users)









