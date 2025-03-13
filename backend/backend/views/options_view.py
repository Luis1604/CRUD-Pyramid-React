from pyramid.view import view_config
from pyramid.response import Response

@view_config(route_name='options', request_method='OPTIONS')
def options_view(request):
    print("Solicitud OPTIONS recibida")
    headers = {
        'Access-Control-Allow-Origin': 'http://localhost:3000',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Credentials': 'true',
    }
    return Response(status=200, headers=headers)