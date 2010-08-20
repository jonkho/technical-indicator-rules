import os
import django.core.handlers.wsgi  
os.environ['DJANGO_SETTINGS_MODULE'] = 'sparrow.settings_prod' 
application = django.core.handlers.wsgi.WSGIHandler() 
