import os
import sys
import site

site.addsitedir('/home/user/src/environments/bearapps/lib/python2.7/site-packages')

path = '/home/user/src/bearapps/bear_apps'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'bear_apps.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

