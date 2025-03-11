# Frontend de eCommerce con React

Este repositorio contiene el frontend de un sistema de comercio electrónico construido con React. El frontend está diseñado para interactuar con una API de backend que gestiona usuarios, productos y pedidos. El sistema permite a los usuarios registrarse, iniciar sesión, explorar productos y realizar pedidos.

## Estructura del Proyecto

La estructura de archivos del proyecto sigue las mejores prácticas de React, lo que permite la modularidad y la escalabilidad del código. A continuación se describe la organización del proyecto:


### Descripción de las carpetas y archivos:
- **assets**: Contiene recursos como imágenes e íconos utilizados en la aplicación.
- **components**: Contiene componentes reutilizables como el encabezado (`Header.js`), pie de página (`Footer.js`) y barra lateral (`Sidebar.js`).
- **context**: Define los contextos de autenticación (`AuthContext.js`) y tema (`ThemeContext.js`).
- **hooks**: Contiene hooks personalizados como `useAuth.js` para manejar la autenticación y `useFetch.js` para manejar las peticiones a la API.
- **pages**: Contiene las páginas de la aplicación, como la página de inicio (`HomePage.js`), sobre nosotros (`AboutPage.js`) y contacto (`ContactPage.js`).
- **routes**: Gestiona las rutas de la aplicación, configuradas en el archivo `AppRoutes.js`.
- **services**: Contiene servicios de API como `api.js` y el servicio de autenticación (`authService.js`).
- **styles**: Archivos CSS globales y de tema como `global.css`, `variables.css` y `theme.css`.
- **App.js**: El componente principal de la aplicación.
- **index.js**: El punto de entrada principal para renderizar la aplicación en el DOM.
- **reportWebVitals.js**: Para medir el rendimiento de la aplicación.

## Requisitos previos

Antes de comenzar, asegúrate de tener lo siguiente instalado:
- [Node.js](https://nodejs.org/) (v14 o superior).
- [npm](https://www.npmjs.com/) o [yarn](https://yarnpkg.com/) (para gestionar dependencias).

## Instalación

1. **Clonar el repositorio:**

   Si aún no has clonado el repositorio, usa el siguiente comando:

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <DIRECTORIO_DEL_REPOSITORIO>
