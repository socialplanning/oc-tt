from Products.CMFCore.utils import getToolByName
from opencore.interfaces import IProject
from opencore.tasktracker.interfaces import ITaskTrackerFeatureletInstalled
from opencore.utility.interfaces import IHTTPClient
from opencore.utility.interfaces import IProvideSiteConfig
from plone.memoize.instance import memoizedproperty, memoize
from topp.featurelets.base import BaseFeaturelet
from topp.featurelets.interfaces import IFeaturelet
from zope.component import getUtility
from zope.interface import implements
import logging

log = logging.getLogger('opencore.tasktracker')


class TaskTrackerFeaturelet(BaseFeaturelet):
    # could we make featurlets named utilities?
    # currently featurelet all have the same state always
    """
    A featurelet that installs a Task Tracker
    """

    implements(IFeaturelet)

    id = "tasks"
    title = "Task Tracker"
    installed_marker = ITaskTrackerFeatureletInstalled

    _required_interfaces = BaseFeaturelet._required_interfaces + (IProject,)
    _info = {'menu_items': ({'title': u'Tasks',
                             'description': u'Task tracker',
                             'action': 'tasks'
                             },
                            ),
             }

    @property
    def uri(self):
        return getUtility(IProvideSiteConfig).get('tasktracker uri')

    @property
    def active(self):
        return bool(self.uri)

    @property
    def init_uri(self):
        return "%s/project/initialize/" % self.uri

    # we're currently uninitializing projects, not destroying them
    @property
    def uninit_uri(self):
        return "%s/project/uninitialize/" % self.uri

    @property
    def destroy_uri(self):
        return "%s/project/destroy/" % self.uri

    @memoizedproperty
    def http(self):
        return getUtility(IHTTPClient)

    def _makeHttpReqAsUser(self, uri, obj, method="POST", headers=None):
        if headers is None: headers = {}
        auth = obj.acl_users.credentials_signed_cookie_auth

        user_id = getToolByName(obj, 'portal_membership').getAuthenticatedMember().getId()
        headers['Cookie'] = auth.generateCookie(user_id)
        headers['X-Openplans-Project'] = obj.getId()
        return self.http.request(uri, method=method, headers=headers)
