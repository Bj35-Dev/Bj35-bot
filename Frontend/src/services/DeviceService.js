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
  
  // 添加运行任务的方法
  async runRobotTask(robotId, locations) {
    try {
      const response = await this.post(`/run-task/${robotId}`, {
        locations: locations
      });
      
      if (response.code !== 0) {
        throw new Error(response.message || '任务执行失败');
      }
      
      return response.data;
    } catch (error) {
      console.error('执行机器人任务失败:', error);
      throw error;
    }
  }
}

export default new DeviceService();
