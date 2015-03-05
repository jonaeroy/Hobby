from ferris import Controller, route, route_with,messages
from ferris.core.ndb import ndb
from app.models.phonebook import Phonebook
import json


class Phonebooks(Controller):
    class Meta:
        prefix = ('api',)
        components = (messages.Messaging, )
        Model = Phonebook

        

    ####################RESTFUL############################

    @route_with('/api/phonebooks', methods=['GET'])
    def api_list_all(self):
        self.context['data'] = PhoneBook.list_all()

    @route_with('/api/phonebooks', methods=['POST'])
    def api_create(self):
        params = json.loads(self.request.body)
        self.context['data'] = Phonebook.create(params)
