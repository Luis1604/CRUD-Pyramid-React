<%inherit file="layout.mako"/>
<%block name="title">Error 404 - Página No Encontrada</%block>

<style>
  .error-container {
    text-align: center;
    padding: 80px 20px;
  }
  .error-title {
    font-size: 80px;
    font-weight: bold;
    color: #d9534f;
  }
  .error-subtitle {
    font-size: 24px;
    font-weight: 600;
    color: #5a5a5a;
  }
  .error-message {
    font-size: 18px;
    color: #777;
    margin-top: 10px;
  }
  .btn-home {
    margin-top: 20px;
    padding: 10px 20px;
    font-size: 18px;
    font-weight: bold;
    background-color: #0275d8;
    color: white;
    border-radius: 5px;
    text-decoration: none;
  }
  .btn-home:hover {
    background-color: #025aa5;
  }
</style>

<div class="container error-container">
  <h1 class="error-title">404</h1>
  <p class="error-subtitle">Página No Encontrada</p>
  <p class="error-message">Lo sentimos, la página que buscas no existe o ha sido movida.</p>
  <a href="/" class="btn btn-home">Volver al Inicio</a>
</div>
