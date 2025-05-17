import ApiPrefix from '../utils/ApiPrefix';
import AuthService from './AuthService';

class UserService extends ApiPrefix {
  constructor() {
    super();
  }

  async getUserInfo() {
    try {
      const info = await this.get('/get_user_profile');
      console.log(info);
      return info;
    } catch (error) {
      throw error;
    }
  }

  async getUserAvatar() {
    try {
      const userinfo = await this.getUserInfo();
      const avatar = userinfo.avatar_url;
      console.log(avatar);
      return avatar;
    } catch (error) {
      throw error;
    }
  }
  
  async updateUserProfile(data) {
    try {
      const response = await this.post('/post_user_profile', data);
      return response;
    } catch (error) {
      throw error;
    }
  }

  async updateUserAvatar(data) {
    try {
      const response = await this.post('/post_user_avatar', data);
      return response;
    } catch (error) {
      throw error;
    }
  }
  
  async changeUserPassword(data) {
    try {
      const response = await this.post('/change-password', {
        wecom_id: data.wecom_id,
        old_password: data.old_password,
        new_password: data.new_password
      });

      if (!response.success) {
        throw new Error(response.message || '密码修改失败');
      }

      return response;
    } catch (error) {
      console.error('修改密码请求失败:', error);
      throw error;
    }
  }
  
  async sendMessage(message, username) {
    try {
      const response = await this.post('/send-message', {
        message,
        username
      });
      
      if (response.code !== 0) {
        throw new Error(response.message);
      }

      return response;
    } catch (error) {
      throw error;
    }
  }
}

export default new UserService();
