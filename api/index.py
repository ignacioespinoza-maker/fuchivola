import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fuchivola.settings')

app = get_wsgi_application()

def handler(request):
    """Handler para Vercel Serverless Functions"""
    return app(request)
