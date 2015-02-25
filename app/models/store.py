from ferris.core.ndb import Model
from google.appengine.ext import ndb

class Store(Model):
    number = ndb.IntegerProperty(indexed=True)
    name = ndb.StringProperty(indexed=False)
    address1 = ndb.StringProperty(indexed=False)
    address2 = ndb.StringProperty(indexed=False)
    suburb = ndb.StringProperty(indexed=False)
    state = ndb.StringProperty(indexed=False)
    postcode = ndb.StringProperty(indexed=False)

    @classmethod
    def all_stores(cls):
        return cls.query().order(cls.number)

    @classmethod
    def get_by_store_num(cls, store_number):
        return cls.query(cls.number == store_number).order(cls.number)

    @classmethod
    def create(cls, params):
        item = cls()
        item.populate(**params)
        item.put()
        return item
