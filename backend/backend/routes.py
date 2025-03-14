from pyramid.config import Configurator 
from backend.views import options_view
import logging

# Configura el logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def includeme(config):
    # Rutas de la API
    config.add_route('home', '/')
    
    # Manejo de solicitudes OPTIONS para CORS
    config.add_route('options', '*path', request_method='OPTIONS')

    # Agregar rutas para login
    config.add_route('login', '/api/login') 
    config.add_route('auth_google', '/api/auth_google') 

    # Validacion de toke
    config.add_route('dashboard', '/api/dashboard') 
    
    # Usuarios
    config.add_route('listusers', '/api/listusers')
    config.add_route('createuser', '/api/createuser')
    config.add_route('user', '/api/users/{id}')
    
    # Productos
    config.add_route('products', '/api/products')
    config.add_route('createproduct', '/api/createproduct')
    config.add_route('product', '/api/products/{id}')
    
    # Órdenes
    config.add_route('orders', '/api/orders')
    config.add_route('order', '/api/orders/{id}')


    config.add_view(options_view.options_view, route_name='options', renderer='json')
