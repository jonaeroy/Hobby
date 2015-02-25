from ferris import Controller, route_with, messages
from app.models.woolies_form import WooliesForm
from google.appengine.api import users
from app.models.user import User

#from plugins import directory
from google.appengine.api import memcache
from app.models.user import User

from ferris.core.ndb import BasicModel
from app.controllers.utils import Utils

from google.appengine.ext.ndb import FilterNode
from app.models.leaveapp import Leaveapp
from app.models.bnld import Bnld
from app.models.bws_store import BwsStore

#import google.appengine.ext.db

import logging
import json

from app.models.draft import Draft


class Main(Controller):
    listOfStatuses = ["Pending Approval", "Temporarily Approved", "Approved", "Rejected"]
    
    class Meta:
        prefixes = ('api', )
        components = (messages.Messaging, )
        Model = Draft


    class FormStats:
        def __init__(self,
                     formListId,
                     query,
                     queryApproverFilter,
                     statusFilter):
            self.query = query
            self.queryApproverFilter = queryApproverFilter
            self.statusFilter = statusFilter
            self.formListId = formListId
            self.isApprover = False
            self.formDescription = ""
            self.numberOfActions = 0
            self.statusCounts = [0, 0, 0, 0]

        def locatedData(self):
            if (self.numberOfActions > 0):
                return True

            for statusCount in self.statusCounts:
                if (statusCount > 0):
                    return True

            return False

        
    @route_with(template='/')
    def show(self):
        self.meta.view.template_name = 'angular/layouts/main.html'


    @route_with('/api/dashboard', methods=['GET'])
    def api_dashboard(self):

        user_group = self.session.get('user_group')
        is_approver = False
        is_admin = False
        user_directory_givenName = None
        user_directory_fullname = None
        woolies_forms = WooliesForm.all()
        user_email = self.session.get('user_email')
        user_from_directory = memcache.get('%s:users' % user_email)
        
        logging.info("user_from_directory==========> %s", user_from_directory)
        if user_from_directory is not None:
            user_directory_givenName = user_from_directory.get('name').get('givenName')
            user_directory_fullname  = user_from_directory.get('name').get('fullName')
        else:
            #user_from_directory = directory.get_user_by_email(user_email)
            logging.info("user_from_directory==> %s" % user_from_directory)
            if user_from_directory:
                if not memcache.add('%s:users' % user_email, user_from_directory, 60000):
                    logging.error('Memcache set failed.')
                    try:
                        user_directory_givenName = user_from_directory['givenName']
                        user_directory_fullname  = user_from_directory['fullName']
                    except:
                        pass
                    
        if user_group is not None:
            for forms in woolies_forms:
                for group in user_group:
                    if forms.first_level_manager == group:
                        is_approver = True
                        break
                    if forms.second_level_manager == group:
                        is_approver = True
                        break

            for forms in woolies_forms:
                for group in user_group:
                    if forms.form_administrator == group:
                        is_admin = True
                        break

        user_isFormApprover = is_approver
        user_isFormAdmin = is_admin

        statusText = "Pending Approval"

        current_user_email  = str(users.get_current_user().email()).lower()
        pending_status_code = Utils.revertStatus(statusText)

        if (isinstance(pending_status_code, int) != True):
            raise Exception("Status text: [%s] failed to be converted to a valid value." % (statusText,))


        listOfFormStats = []

        listOfFormStats.append(Main.FormStats(formListId="bnlds",                         \
                                               query=Bnld.query(),                         \
                                               queryApproverFilter="Merchandise_Manager",  \
                                               statusFilter="Status"))


        listOfFormStats.append(Main.FormStats(formListId="bws_stores",                    \
                                               query=BwsStore.query(),                     \
                                               queryApproverFilter=None,                   \
                                               statusFilter="status"))


        listOfFormStats.append(Main.FormStats(formListId="leaveapps",                     \
                                               query=Leaveapp.query(),                     \
                                               queryApproverFilter="Line_Manager",         \
                                               statusFilter="Status"))

        # Provide access to stats data for the UI
        formStats = listOfFormStats


        user_group = self.session.get('user_group')


        # for each form status object query the number of enteries that match the current user
        for formStats in listOfFormStats:

            # Locate the form description and the approver groups
            for form in woolies_forms:
                if  (form.list_url == formStats.formListId):
                    formStats.formDescription = form.name

                    if user_group:
                        for groupKey in user_group:
                            if  (groupKey in [form.first_level_manager, form.second_level_manager]):
                                formStats.isApprover = True
                                break

                    break


            if  (formStats.queryApproverFilter != None):
                # Collect requests that have the current user still to approve.
                filteredQuery = formStats.query.filter(FilterNode(formStats.queryApproverFilter,  "=", current_user_email))   \
                                               .filter(FilterNode(formStats.statusFilter,         "=", pending_status_code))

                formStats.numberOfActions = filteredQuery.count()

            elif  (formStats.isApprover):
                # The current user is an approver so any requests in the pending status will require action
                filteredQuery = formStats.query.filter(FilterNode(formStats.statusFilter,    "=", pending_status_code))

                formStats.numberOfActions = filteredQuery.count()


            # For each of the status values query the number of matching values for the current user for each of the statuses
            for statusIndex in range(len(self.listOfStatuses)):
                statusText = self.listOfStatuses[statusIndex]

                # Convert the status text to the Id stored within the data.
                statusCode = Utils.revertStatus(statusText)

                if  (isinstance(statusCode, int) != True):
                    raise Exception("Status text: [%s] failed to be converted to a valid value." % (statusText,))


                # For the current status code find the number of requests that the current user has instigated.
                filteredQuery = formStats.query.filter(BasicModel.created_by == users.User(email=current_user_email)) \
                                               .filter(FilterNode(formStats.statusFilter, "=", statusCode))

                # Store the result value into the array that aligns to the statuses we are checking
                formStats.statusCounts[statusIndex] = filteredQuery.count()

                user_group = self.session.get('user_group')
                
        is_approver = False
        is_admin = False
        user_directory_givenName = None
        user_directory_fullname = None
        woolies_forms = WooliesForm.all()
        user_email = self.session.get('user_email')
        user_from_directory = memcache.get('%s:users' % user_email)

        data = DasboardMessage(title = 'Dashboard',
                               is_approver = is_approver,
                               is_admin = is_admin)
        self.context['data'] = data

        
        
