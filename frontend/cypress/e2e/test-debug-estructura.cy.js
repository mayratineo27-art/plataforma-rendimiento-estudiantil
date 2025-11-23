// cypress/e2e/test-debug-estructura.cy.js
// Test de DEBUG - Para entender la estructura de tu frontend

describe('🔍 DEBUG: Inspeccionar Estructura del Frontend', () => {
  const baseUrl = 'http://localhost:3000';
  const apiUrl = 'http://localhost:5000';

  beforeEach(() => {
    cy.on('uncaught:exception', () => false);
  });

  it('1. Verificar que backend está corriendo', () => {
    cy.request({
      url: `${apiUrl}/api/health`,
      failOnStatusCode: false
    }).then((response) => {
      cy.log('Estado del backend: ' + response.status);
      if (response.status === 200) {
        cy.log('✅ Backend funcionando correctamente');
      } else {
        cy.log('⚠️ Backend no responde en /api/health');
      }
    });
  });

  it('2. Cargar página principal y ver qué hay', () => {
    cy.visit(baseUrl);
    cy.wait(2000);
    
    cy.log('=== INSPECCIONANDO PÁGINA PRINCIPAL ===');
    
    // Ver URL actual
    cy.url().then((url) => {
      cy.log('URL actual: ' + url);
    });
    
    // Ver título
    cy.title().then((title) => {
      cy.log('Título: ' + title);
    });
    
    // Listar todos los links
    cy.get('a').then(($links) => {
      cy.log(`📎 Se encontraron ${$links.length} links`);
      $links.each((i, link) => {
        cy.log(`  ${i + 1}. "${link.textContent.trim()}" → ${link.href}`);
      });
    });
    
    // Listar todos los botones
    cy.get('button').then(($buttons) => {
      cy.log(`🔘 Se encontraron ${$buttons.length} botones`);
      $buttons.each((i, button) => {
        cy.log(`  ${i + 1}. "${button.textContent.trim()}"`);
      });
    });
    
    // Verificar si hay formularios
    cy.get('form').then(($forms) => {
      cy.log(`📝 Se encontraron ${$forms.length} formularios`);
    });
    
    // Verificar inputs
    cy.get('input').then(($inputs) => {
      cy.log(`📋 Se encontraron ${$inputs.length} inputs`);
      $inputs.each((i, input) => {
        cy.log(`  ${i + 1}. type="${input.type}" name="${input.name}" placeholder="${input.placeholder}"`);
      });
    });
  });

  it('3. Intentar encontrar página de login', () => {
    cy.log('=== BUSCANDO PÁGINA DE LOGIN ===');
    
    // Estrategia 1: Buscar link que contenga "login"
    cy.visit(baseUrl);
    cy.wait(1000);
    
    cy.get('body').then(($body) => {
      const loginLink = $body.find('a').filter((i, el) => {
        return /login|ingresar|entrar|sign in/i.test(el.textContent);
      });
      
      if (loginLink.length > 0) {
        cy.log('✅ Encontrado link de login: ' + loginLink.first().text());
        cy.wrap(loginLink).first().click();
        cy.wait(1000);
        cy.url().then((url) => cy.log('URL después de click: ' + url));
      } else {
        cy.log('⚠️ No se encontró link de login visible');
      }
    });
    
    // Estrategia 2: Intentar ir directo a /login
    cy.visit(`${baseUrl}/login`, { failOnStatusCode: false });
    cy.wait(1000);
    
    cy.url().then((url) => {
      if (url.includes('/login')) {
        cy.log('✅ Página /login existe');
        
        // Analizar la página de login
        cy.get('input').then(($inputs) => {
          cy.log(`📋 Inputs en página de login: ${$inputs.length}`);
          $inputs.each((i, input) => {
            cy.log(`  ${i + 1}. type="${input.type}" name="${input.name}"`);
          });
        });
        
        cy.get('button').then(($buttons) => {
          cy.log(`🔘 Botones en página de login: ${$buttons.length}`);
          $buttons.each((i, button) => {
            cy.log(`  ${i + 1}. "${button.textContent.trim()}"`);
          });
        });
      } else {
        cy.log('⚠️ /login no existe o redirige a: ' + url);
      }
    });
  });

  it('4. Intentar encontrar página de registro', () => {
    cy.log('=== BUSCANDO PÁGINA DE REGISTRO ===');
    
    // Estrategia 1: Buscar link de registro
    cy.visit(baseUrl);
    cy.wait(1000);
    
    cy.get('body').then(($body) => {
      const registerLink = $body.find('a, button').filter((i, el) => {
        return /registr|sign up|crear cuenta/i.test(el.textContent);
      });
      
      if (registerLink.length > 0) {
        cy.log('✅ Encontrado link de registro: ' + registerLink.first().text());
        cy.wrap(registerLink).first().click();
        cy.wait(1000);
        cy.url().then((url) => cy.log('URL después de click: ' + url));
      } else {
        cy.log('⚠️ No se encontró link de registro visible');
      }
    });
    
    // Estrategia 2: Intentar ir directo a /register
    cy.visit(`${baseUrl}/register`, { failOnStatusCode: false });
    cy.wait(1000);
    
    cy.url().then((url) => {
      if (url.includes('/register')) {
        cy.log('✅ Página /register existe');
        
        // Analizar la página de registro
        cy.get('input').then(($inputs) => {
          cy.log(`📋 Inputs en página de registro: ${$inputs.length}`);
          $inputs.each((i, input) => {
            cy.log(`  ${i + 1}. type="${input.type}" name="${input.name}" placeholder="${input.placeholder}"`);
          });
        });
      } else {
        cy.log('⚠️ /register no existe o redirige a: ' + url);
      }
    });
  });

  it('5. Mapear todas las rutas disponibles', () => {
    cy.log('=== MAPEANDO RUTAS DISPONIBLES ===');
    
    const rutasComunes = [
      '/',
      '/home',
      '/dashboard',
      '/login',
      '/register',
      '/analisis-progreso',
      '/sesion-tiempo-real',
      '/perfil',
      '/reportes'
    ];
    
    rutasComunes.forEach((ruta) => {
      cy.request({
        url: `${baseUrl}${ruta}`,
        failOnStatusCode: false
      }).then((response) => {
        const status = response.status;
        const emoji = status === 200 ? '✅' : status === 404 ? '❌' : '⚠️';
        cy.log(`${emoji} ${ruta} → ${status}`);
      });
    });
  });

  it('6. Verificar data-testids disponibles', () => {
    cy.log('=== VERIFICANDO DATA-TESTIDS ===');
    
    cy.visit(baseUrl);
    cy.wait(1000);
    
    cy.get('[data-testid]').then(($elements) => {
      if ($elements.length > 0) {
        cy.log(`✅ Se encontraron ${$elements.length} elementos con data-testid:`);
        $elements.each((i, el) => {
          cy.log(`  ${i + 1}. data-testid="${el.getAttribute('data-testid')}" (${el.tagName})`);
        });
      } else {
        cy.log('⚠️ No se encontraron elementos con data-testid');
        cy.log('Necesitas agregar data-testid a tus componentes');
      }
    });
    
    // Intentar en /login
    cy.visit(`${baseUrl}/login`, { failOnStatusCode: false });
    cy.wait(1000);
    
    cy.get('[data-testid]').then(($elements) => {
      if ($elements.length > 0) {
        cy.log(`✅ En /login hay ${$elements.length} elementos con data-testid:`);
        $elements.each((i, el) => {
          cy.log(`  ${i + 1}. data-testid="${el.getAttribute('data-testid')}" (${el.tagName})`);
        });
      } else {
        cy.log('⚠️ En /login no hay elementos con data-testid');
      }
    });
  });

  it('7. Generar reporte de estructura', () => {
    cy.log('=================================================');
    cy.log('📊 REPORTE DE ESTRUCTURA DEL FRONTEND');
    cy.log('=================================================');
    
    cy.visit(baseUrl);
    cy.wait(2000);
    
    // Resumen general
    cy.get('a').its('length').then((links) => {
      cy.log(`Links totales: ${links}`);
    });
    
    cy.get('button').its('length').then((buttons) => {
      cy.log(`Botones totales: ${buttons}`);
    });
    
    cy.get('input').its('length').then((inputs) => {
      cy.log(`Inputs totales: ${inputs}`);
    });
    
    cy.get('[data-testid]').its('length').then((testids) => {
      cy.log(`Elementos con data-testid: ${testids}`);
    });
    
    cy.log('=================================================');
    cy.log('💡 RECOMENDACIONES:');
    
    cy.get('[data-testid]').then(($elements) => {
      if ($elements.length === 0) {
        cy.log('1. Agrega data-testid a tus componentes React');
        cy.log('2. Ejemplo: <button data-testid="btn-login">Login</button>');
      } else {
        cy.log('1. ✅ Ya tienes algunos data-testid');
        cy.log('2. Asegúrate de que todos los componentes críticos los tengan');
      }
    });
    
    cy.log('=================================================');
  });
});
