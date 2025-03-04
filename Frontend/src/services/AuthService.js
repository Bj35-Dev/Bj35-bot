import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

class AuthService {
  login(username, password) {

    return axios
      .post(`${import.meta.env.VITE_APP_API_URL}/login`, {
        username,
        password
      })
      .then(response => {
        if (response.data.access_token) {
          localStorage.setItem('access_token', response.data.access_token);
        }
        return response.data;
      });
  }

  logout() {
    localStorage.removeItem('access_token');
  }

  getToken() {
    return localStorage.getItem('access_token');
  }

  isAuthenticated() {
    const token = this.getToken();
    if (!token) {
      return false;
    }
    
    try {
      const decoded = jwtDecode(token);
      // 检查令牌是否过期
      const currentTime = Date.now() / 1000;
      if (decoded.exp < currentTime) {
        // 令牌已过期
        this.logout();
        return false;
      }
      return true;
    } catch (error) {
      // 解码失败
      return false;
    }
  }
}

export default new AuthService();