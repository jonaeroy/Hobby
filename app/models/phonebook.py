from ferris.core.ndb import BasicModel
from ferris.behaviors.searchable import Searchable
from google.appengine.ext import ndb

class Phonebook(BasicModel):
    
    Name = ndb.StringProperty(required=True)
    Number = ndb.StringProperty(required=True)

    class Meta:
        behaviors = (Searchable,)

    @classmethod
    def create(cls, params):
        item = cls()
        item.populate(**params)
        item.put()
        return item
        
    @classmethod
    def list(cls):
        return cls.query()
    
