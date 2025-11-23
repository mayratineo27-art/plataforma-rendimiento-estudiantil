// cypress/e2e/test-completo-frontend.cy.js
// Test End-to-End Completo - Plataforma Integral de Rendimiento Estudiantil

describe('Test Completo de la Plataforma - 4 Módulos', () => {
  const testUser = {
    email: 'estudiante.test@universidad.edu',
    password: 'TestPassword123!',
    nombre: 'Juan Pérez'
  };

  const baseUrl = 'http://localhost:3000'; // Puerto de React
  const apiUrl = 'http://localhost:5000';  // Puerto de Flask

  before(() => {
    // Setup: Limpiar datos de prueba si existen
    cy.request('POST', `${apiUrl}/api/test/cleanup`, { email: testUser.email });
  });

  beforeEach(() => {
    cy.visit(baseUrl);
  });

  // ============================================
  // FASE 1: AUTENTICACIÓN
  // ============================================
  describe('Fase 1: Autenticación y Registro', () => {
    it('Debe registrar un nuevo estudiante y hacer login', () => {
      // Ir a registro
      cy.contains('Registrarse').click();
      cy.url().should('include', '/register');

      // Llenar formulario de registro
      cy.get('[data-testid="input-nombre"]').type(testUser.nombre);
      cy.get('[data-testid="input-email"]').type(testUser.email);
      cy.get('[data-testid="input-password"]').type(testUser.password);
      cy.get('[data-testid="input-confirm-password"]').type(testUser.password);
      
      // Enviar formulario
      cy.get('[data-testid="btn-registrar"]').click();

      // Verificar redirección al dashboard
      cy.url().should('include', '/dashboard', { timeout: 10000 });
      cy.contains(testUser.nombre).should('be.visible');
    });
  });

  // ============================================
  // FASE 2: MÓDULO 1 - ANÁLISIS DE PROGRESO ACADÉMICO
  // ============================================
  describe('Fase 2: Módulo 1 - Análisis de Documentos', () => {
    beforeEach(() => {
      // Login antes de cada test
      cy.visit(`${baseUrl}/login`);
      cy.get('[data-testid="input-email"]').type(testUser.email);
      cy.get('[data-testid="input-password"]').type(testUser.password);
      cy.get('[data-testid="btn-login"]').click();
      cy.url().should('include', '/dashboard');
    });

    it('Debe subir un documento PDF y mostrar análisis de progreso', () => {
      // Navegar al módulo 1
      cy.get('[data-testid="nav-analisis-progreso"]').click();
      cy.url().should('include', '/analisis-progreso');

      // Subir documento de prueba
      cy.get('[data-testid="input-file-upload"]').attachFile('documento-prueba.pdf');
      
      // Seleccionar semestre
      cy.get('[data-testid="select-semestre"]').select('5');
      
      // Iniciar análisis
      cy.get('[data-testid="btn-analizar-documento"]').click();

      // Verificar que muestra loading
      cy.get('[data-testid="loading-analysis"]').should('be.visible');

      // Esperar resultados (máximo 30 segundos)
      cy.get('[data-testid="dashboard-progreso"]', { timeout: 30000 }).should('be.visible');

      // Verificar métricas visibles
      cy.get('[data-testid="metric-vocabulario"]').should('exist');
      cy.get('[data-testid="metric-complejidad"]').should('exist');
      cy.get('[data-testid="metric-coherencia"]').should('exist');

      // Verificar que hay un gráfico
      cy.get('[data-testid="chart-progreso"]').should('be.visible');

      // Guardar análisis
      cy.get('[data-testid="btn-guardar-analisis"]').click();
      cy.contains('Análisis guardado correctamente').should('be.visible');
    });

    it('Debe comparar documentos de diferentes semestres', () => {
      cy.get('[data-testid="nav-analisis-progreso"]').click();

      // Subir segundo documento
      cy.get('[data-testid="input-file-upload"]').attachFile('documento-prueba-2.pdf');
      cy.get('[data-testid="select-semestre"]').select('6');
      cy.get('[data-testid="btn-analizar-documento"]').click();

      // Esperar y guardar
      cy.get('[data-testid="dashboard-progreso"]', { timeout: 30000 }).should('be.visible');
      cy.get('[data-testid="btn-guardar-analisis"]').click();

      // Ir a comparación
      cy.get('[data-testid="tab-comparacion"]').click();
      
      // Seleccionar documentos para comparar
      cy.get('[data-testid="select-doc-1"]').select('Semestre 5');
      cy.get('[data-testid="select-doc-2"]').select('Semestre 6');
      cy.get('[data-testid="btn-comparar"]').click();

      // Verificar visualización de comparación
      cy.get('[data-testid="chart-comparacion"]', { timeout: 15000 }).should('be.visible');
      cy.contains('Mejora detectada').should('exist');
    });
  });

  // ============================================
  // FASE 3: MÓDULO 2 - INTERACCIÓN EN TIEMPO REAL
  // ============================================
  describe('Fase 3: Módulo 2 - Video y Audio en Tiempo Real', () => {
    beforeEach(() => {
      cy.visit(`${baseUrl}/login`);
      cy.get('[data-testid="input-email"]').type(testUser.email);
      cy.get('[data-testid="input-password"]').type(testUser.password);
      cy.get('[data-testid="btn-login"]').click();
    });

    it('Debe iniciar sesión de análisis con cámara y micrófono', () => {
      // Navegar al módulo 2
      cy.get('[data-testid="nav-sesion-tiempo-real"]').click();
      cy.url().should('include', '/sesion-tiempo-real');

      // Stub de permisos de cámara y micrófono
      cy.window().then((win) => {
        cy.stub(win.navigator.mediaDevices, 'getUserMedia')
          .resolves({
            getTracks: () => [{ stop: () => {} }],
            getVideoTracks: () => [{ stop: () => {} }],
            getAudioTracks: () => [{ stop: () => {} }]
          });
      });

      // Iniciar sesión
      cy.get('[data-testid="btn-iniciar-sesion"]').click();

      // Verificar que se solicitaron permisos
      cy.get('[data-testid="status-permisos"]')
        .should('contain', 'Cámara y micrófono activados');

      // Verificar preview de video
      cy.get('[data-testid="video-preview"]').should('be.visible');

      // Verificar indicador de audio
      cy.get('[data-testid="audio-indicator"]').should('be.visible');
    });

    it('Debe capturar y analizar emociones durante la sesión', () => {
      cy.get('[data-testid="nav-sesion-tiempo-real"]').click();

      // Stub de getUserMedia
      cy.window().then((win) => {
        cy.stub(win.navigator.mediaDevices, 'getUserMedia')
          .resolves({
            getTracks: () => [{ stop: () => {} }],
            getVideoTracks: () => [{ stop: () => {} }],
            getAudioTracks: () => [{ stop: () => {} }]
          });
      });

      cy.get('[data-testid="btn-iniciar-sesion"]').click();

      // Esperar 5 segundos de "grabación"
      cy.wait(5000);

      // Verificar que se muestran emociones detectadas en tiempo real
      cy.get('[data-testid="emotion-display"]').should('be.visible');
      cy.get('[data-testid="attention-meter"]').should('be.visible');

      // Detener sesión
      cy.get('[data-testid="btn-detener-sesion"]').click();

      // Verificar que muestra resumen
      cy.get('[data-testid="sesion-summary"]', { timeout: 15000 }).should('be.visible');
      cy.get('[data-testid="timeline-emociones"]').should('exist');
    });

    it('Debe transcribir audio correctamente (>70%)', () => {
      cy.get('[data-testid="nav-sesion-tiempo-real"]').click();

      // Stub de getUserMedia con audio de prueba
      cy.window().then((win) => {
        cy.stub(win.navigator.mediaDevices, 'getUserMedia')
          .resolves({
            getTracks: () => [{ stop: () => {} }],
            getVideoTracks: () => [{ stop: () => {} }],
            getAudioTracks: () => [{ stop: () => {} }]
          });
      });

      cy.get('[data-testid="btn-iniciar-sesion"]').click();
      cy.wait(5000);
      cy.get('[data-testid="btn-detener-sesion"]').click();

      // Verificar transcripción
      cy.get('[data-testid="transcripcion-display"]', { timeout: 20000 })
        .should('be.visible');

      // Verificar que muestra porcentaje de precisión
      cy.get('[data-testid="transcription-accuracy"]')
        .invoke('text')
        .then((text) => {
          const accuracy = parseInt(text.match(/\d+/)[0]);
          expect(accuracy).to.be.greaterThan(70);
        });
    });
  });

  // ============================================
  // FASE 4: MÓDULO 3 - PERFIL INTEGRAL
  // ============================================
  describe('Fase 4: Módulo 3 - Perfil Integral del Estudiante', () => {
    beforeEach(() => {
      cy.visit(`${baseUrl}/login`);
      cy.get('[data-testid="input-email"]').type(testUser.email);
      cy.get('[data-testid="input-password"]').type(testUser.password);
      cy.get('[data-testid="btn-login"]').click();
    });

    it('Debe mostrar perfil consolidado con datos de Módulos 1 y 2', () => {
      // Navegar al perfil
      cy.get('[data-testid="nav-perfil"]').click();
      cy.url().should('include', '/perfil');

      // Verificar secciones del perfil
      cy.get('[data-testid="section-fortalezas"]').should('be.visible');
      cy.get('[data-testid="section-debilidades"]').should('be.visible');
      cy.get('[data-testid="section-estilo-aprendizaje"]').should('be.visible');

      // Verificar que hay datos de análisis de documentos
      cy.get('[data-testid="resumen-documentos"]')
        .should('contain', 'documentos analizados');

      // Verificar que hay datos de sesiones de video
      cy.get('[data-testid="resumen-sesiones"]')
        .should('contain', 'sesiones completadas');

      // Verificar gráficos de evolución
      cy.get('[data-testid="chart-evolucion-global"]').should('be.visible');
    });

    it('Debe identificar fortalezas y debilidades específicas', () => {
      cy.get('[data-testid="nav-perfil"]').click();

      // Verificar lista de fortalezas
      cy.get('[data-testid="list-fortalezas"]')
        .find('[data-testid^="fortaleza-"]')
        .should('have.length.at.least', 1);

      // Verificar lista de debilidades
      cy.get('[data-testid="list-debilidades"]')
        .find('[data-testid^="debilidad-"]')
        .should('have.length.at.least', 1);

      // Verificar recomendaciones
      cy.get('[data-testid="recomendaciones-ia"]')
        .should('be.visible')
        .and('not.be.empty');
    });

    it('Debe determinar estilo de aprendizaje preferido', () => {
      cy.get('[data-testid="nav-perfil"]').click();

      // Verificar que muestra estilo de aprendizaje
      cy.get('[data-testid="estilo-aprendizaje"]')
        .should('be.visible')
        .and('contain.oneOf', ['Visual', 'Auditivo', 'Kinestésico', 'Lectura/Escritura']);

      // Verificar porcentaje de confianza
      cy.get('[data-testid="confidence-level"]')
        .invoke('text')
        .then((text) => {
          const confidence = parseInt(text.match(/\d+/)[0]);
          expect(confidence).to.be.within(0, 100);
        });
    });
  });

  // ============================================
  // FASE 5: MÓDULO 4 - REPORTES PERSONALIZADOS
  // ============================================
  describe('Fase 5: Módulo 4 - Generación de Reportes', () => {
    beforeEach(() => {
      cy.visit(`${baseUrl}/login`);
      cy.get('[data-testid="input-email"]').type(testUser.email);
      cy.get('[data-testid="input-password"]').type(testUser.password);
      cy.get('[data-testid="btn-login"]').click();
    });

    it('Debe generar reporte semestral en PDF', () => {
      // Navegar a reportes
      cy.get('[data-testid="nav-reportes"]').click();
      cy.url().should('include', '/reportes');

      // Seleccionar tipo de reporte
      cy.get('[data-testid="select-tipo-reporte"]').select('Semestral');
      
      // Seleccionar semestre
      cy.get('[data-testid="select-semestre-reporte"]').select('5');

      // Generar reporte
      cy.get('[data-testid="btn-generar-reporte"]').click();

      // Verificar loading
      cy.get('[data-testid="loading-reporte"]').should('be.visible');

      // Esperar generación (máximo 30 segundos)
      cy.get('[data-testid="btn-descargar-reporte"]', { timeout: 30000 })
        .should('be.visible')
        .and('not.be.disabled');

      // Verificar preview del reporte
      cy.get('[data-testid="preview-reporte"]').should('be.visible');
      
      // Verificar que incluye gráficos
      cy.get('[data-testid="reporte-charts"]').should('exist');
    });

    it('Debe generar presentación PowerPoint personalizada', () => {
      cy.get('[data-testid="nav-reportes"]').click();

      // Seleccionar generación de PPT
      cy.get('[data-testid="tab-plantillas"]').click();
      
      // Seleccionar tema
      cy.get('[data-testid="input-tema-ppt"]')
        .type('Metodología de Investigación Científica');

      // Seleccionar debilidad a trabajar
      cy.get('[data-testid="select-debilidad"]')
        .select('Estructura de capítulos');

      // Configurar personalización
      cy.get('[data-testid="checkbox-incluir-imagenes"]').check();
      cy.get('[data-testid="slider-nivel-detalle"]').invoke('val', 70).trigger('change');

      // Generar presentación
      cy.get('[data-testid="btn-generar-ppt"]').click();

      // Esperar generación
      cy.get('[data-testid="btn-descargar-ppt"]', { timeout: 40000 })
        .should('be.visible');

      // Verificar preview de diapositivas
      cy.get('[data-testid="slide-preview"]')
        .find('[data-testid^="slide-"]')
        .should('have.length.at.least', 5);
    });

    it('Debe adaptar contenido según estilo de aprendizaje', () => {
      cy.get('[data-testid="nav-reportes"]').click();
      cy.get('[data-testid="tab-plantillas"]').click();

      // Verificar que muestra el estilo de aprendizaje detectado
      cy.get('[data-testid="info-estilo-aprendizaje"]')
        .should('be.visible')
        .and('contain', 'estilo de aprendizaje');

      // Generar con adaptación automática
      cy.get('[data-testid="input-tema-ppt"]').type('Análisis Estadístico');
      cy.get('[data-testid="checkbox-adaptar-estilo"]').should('be.checked');
      cy.get('[data-testid="btn-generar-ppt"]').click();

      // Esperar generación
      cy.get('[data-testid="slide-preview"]', { timeout: 40000 }).should('be.visible');

      // Verificar que el contenido está adaptado
      // (si el estilo es Visual, debe tener muchas imágenes)
      cy.get('[data-testid="content-adaptation-info"]')
        .should('contain', 'adaptado a tu estilo');
    });

    it('Debe permitir descargar múltiples formatos', () => {
      cy.get('[data-testid="nav-reportes"]').click();

      // Generar reporte
      cy.get('[data-testid="select-tipo-reporte"]').select('Completo');
      cy.get('[data-testid="btn-generar-reporte"]').click();
      cy.get('[data-testid="btn-descargar-reporte"]', { timeout: 30000 })
        .should('be.visible');

      // Verificar opciones de descarga
      cy.get('[data-testid="dropdown-formato"]').click();
      cy.get('[data-testid="option-pdf"]').should('exist');
      cy.get('[data-testid="option-docx"]').should('exist');
      cy.get('[data-testid="option-pptx"]').should('exist');

      // Descargar en PDF
      cy.get('[data-testid="option-pdf"]').click();
      
      // Verificar que inició descarga (esperar cambio de estado del botón)
      cy.get('[data-testid="download-status"]')
        .should('contain', 'Descargando');
    });
  });

  // ============================================
  // FASE 6: INTEGRACIÓN COMPLETA
  // ============================================
  describe('Fase 6: Flujo Completo End-to-End', () => {
    it('Debe completar el ciclo completo desde registro hasta reporte', () => {
      // 1. Registro/Login
      cy.visit(`${baseUrl}/login`);
      cy.get('[data-testid="input-email"]').type(testUser.email);
      cy.get('[data-testid="input-password"]').type(testUser.password);
      cy.get('[data-testid="btn-login"]').click();
      cy.url().should('include', '/dashboard');

      // 2. Subir documento (Módulo 1)
      cy.get('[data-testid="nav-analisis-progreso"]').click();
      cy.get('[data-testid="input-file-upload"]').attachFile('documento-prueba.pdf');
      cy.get('[data-testid="select-semestre"]').select('7');
      cy.get('[data-testid="btn-analizar-documento"]').click();
      cy.get('[data-testid="btn-guardar-analisis"]', { timeout: 30000 }).click();
      cy.contains('guardado correctamente').should('be.visible');

      // 3. Sesión de video (Módulo 2)
      cy.get('[data-testid="nav-sesion-tiempo-real"]').click();
      cy.window().then((win) => {
        cy.stub(win.navigator.mediaDevices, 'getUserMedia')
          .resolves({
            getTracks: () => [{ stop: () => {} }],
            getVideoTracks: () => [{ stop: () => {} }],
            getAudioTracks: () => [{ stop: () => {} }]
          });
      });
      cy.get('[data-testid="btn-iniciar-sesion"]').click();
      cy.wait(3000);
      cy.get('[data-testid="btn-detener-sesion"]').click();
      cy.get('[data-testid="sesion-summary"]', { timeout: 15000 }).should('be.visible');

      // 4. Ver perfil actualizado (Módulo 3)
      cy.get('[data-testid="nav-perfil"]').click();
      cy.get('[data-testid="section-fortalezas"]').should('be.visible');
      cy.get('[data-testid="resumen-documentos"]')
        .should('contain', 'documentos analizados');
      cy.get('[data-testid="resumen-sesiones"]')
        .should('contain', 'sesiones completadas');

      // 5. Generar reporte final (Módulo 4)
      cy.get('[data-testid="nav-reportes"]').click();
      cy.get('[data-testid="select-tipo-reporte"]').select('Completo');
      cy.get('[data-testid="btn-generar-reporte"]').click();
      cy.get('[data-testid="btn-descargar-reporte"]', { timeout: 40000 })
        .should('be.visible');

      // Verificación final: Dashboard muestra todos los datos
      cy.get('[data-testid="nav-dashboard"]').click();
      cy.get('[data-testid="widget-progreso-academico"]').should('be.visible');
      cy.get('[data-testid="widget-sesiones-recientes"]').should('be.visible');
      cy.get('[data-testid="widget-perfil-resumen"]').should('be.visible');
      cy.get('[data-testid="widget-reportes-generados"]').should('be.visible');
    });
  });

  // ============================================
  // LIMPIEZA
  // ============================================
  after(() => {
    // Cleanup: Eliminar datos de prueba
    cy.request('POST', `${apiUrl}/api/test/cleanup`, { email: testUser.email });
  });
});