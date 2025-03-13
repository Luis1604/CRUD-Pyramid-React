from pyramid.config import Configurator
from backend.routes import includeme


def main(global_config, **settings):
    """ Esta función retorna una aplicación Pyramid WSGI. """

    with Configurator(settings=settings) as config:
        config.add_static_view(name='static', path='backend:static', cache_max_age=3600)
        config.include(includeme)
        config.include('pyramid_tm')
        config.include('pyramid_mako')  
        config.include('.routes')
        config.include('.models') 
        config.scan()
    return config.make_wsgi_app()
