import ApiPrefix from '../utils/ApiPrefix';

class DeviceService extends ApiPrefix {
  constructor() {
    super();
  }
  
  async getRobotList() {
    try {
      const data = await this.get('/robot_list');

      if (data.code !== 0) { 
        throw new Error(data.message); 
      }

      return data;
    } catch (error) {
      throw error;
    }
  }

  async getDeviceById(id) {
    try {
      const data = await this.get(`/device_status/${id}`);
      
      if (data.code !== 0) { 
        throw new Error(data.message); 
      }

      return data;
    } catch (error) {
      throw error;
    }
  }

  async getDeviceName(id) {
    try {
      const data = await this.get(`/map-position/${id}`);

      if (data.code !== 0) { 
        throw new Error(data.message); 
      }

      return data;
    } catch (error) {
      throw error;
    }
  }
}

export default new DeviceService();
