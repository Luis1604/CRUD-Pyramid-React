import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.services.order_service import create_order, delete_order
from backend.models.order_product import OrderProduct
from backend.models.order import Order
from backend.models.product import Product
from backend.models.user import User
from backend.models.meta import Base

# Configuración para las pruebas
@pytest.fixture(scope="module")
def test_db():
    # Crear un motor y una sesión para la base de datos de prueba
    engine = create_engine("sqlite:///:memory:", echo=True)  # Base de datos en memoria para pruebas
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db_session = Session()
    
    # Crear datos de prueba
    user = User(id=1, name="Test User", email="test@example.com", hashed_password="test")
    db_session.add(user)
    db_session.commit()

    product1 = Product(id=1, name="Product 1", description="Description 1", price=10.0)
    product2 = Product(id=2, name="Product 2", description="Description 2", price=20.0)
    db_session.add_all([product1, product2])
    db_session.commit()

    yield db_session
    
    db_session.close()
    engine.dispose()

def test_create_order(test_db):
    # Prueba de creación de orden
    user_id = 1
    product_ids = [1, 2]

    order = create_order(test_db, user_id, product_ids)
    
    assert order is not None  # Verifica que la orden ha sido creada
    assert order.user_id == user_id  # Verifica que el user_id es el correcto
    assert len(order.products) == 2  # Verifica que se han asignado 2 productos
    assert order.products[0].product_id == product_ids[0]  # Verifica el primer producto
    assert order.products[1].product_id == product_ids[1]  # Verifica el segundo producto

def test_delete_order(test_db):
    # Prueba de eliminación de orden
    order = create_order(test_db, 1, [1, 2])
    order_id = order.id
    
    # Llamamos a la función de eliminación directamente
    deleted_order = delete_order(test_db, order_id)
    
    assert deleted_order.id == order_id  # Verifica que la orden eliminada sea la correcta
    assert delete_order(test_db, order_id) is None  # Verifica que la orden ya no existe después de eliminarla
