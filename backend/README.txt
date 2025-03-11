# Proyecto de CRUD con Pyramid y SQLAlchemy

Este proyecto es una implementación de un sistema de eCommerce usando Pyramid y SQLAlchemy. Incluye un conjunto de modelos de base de datos que gestionan usuarios, productos y pedidos. Este README proporciona una descripción general del proyecto y cómo configurarlo.

## Estructura del Proyecto

El proyecto está estructurado para usar Pyramid como framework de backend y SQLAlchemy para manejar la base de datos. La estructura de los modelos refleja un sistema de comercio electrónico básico donde los usuarios pueden realizar pedidos que contienen productos.

## Modelos

El proyecto define varios modelos de base de datos que se utilizan para almacenar información de usuarios, productos y pedidos. Los modelos están implementados en clases de Python y usan SQLAlchemy para mapear las tablas de la base de datos.

### `User`
El modelo `User` representa a un usuario en el sistema. Los usuarios tienen un nombre, un correo electrónico y una contraseña encriptada. También se define una relación con los pedidos realizados por el usuario.

#### Campos:
- `id`: Identificador único del usuario (clave primaria).
- `name`: Nombre del usuario.
- `email`: Correo electrónico único del usuario.
- `hashed_password`: Contraseña encriptada del usuario.

#### Métodos:
- `check_password(password)`: Verifica si la contraseña proporcionada coincide con la contraseña almacenada.
- `set_password(password)`: Establece una nueva contraseña encriptada.

### `Product`
El modelo `Product` representa un producto en el sistema. Los productos tienen un nombre, una descripción y un precio.

#### Campos:
- `id`: Identificador único del producto (clave primaria).
- `name`: Nombre del producto.
- `description`: Descripción del producto.
- `price`: Precio del producto.

#### Relaciones:
- Se establece una relación con los productos a través de la tabla intermedia `order_products`.

### `Order`
El modelo `Order` representa un pedido realizado por un usuario. Los pedidos están asociados a un usuario a través de la clave foránea `user_id`. Además, están relacionados con los productos a través de la tabla `order_products`.

#### Campos:
- `id`: Identificador único del pedido (clave primaria).
- `user_id`: Identificador del usuario que realizó el pedido (clave foránea hacia `users`).
  
#### Relaciones:
- Relación con `User`: Cada pedido está asociado con un usuario que lo realizó.
- Relación con `OrderProduct`: Los productos del pedido están asociados a través de la tabla `order_products`.

### `OrderProduct`
El modelo `OrderProduct` es una tabla intermedia entre los modelos `Order` y `Product`. Esta tabla maneja la relación muchos a muchos entre pedidos y productos.

#### Campos:
- `order_id`: Identificador del pedido (clave foránea hacia `orders`).
- `product_id`: Identificador del producto (clave foránea hacia `products`).

#### Relaciones:
- Relación con `Order`: Cada entrada en `order_products` está asociada con un pedido.
- Relación con `Product`: Cada entrada en `order_products` está asociada con un producto.

## Instalación

Para ejecutar este proyecto en tu máquina local, sigue los siguientes pasos:

### Requisitos previos:
- Python 3.10+.
- PostgreSQL o cualquier otra base de datos compatible con SQLAlchemy.

### Pasos de instalación:

1. **Clonar el repositorio:**

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <DIRECTORIO_DEL_REPOSITORIO>
