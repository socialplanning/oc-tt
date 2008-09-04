==================================
 tasktracker opencore integration
==================================

URI convenience api
===================

    >>> from opencore.utility.interfaces import IProvideSiteConfig
    >>> from zope.component import getUtility
    >>> getUtility(IProvideSiteConfig)._set('tasktracker uri', 'http://nohost:tasktracker')


Dummy 'tasks' view
==================

A dummy view is registered at the URL used for a project's tasks, just
to prevent people from accidentally creating pages at that URL. (See
also in opencore: opencore/nui/setup.txt)

    >>> project = self.portal.projects.p1
    >>> from opencore.browser.naming import ProjectDummy
    >>> view = project.restrictedTraverse('tasks')
    >>> isinstance(view, ProjectDummy)
    True

This dummy view will block creating a page at that path::

    >>> self.loginAsPortalOwner()
    >>> id1 = project.invokeFactory('Document', 'tasks', title='Bad Path')
    >>> import transaction
    >>> sp = transaction.savepoint(optimistic=True)

Let's make sure our content got renamed::

    >>> from opencore.upgrades.utils import move_blocking_content
    >>> move_blocking_content(self.portal)
    >>> id1 in project.objectIds()
    False
    >>> '%s-page' % id1 in project.objectIds()
    True



featurelet install
==================

    >>> from opencore.tasktracker.featurelet import TaskTrackerFeaturelet
    >>> project = self.app.plone.projects.p1
    >>> ttf = TaskTrackerFeaturelet(project)

The mock http should be hooked up::

    >>> ttf.http
    <HTTPMock ... httplib2.Http>

Calling request(uri) on the mock http will return a (response, content)
tuple like httplib2.Http.request()::
    >>> response, content = ttf.http.request('http://nohost')
    Called ...

The response is set up to return status code 200::
    >>> response.status
    200
    >>> content
    'Mock request succeeded!'

Install a tasktracker featurelet
================================

Make sure we can install a TaskTracker featurelet too::
    >>> self.loginAsPortalOwner()
    >>> form_vars = dict(title='new full name',
    ...                  workflow_policy='closed_policy',
    ...                  update=True,
    ...                  featurelets=['tasks'],
    ...                  set_flets=1,
    ...                  __initialize_project__=False)

    >>> proj = self.portal.projects.p3
    >>> view = proj.restrictedTraverse('preferences')
    >>> view.request.set('flet_recurse_flag', None)
    >>> view.request.form.update(form_vars)
    >>> view.handle_request()

    >>> from opencore.project.utils import get_featurelets
    >>> get_featurelets(proj)
    [{'url': 'tasks', 'name': 'tasks', 'title': u'Tasks'}]

Featurelet removal (stolen from
opencore/project/browser/delete-project.txt)
============================================

    >>> from opencore.project.browser.preferences import handle_flet_uninstall

Tasks are now deleted from a project, and the message is sent through
cabochon::

    >>> handle_flet_uninstall(project) 

Gotta reinstall::    

    >>> from topp.featurelets.interfaces import IFeatureletSupporter
    >>> IFeatureletSupporter(project).installFeaturelet(TaskTrackerFeaturelet(project))
