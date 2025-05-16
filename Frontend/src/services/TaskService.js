import ApiPrefix from '../utils/ApiPrefix';

class TaskService extends ApiPrefix {
  constructor() {
    super();
  }
  
  async getTasklist() {
    try {
      const data = await this.get(`/school-tasks/100/1`);

      if (data.code !== 0) {
        throw new Error(data.message);
      }

      return data.data;
    } catch (error) {
      throw error;
    }
  }
  
  async getTargetlist() {
    try {
      const targetlist = await this.get('/target-list');
      return targetlist;
    } catch (error) {
      throw error;
    }
  }
}

export default new TaskService();
