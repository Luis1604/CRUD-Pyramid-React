from pyramid.config import Configurator 

def includeme(config):
    
    config.add_route('home', '/')
    config.add_route('users', '/api/users')
    config.add_route('user', '/api/users/{id}')
    config.add_route('products', '/api/products')
    config.add_route('product', '/api/products/{id}')
    config.add_route('orders', '/api/orders')
    config.add_route('order', '/api/orders/{id}')
    
    #Manejo de solicitudes
    config.add_route('options', '*path', request_method='OPTIONS')
