// frontend/src/modules/modulo4-reportes-personalizados/services/reportService.js
// Servicio para generación y gestión de reportes

import api from '../../../services/api';

const reportService = {
  /**
   * Genera un reporte completo (PPT + DOCX + PDF)
   * @param {number} userId - ID del usuario
   * @param {string} reportType - Tipo de reporte (integral, semestral, curso)
   * @param {boolean} includePpt - Incluir PowerPoint
   * @param {boolean} includeDocx - Incluir Word
   * @returns {Promise} Información de archivos generados
   */
  generateReport: async (userId, reportType = 'integral', includePpt = true, includeDocx = true) => {
    try {
      const response = await api.post('/reports/generate', {
        user_id: userId,
        report_type: reportType,
        include_ppt: includePpt,
        include_docx: includeDocx,
      });
      return response.data;
    } catch (error) {
      console.error('Error generando reporte:', error);
      throw error;
    }
  },

  /**
   * Obtiene información de un reporte específico
   * @param {number} reportId - ID del reporte
   * @returns {Promise} Datos del reporte
   */
  getReport: async (reportId) => {
    try {
      const response = await api.get(`/reports/${reportId}`);
      return response.data;
    } catch (error) {
      console.error('Error obteniendo reporte:', error);
      throw error;
    }
  },

  /**
   * Lista todos los reportes de un usuario
   * @param {number} userId - ID del usuario
   * @param {number} limit - Número máximo de reportes
   * @returns {Promise} Lista de reportes
   */
  getUserReports: async (userId, limit = 10) => {
    try {
      const response = await api.get(`/reports/user/${userId}`, {
        params: { limit },
      });
      return response.data;
    } catch (error) {
      console.error('Error obteniendo reportes del usuario:', error);
      throw error;
    }
  },

  /**
   * Genera una plantilla PowerPoint personalizada
   * @param {number} userId - ID del usuario
   * @param {string} topic - Tema de la presentación
   * @param {number} slidesCount - Número de slides
   * @param {string} style - Estilo (academic, professional, creative)
   * @returns {Promise} Información del archivo generado
   */
  generatePptTemplate: async (userId, topic, slidesCount = 10, style = 'academic') => {
    try {
      const response = await api.post('/reports/template/ppt', {
        user_id: userId,
        topic,
        slides_count: slidesCount,
        style,
      });
      return response.data;
    } catch (error) {
      console.error('Error generando plantilla PPT:', error);
      throw error;
    }
  },

  /**
   * Genera una plantilla Word personalizada
   * @param {number} userId - ID del usuario
   * @param {string} topic - Tema del documento
   * @param {string} documentType - Tipo (informe, ensayo, monografia)
   * @returns {Promise} Información del archivo generado
   */
  generateDocxTemplate: async (userId, topic, documentType = 'informe') => {
    try {
      const response = await api.post('/reports/template/docx', {
        user_id: userId,
        topic,
        document_type: documentType,
      });
      return response.data;
    } catch (error) {
      console.error('Error generando plantilla DOCX:', error);
      throw error;
    }
  },

  /**
   * Obtiene datos de visualización para gráficos
   * @param {number} userId - ID del usuario
   * @returns {Promise} Datos para Chart.js
   */
  getVisualizationData: async (userId) => {
    try {
      const response = await api.get(`/reports/visualizations/${userId}`);
      return response.data;
    } catch (error) {
      console.error('Error obteniendo datos de visualización:', error);
      throw error;
    }
  },

  /**
   * Descarga un archivo de reporte/plantilla
   * @param {number} templateId - ID de la plantilla
   * @returns {string} URL de descarga
   */
  getDownloadUrl: (templateId) => {
    return `${api.defaults.baseURL}/reports/download/template/${templateId}`;
  },

  /**
   * Lista plantillas de un usuario
   * @param {number} userId - ID del usuario
   * @param {string} type - Tipo de plantilla (ppt, docx, pdf)
   * @returns {Promise} Lista de plantillas
   */
  getUserTemplates: async (userId, type = null) => {
    try {
      const params = type ? { type } : {};
      const response = await api.get(`/reports/templates/user/${userId}`, { params });
      return response.data;
    } catch (error) {
      console.error('Error obteniendo plantillas:', error);
      throw error;
    }
  },
};

export default reportService;