// Comando para attachFile (subir archivos)
import 'cypress-file-upload';

// Comando personalizado para login rápido
Cypress.Commands.add('login', (email, password) => {
  cy.visit('/login');
  cy.get('[data-testid="input-email"]').type(email);
  cy.get('[data-testid="input-password"]').type(password);
  cy.get('[data-testid="btn-login"]').click();
  cy.url().should('include', '/dashboard');
});

// Comando para stub de getUserMedia
Cypress.Commands.add('mockMediaDevices', () => {
  cy.window().then((win) => {
    cy.stub(win.navigator.mediaDevices, 'getUserMedia').resolves({
      getTracks: () => [{ stop: () => {} }],
      getVideoTracks: () => [{ stop: () => {} }],
      getAudioTracks: () => [{ stop: () => {} }]
    });
  });
});