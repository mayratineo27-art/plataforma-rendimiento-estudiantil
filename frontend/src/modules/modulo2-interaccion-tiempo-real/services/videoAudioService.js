// frontend/src/modules/modulo2-interaccion-tiempo-real/services/videoAudioService.js
// Servicio CORREGIDO para video/audio

import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Crear instancia de axios con configuración correcta
const api = axios.create({
  baseURL: `${API_URL}/api`, // ← Solo /api UNA VEZ
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

const videoAudioService = {
  /**
   * Inicia una nueva sesión de video/audio
   */
  startSession: async (userId) => {
    try {
      const response = await api.post('/video/session/start', {
        user_id: userId,
        session_name: 'Sesión de Video/Audio',
        session_type: 'estudio'
      });
      
      console.log('✅ Sesión iniciada:', response.data);
      return response.data;
    } catch (error) {
      console.error('❌ Error iniciando sesión:', error);
      console.error('URL intentada:', error.config?.url);
      console.error('Respuesta:', error.response?.data);
      throw error;
    }
  },

  /**
   * Envía un frame de video para análisis
   */
  analyzeFrame: async (sessionId, frameBase64) => {
    try {
      // Convertir base64 a blob
      const byteString = atob(frameBase64.split(',')[1]);
      const mimeString = frameBase64.split(',')[0].split(':')[1].split(';')[0];
      const ab = new ArrayBuffer(byteString.length);
      const ia = new Uint8Array(ab);
      for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
      }
      const blob = new Blob([ab], { type: mimeString });

      // Crear FormData
      const formData = new FormData();
      formData.append('frame', blob, 'frame.jpg');
      formData.append('session_id', sessionId);
      formData.append('timestamp', Date.now() / 1000);

      const response = await api.post('/video/analyze-frame', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      return response.data;
    } catch (error) {
      console.error('Error analizando frame:', error);
      throw error;
    }
  },

  /**
   * Envía audio para transcripción
   */
  transcribeAudio: async (sessionId, audioBlob) => {
    try {
      const formData = new FormData();
      formData.append('audio', audioBlob, 'audio.webm');
      formData.append('session_id', sessionId);
      formData.append('start_time', Date.now() / 1000);
      formData.append('end_time', (Date.now() / 1000) + 10);

      const response = await api.post('/audio/transcribe', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      return response.data;
    } catch (error) {
      console.error('Error transcribiendo audio:', error);
      throw error;
    }
  },

  /**
   * Finaliza una sesión
   */
  endSession: async (sessionId) => {
    try {
      const response = await api.post('/video/session/end', {
        session_id: sessionId
      });
      return response.data;
    } catch (error) {
      console.error('Error finalizando sesión:', error);
      throw error;
    }
  },

  /**
   * Obtiene el análisis completo
   */
  getSessionAnalysis: async (sessionId) => {
    try {
      const response = await api.get(`/video/session/${sessionId}/analysis`);
      return response.data;
    } catch (error) {
      console.error('Error obteniendo análisis:', error);
      throw error;
    }
  },

  /**
   * Obtiene métricas de atención
   */
  getAttentionMetrics: async (sessionId) => {
    try {
      const response = await api.get(`/video/session/${sessionId}/attention`);
      return response.data;
    } catch (error) {
      console.error('Error obteniendo métricas:', error);
      throw error;
    }
  },

  /**
   * Obtiene historial de sesiones
   */
  getUserSessions: async (userId, limit = 10) => {
    try {
      const response = await api.get(`/video/sessions/${userId}`, {
        params: { limit }
      });
      return response.data;
    } catch (error) {
      console.error('Error obteniendo sesiones:', error);
      throw error;
    }
  }
};

export default videoAudioService;