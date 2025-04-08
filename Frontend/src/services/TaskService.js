 // * @copyright Copyright (c) 2020-2025 The ESAP Project.
 // * @author AptS:1547
 // * @Link https://esaps.net/
 // * @version 0.1.0
 // * @license
 // * 使用本代码需遵循 GPL3.0 协议，以及 Tailwind Plus Personal 许可证
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
