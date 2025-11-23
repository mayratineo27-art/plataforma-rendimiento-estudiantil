import './commands';
import 'cypress-file-upload';

// Configuración global
Cypress.on('uncaught:exception', (err, runnable) => {
  // Retorna false para prevenir que Cypress falle el test
  // en excepciones no controladas
  return false;
});