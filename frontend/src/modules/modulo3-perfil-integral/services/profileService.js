// frontend/src/modules/modulo3-perfil-integral/services/profileService.js
// Servicio para interactuar con endpoints de perfil

import api from '../../../services/api';

const profileService = {
  /**
   * Obtiene el perfil del estudiante
   * @param {number} userId - ID del usuario
   * @returns {Promise} Perfil del estudiante
   */
  getProfile: async (userId) => {
    try {
      const response = await api.get(`/profile/${userId}`);
      return response.data;
    } catch (error) {
      console.error('Error obteniendo perfil:', error);
      throw error;
    }
  },

  /**
   * Regenera el perfil con datos actualizados
   * @param {number} userId - ID del usuario
   * @returns {Promise} Perfil regenerado
   */
  regenerateProfile: async (userId) => {
    try {
      const response = await api.post(`/profile/${userId}/regenerate`);
      return response.data;
    } catch (error) {
      console.error('Error regenerando perfil:', error);
      throw error;
    }
  },

  /**
   * Obtiene solo las fortalezas
   * @param {number} userId - ID del usuario
   * @returns {Promise} Lista de fortalezas
   */
  getStrengths: async (userId) => {
    try {
      const response = await api.get(`/profile/${userId}/strengths`);
      return response.data;
    } catch (error) {
      console.error('Error obteniendo fortalezas:', error);
      throw error;
    }
  },

  /**
   * Obtiene solo las debilidades
   * @param {number} userId - ID del usuario
   * @returns {Promise} Lista de debilidades
   */
  getWeaknesses: async (userId) => {
    try {
      const response = await api.get(`/profile/${userId}/weaknesses`);
      return response.data;
    } catch (error) {
      console.error('Error obteniendo debilidades:', error);
      throw error;
    }
  },

  /**
   * Obtiene el score de preparación para tesis
   * @param {number} userId - ID del usuario
   * @returns {Promise} Datos de thesis readiness
   */
  getThesisReadiness: async (userId) => {
    try {
      const response = await api.get(`/profile/${userId}/thesis-readiness`);
      return response.data;
    } catch (error) {
      console.error('Error obteniendo thesis readiness:', error);
      throw error;
    }
  },

  /**
   * Obtiene recomendaciones personalizadas
   * @param {number} userId - ID del usuario
   * @returns {Promise} Lista de recomendaciones
   */
  getRecommendations: async (userId) => {
    try {
      const response = await api.get(`/profile/${userId}/recommendations`);
      return response.data;
    } catch (error) {
      console.error('Error obteniendo recomendaciones:', error);
      throw error;
    }
  },
};

export default profileService;