class DasboardMessage(messages.Message):
    title = messages.StringField(1)
    is_approver = messages.BooleanField(2, default=False)
    is_admin = messages.BooleanField(3, default=False)
    
    
        
        
#     self.context['PAGE_TITLE'] = 'Dashboard'
        
#         user_group = self.session.get('user_group')
#         is_approver = False
#         is_admin = False
#         woolies_forms = WooliesForm.all()
        
#         user_email = self.session.get('user_email')
#         user_from_directory = memcache.get('%s:users' % user_email)
#         logging.info("user_from_directory==========> %s", user_from_directory)
#         if user_from_directory is not None:
#             self.context['user_directory_givenName'] = user_from_directory.get('name').get('givenName')
#             self.context['user_directory_fullname'] = user_from_directory.get('name').get('fullName')
# else:

#             user_from_directory = directory.get_user_by_email(user_email)
#             logging.info("user_from_directory==> %s" % user_from_directory)
#             if user_from_directory:
#                 if not memcache.add('%s:users' % user_email, user_from_directory, 60000):
#                     logging.error('Memcache set failed.')
#                     try:
#                         self.context['user_directory_givenName'] = user_from_directory['givenName']
#                         self.context['user_directory_fullname'] = user_from_directory['fullName']
# except:
#     self.context['user_directory_givenName'] = None
#     self.context['user_directory_fullname'] = None

#         if user_group is not None:
#             for forms in woolies_forms:
#                 for group in user_group:
#                     if forms.first_level_manager == group:
#                         is_approver = True
#                         break
#                     if forms.second_level_manager == group:
#                         is_approver = True
#                         break

#             for forms in woolies_forms:
#                 for group in user_group:
#                     if forms.form_administrator == group:
#                         is_admin = True
#                         break

#         self.context['user_isFormApprover'] = is_approver
#         self.context['user_isFormAdmin'] = is_admin

#         statusText = "Pending Approval"

#         current_user_email  = str(users.get_current_user().email()).lower()
#         pending_status_code = Utils.revertStatus(statusText)

#         if (isinstance(pending_status_code, int) != True):
#             raise Exception("Status text: [%s] failed to be converted to a valid value." % (statusText,))


#         listOfFormStats = []

#         listOfFormStats.append(Main.FormStats(formListId="bnlds",                         \
#                                                query=Bnld.query(),                         \
#                                                queryApproverFilter="Merchandise_Manager",  \
#                                                statusFilter="Status"))


#         listOfFormStats.append(Main.FormStats(formListId="bws_stores",                    \
#                                                query=BwsStore.query(),                     \
#                                                queryApproverFilter=None,                   \
#                                                statusFilter="status"))


#         listOfFormStats.append(Main.FormStats(formListId="leaveapps",                     \
#                                                query=Leaveapp.query(),                     \
#                                                queryApproverFilter="Line_Manager",         \
#                                                statusFilter="Status"))

#         # Provide access to stats data for the UI
#         self.context["formStats"] = listOfFormStats


#         user_group = self.session.get('user_group')


#         # for each form status object query the number of enteries that match the current user
#         for formStats in listOfFormStats:

#             # Locate the form description and the approver groups
#             for form in woolies_forms:
#                 if  (form.list_url == formStats.formListId):
#                     formStats.formDescription = form.name

#                     if user_group:
#                         for groupKey in user_group:
#                             if  (groupKey in [form.first_level_manager, form.second_level_manager]):
#                                 formStats.isApprover = True
#                                 break

#                     break


#             if  (formStats.queryApproverFilter != None):
#                 # Collect requests that have the current user still to approve.
#                 filteredQuery = formStats.query.filter(FilterNode(formStats.queryApproverFilter,  "=", current_user_email))   \
#                                                .filter(FilterNode(formStats.statusFilter,         "=", pending_status_code))

#                 formStats.numberOfActions = filteredQuery.count()

#             elif  (formStats.isApprover):
#                 # The current user is an approver so any requests in the pending status will require action
#                 filteredQuery = formStats.query.filter(FilterNode(formStats.statusFilter,    "=", pending_status_code))

#                 formStats.numberOfActions = filteredQuery.count()


#             # For each of the status values query the number of matching values for the current user for each of the statuses
#             for statusIndex in range(len(self.listOfStatuses)):
#                 statusText = self.listOfStatuses[statusIndex]

#                  # Convert the status text to the Id stored within the data.
#                  statusCode = Utils.revertStatus(statusText)

#                  if  (isinstance(statusCode, int) != True):
#                      raise Exception("Status text: [%s] failed to be converted to a valid value." % (statusText,))


#                  # For the current status code find the number of requests that the current user has instigated.
#              filteredQuery = formStats.query.filter(BasicModel.created_by == users.User(email=current_user_email)) \
#                                             .filter(FilterNode(formStats.statusFilter, "=", statusCode))

#                  # Store the result value into the array that aligns to the statuses we are checking
#                  formStats.statusCounts[statusIndex] = filteredQuery.count()
