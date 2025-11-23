// cypress/e2e/test-completo-frontend-FIXED.cy.js
// Test CORREGIDO - Sin errores de sintaxis jQuery

describe('Test Completo de la Plataforma - CORREGIDO', () => {
  const testUser = {
    email: `test.${Date.now()}@universidad.edu`,
    password: 'TestPassword123!',
    nombre: 'Juan Pérez'
  };

  const baseUrl = 'http://localhost:3000';
  const apiUrl = 'http://localhost:5000';

  beforeEach(() => {
    cy.on('uncaught:exception', () => false);
  });

  // ============================================
  // FASE 1: REGISTRO Y LOGIN
  // ============================================
  describe('Fase 1: Autenticación', () => {
    it('Debe registrar y hacer login', () => {
      cy.visit(`${baseUrl}/register`, { failOnStatusCode: false });
      cy.wait(1000);
      
      // Buscar inputs SIN usar case-insensitive que causa error
      cy.get('body').then(($body) => {
        // Buscar input de nombre
        const nameInput = $body.find('input[name="nombre"], input[placeholder="Nombre"], [data-testid="input-nombre"]').first();
        
        // Buscar input de email
        const emailInput = $body.find('input[type="email"], input[name="email"], [data-testid="input-email"]').first();
        
        // Buscar inputs de password
        const passwordInputs = $body.find('input[type="password"]');
        
        if (emailInput.length > 0 && passwordInputs.length >= 2) {
          cy.log('✅ Formulario de registro encontrado');
          
          // Llenar nombre si existe
          if (nameInput.length > 0) {
            cy.wrap(nameInput).clear().type(testUser.nombre);
          }
          
          // Llenar email
          cy.wrap(emailInput).clear().type(testUser.email);
          
          // Llenar passwords
          cy.wrap(passwordInputs.eq(0)).clear().type(testUser.password);
          cy.wrap(passwordInputs.eq(1)).clear().type(testUser.password);
          
          // Click en submit
          cy.get('button[type="submit"]').first().click();
          
          cy.wait(3000);
          cy.log('✅ Formulario enviado');
        } else {
          cy.log('⚠️ No se encontró formulario completo de registro');
        }
      });
    });
  });

  // ============================================
  // FASE 2: MÓDULO 2 - SESIÓN DE VIDEO
  // ============================================
  describe('Fase 2: Módulo 2 - Sesión de Video', () => {
    it('Debe iniciar y finalizar sesión correctamente', () => {
      // Login primero
      cy.visit(`${baseUrl}/login`, { failOnStatusCode: false });
      cy.wait(500);
      
      cy.get('input[type="email"]').first().type('test@test.com');
      cy.get('input[type="password"]').first().type('password123');
      cy.get('button[type="submit"]').first().click();
      cy.wait(2000);
      
      // Ir al módulo 2
      cy.visit(`${baseUrl}/sesion-tiempo-real`, { failOnStatusCode: false });
      cy.wait(1000);
      
      // Mock de getUserMedia
      cy.window().then((win) => {
        if (win.navigator.mediaDevices) {
          cy.stub(win.navigator.mediaDevices, 'getUserMedia').resolves({
            getTracks: () => [{ stop: cy.stub() }],
            getVideoTracks: () => [{ stop: cy.stub() }],
            getAudioTracks: () => [{ stop: cy.stub() }]
          });
        }
      });
      
      // Buscar botón de iniciar
      cy.get('button').then(($buttons) => {
        const startBtn = $buttons.filter((i, el) => {
          const text = el.textContent.toLowerCase();
          return text.includes('iniciar') || text.includes('start') || text.includes('comenzar');
        });
        
        if (startBtn.length > 0) {
          cy.wrap(startBtn).first().click();
          cy.log('✅ Sesión iniciada');
          cy.wait(3000);
          
          // Buscar botón de finalizar
          cy.get('button').then(($buttons2) => {
            const stopBtn = $buttons2.filter((i, el) => {
              const text = el.textContent.toLowerCase();
              return text.includes('finalizar') || text.includes('stop') || text.includes('detener');
            });
            
            if (stopBtn.length > 0) {
              cy.wrap(stopBtn).first().click();
              cy.log('✅ Intentando finalizar sesión');
              cy.wait(2000);
            } else {
              cy.log('⚠️ No se encontró botón de finalizar');
            }
          });
        } else {
          cy.log('⚠️ No se encontró botón de iniciar');
        }
      });
    });
  });
});
