import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

class AuthService {
  isAuthenticated() {
    const token = localStorage.getItem('token');
    return !!token;
  }

  async login(credentials) {
    try {
      const response = await axios.post(`${API_URL}/auth/login`, credentials);
      if (response.data.token) {
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error en login:', error);
      return false;
    }
  }

  async checkAuth() {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        return false;
      }

      const response = await axios.get(`${API_URL}/profile/1`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      return response.data.success;
    } catch (error) {
      console.error('Error en checkAuth:', error);
      this.logout();
      return false;
    }
  }

  async register(userData) {
    try {
      const response = await axios.post(`${API_URL}/auth/register`, userData);
      return response.data.success;
    } catch (error) {
      console.error('Error en registro:', error);
      throw error;
    }
  }

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  }
}

const authService = new AuthService();
export default authService;