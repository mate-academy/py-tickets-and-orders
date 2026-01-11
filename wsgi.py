import os
from django.core.wsgi import get_wsgi_application

# Дуже важливо: переконайся, що тут 'settings', а не 'py_tickets_and_orders.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

application = get_wsgi_application()