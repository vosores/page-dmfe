import os
import sys

os.environ['EMAIL_HOST_USER'] = 'ingenieria.matematica@ucm.cl'
os.environ['EMAIL_HOST_PASSWORD'] = 'IngMate.UCM#'

# Ruta a tu proyecto
path = '/home/dmfeucm/page_dmfe'
if path not in sys.path:
    sys.path.append(path)

# Configurar el módulo de configuración de Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'dmfe.settings'

# Iniciar la aplicación WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()