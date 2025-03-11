from pyramid.view import view_config

from .. import models

@view_config(route_name='home', renderer='backend:templates/mytemplate.mako')
def my_view(request):
    return {'project': 'Backend'}

