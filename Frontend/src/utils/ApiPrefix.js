import axios from 'axios';
import AuthService from '../services/AuthService';

class ApiPrefix {
  constructor() {
    this.api = axios.create({
      baseURL: import.meta.env.VITE_APP_API_URL || 'http://localhost:8080/api/v1',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    // 请求拦截器 - 添加认证令牌到每个请求
    this.api.interceptors.request.use(
      config => {
        const token = AuthService.getToken();
        if (token) {
          // 将token添加到Authorization头部
          config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
      },
      error => {
        return Promise.reject(error);
      }
    );

    // 响应拦截器 - 处理认证失败等情况
    this.api.interceptors.response.use(
      response => response,
      error => {
        if (error.response && error.response.status === 401) {
          AuthService.logout();
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // 基本HTTP方法封装
  async get(url, params = {}) {
    try {
      const response = await this.api.get(url, { params });
      return response.data;
    } catch (error) {
      this._handleError(error);
      throw error;
    }
  }

  async post(url, data = {}) {
    try {
      const response = await this.api.post(url, data);
      return response.data;
    } catch (error) {
      this._handleError(error);
      throw error;
    }
  }

  async put(url, data = {}) {
    try {
      const response = await this.api.put(url, data);
      return response.data;
    } catch (error) {
      this._handleError(error);
      throw error;
    }
  }

  async patch(url, data = {}) {
    try {
      const response = await this.api.patch(url, data);
      return response.data;
    } catch (error) {
      this._handleError(error);
      throw error;
    }
  }

  async delete(url, params = {}) {
    try {
      const response = await this.api.delete(url, { params });
      return response.data;
    } catch (error) {
      this._handleError(error);
      throw error;
    }
  }

  // 错误处理
  _handleError(error) {
    console.error('API请求错误:', error);
    if (error.response && error.response.status === 401) {
      AuthService.logout();
      window.location.href = '/login';
    }
  }
}

export default ApiPrefix;
