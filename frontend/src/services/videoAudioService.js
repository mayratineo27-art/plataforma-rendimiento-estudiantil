import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export const videoAudioService = {
  // Video endpoints
  async startSession(userId, sessionName = 'Sesión de estudio') {
    const response = await axios.post(`${API_URL}/video/session/start`, {
      user_id: userId,
      session_name: sessionName,
      session_type: 'estudio'
    });
    return response.data;
  },

  async analyzeFrame(sessionId, frameBase64, timestamp = 0) {
    const response = await axios.post(`${API_URL}/video/analyze-frame`, {
      session_id: sessionId,
      frame_base64: frameBase64,
      timestamp_seconds: timestamp,
      frame_number: Math.floor(timestamp * 2)
    });
    return response.data;
  },

  async endSession(sessionId) {
    const response = await axios.post(`${API_URL}/video/session/end`, {
      session_id: sessionId
    });
    return response.data;
  },

  async getSessionAnalysis(sessionId) {
    const response = await axios.get(`${API_URL}/video/session/${sessionId}/analysis`);
    return response.data;
  },

  async getAttentionMetrics(sessionId) {
    const response = await axios.get(`${API_URL}/video/session/${sessionId}/attention`);
    return response.data;
  },

  // Audio endpoints
  async transcribeAudio(audioBlob, sessionId, userId) {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'audio.webm');
    formData.append('session_id', sessionId);
    formData.append('user_id', userId);

    const response = await axios.post(`${API_URL}/audio/transcribe`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  },

  async getTranscriptions(sessionId) {
    const response = await axios.get(`${API_URL}/audio/session/${sessionId}/transcriptions`);
    return response.data;
  },

  async generateSummary(sessionId) {
    const response = await axios.post(`${API_URL}/audio/session/${sessionId}/summary`);
    return response.data;
  }
};
