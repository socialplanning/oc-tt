from opencore.testing import utils
from zope.app.component.hooks import setSite

def base_tt_setup(tc):
    tc.new_request = utils.new_request()
    import opencore.tasktracker
    from zope.app.annotation.interfaces import IAttributeAnnotatable
    from zope.testing.loggingsupport import InstalledHandler
    tc.log = InstalledHandler(opencore.tasktracker.LOG)
    setSite(tc.app.plone)

