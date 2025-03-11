from pyramid.config import Configurator 

def includeme(config):
    # Rutas de la API
    config.add_route('home', '/')

    # Agregar rutas para login
    config.add_route('login', '/login')
    
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
    
    # Manejo de solicitudes OPTIONS para CORS
    config.add_route('options', '*path', request_method='OPTIONS')
