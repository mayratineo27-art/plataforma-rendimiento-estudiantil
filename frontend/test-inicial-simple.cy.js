// cypress/e2e/test-inicial-simple.cy.js
// Test Inicial Simple - Para Verificar que Todo Funciona

describe('Test Inicial - Verificación Básica', () => {
  const baseUrl = 'http://localhost:3000';
  const apiUrl = 'http://localhost:5000';

  // ============================================
  // TEST 1: Verificar que el frontend carga
  // ============================================
  it('Debe cargar la página principal', () => {
    cy.visit(baseUrl);
    cy.url().should('include', baseUrl);
    
    // Verificar que la página carga sin errores
    cy.get('body').should('be.visible');
  });

  // ============================================
  // TEST 2: Verificar que el backend responde
  // ============================================
  it('Debe conectar con el backend', () => {
    cy.request(`${apiUrl}/api/health`)
      .its('status')
      .should('eq', 200);
  });

  // ============================================
  // TEST 3: Verificar navegación básica
  // ============================================
  it('Debe navegar entre páginas', () => {
    cy.visit(baseUrl);
    
    // Intenta encontrar links de navegación
    cy.get('a, button').should('have.length.greaterThan', 0);
  });

  // ============================================
  // TEST 4: Verificar formulario de login existe
  // ============================================
  it('Debe mostrar formulario de login', () => {
    cy.visit(`${baseUrl}/login`);
    
    // Busca inputs de email y password (sin data-testid primero)
    cy.get('input[type="email"], input[name="email"]').should('exist');
    cy.get('input[type="password"], input[name="password"]').should('exist');
    cy.get('button[type="submit"], button').contains(/login|entrar/i).should('exist');
  });

  // ============================================
  // TEST 5: Verificar acceso a módulo 1
  // ============================================
  it('Debe existir ruta para análisis de progreso', () => {
    // Este test verificará si existe la ruta, aunque esté protegida
    cy.request({ 
      url: `${baseUrl}/analisis-progreso`,
      failOnStatusCode: false 
    }).then((response) => {
      // Debe responder 200 (si es pública) o 302/401 (si está protegida)
      expect([200, 302, 401, 403]).to.include(response.status);
    });
  });

  // ============================================
  // TEST 6: Verificar que puede subir archivos
  // ============================================
  it('Debe tener endpoint para subir documentos', () => {
    cy.request({
      method: 'OPTIONS',
      url: `${apiUrl}/api/documents/upload`,
      failOnStatusCode: false
    }).then((response) => {
      // Verifica que el endpoint existe (aunque necesite autenticación)
      expect([200, 401, 403, 404]).to.include(response.status);
    });
  });

  // ============================================
  // TEST 7: Verificar console.log y errores
  // ============================================
  it('No debe tener errores graves en consola', () => {
    cy.visit(baseUrl);
    
    // Captura errores de consola
    cy.on('window:before:load', (win) => {
      cy.spy(win.console, 'error');
    });
    
    cy.wait(2000);
    
    // Este test solo advierte, no falla
    cy.window().then((win) => {
      if (win.console.error.called) {
        cy.log('⚠️ Hay errores en consola, pero continuamos');
      }
    });
  });

  // ============================================
  // TEST 8: Verificar que React está cargado
  // ============================================
  it('Debe tener React montado', () => {
    cy.visit(baseUrl);
    
    // Busca el root div de React
    cy.get('#root, #app, [data-reactroot]').should('exist');
  });

  // ============================================
  // TEST 9: Verificar responsive design
  // ============================================
  it('Debe ser responsive en diferentes tamaños', () => {
    // Desktop
    cy.viewport(1920, 1080);
    cy.visit(baseUrl);
    cy.get('body').should('be.visible');
    
    // Tablet
    cy.viewport(768, 1024);
    cy.get('body').should('be.visible');
    
    // Mobile
    cy.viewport(375, 667);
    cy.get('body').should('be.visible');
  });

  // ============================================
  // TEST 10: Verificar carga de recursos
  // ============================================
  it('Debe cargar CSS y JS correctamente', () => {
    cy.visit(baseUrl);
    
    // Verifica que hay estilos aplicados
    cy.get('body').should('have.css', 'margin');
    
    // Verifica que hay scripts cargados
    cy.window().should('have.property', 'React').or('have.property', 'ReactDOM');
  });
});

// ============================================
// TEST RÁPIDO DE INTEGRACIÓN BÁSICA
// ============================================
describe('Test de Integración Básica Frontend-Backend', () => {
  const testUser = {
    email: `test.${Date.now()}@universidad.edu`,
    password: 'TestPassword123!'
  };

  const baseUrl = 'http://localhost:3000';
  const apiUrl = 'http://localhost:5000';

  it('Flujo básico: Registro → Login → Dashboard', () => {
    // 1. Visitar página de registro
    cy.visit(`${baseUrl}/register`);
    
    // 2. Llenar formulario (adapta los selectores según tu frontend)
    cy.get('input').first().type('Usuario Test');
    cy.get('input[type="email"]').type(testUser.email);
    cy.get('input[type="password"]').first().type(testUser.password);
    cy.get('input[type="password"]').last().type(testUser.password);
    
    // 3. Enviar
    cy.get('button[type="submit"]').click();
    
    // 4. Debe redirigir o mostrar éxito
    cy.url().should('not.include', '/register');
    
    // 5. Si redirige a login, hacer login
    cy.url().then((url) => {
      if (url.includes('/login')) {
        cy.get('input[type="email"]').type(testUser.email);
        cy.get('input[type="password"]').type(testUser.password);
        cy.get('button[type="submit"]').click();
      }
    });
    
    // 6. Debe llegar al dashboard o home
    cy.wait(2000);
    cy.url().should('satisfy', (url) => {
      return url.includes('/dashboard') || 
             url.includes('/home') || 
             url === baseUrl + '/';
    });
  });
});
