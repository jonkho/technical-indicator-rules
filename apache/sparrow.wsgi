import os, sys, socket
apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
#sys.stdout = sys.stderr
sys.path.append(workspace)
sys.path.append('/home/developer/denv/lib/python2.6/')

import wsgi_monitor
wsgi_monitor.start(interval=1.0)


os.environ['DJANGO_SETTINGS_MODULE'] = 'sparrow.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler() 