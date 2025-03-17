from pyramid.view import view_config
from pyramid.response import Response
from pyramid.security import Allow, Everyone
import logging

logger = logging.getLogger(__name__)

@view_config(route_name='options', request_method='OPTIONS')
def options_view(request):
    logger.info("Solicitud OPTIONS recibida")
    headers = {
        'Access-Control-Allow-Origin': 'http://localhost:3000',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Credentials': 'true',
    }
    return Response(status=200, headers=headers)

# Middleware para permitir CORS en todas las respuestas
def add_cors_headers(event):
    event.response.headers.update({
        'Access-Control-Allow-Origin': 'http://localhost:3000',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Credentials': 'true',
    })

def includeme(config):
    config.add_subscriber(add_cors_headers, 'pyramid.events.NewResponse')
