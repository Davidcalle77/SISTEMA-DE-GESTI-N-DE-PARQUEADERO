// Parqueadero Autos Colombia - main.js

// Auto-cerrar alertas despues de 4 segundos
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.alert').forEach(a => {
    setTimeout(() => {
      a.style.transition = 'opacity .4s';
      a.style.opacity = '0';
      setTimeout(() => a.remove(), 400);
    }, 4000);
  });
});
