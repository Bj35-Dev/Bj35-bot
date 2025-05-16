import UserService from './UserService';
import DeviceService from './DeviceService';
import TaskService from './TaskService';

// 为了保持兼容性，我们可以导出一个统一的 API 服务对象
export default {
  // 用户相关服务
  getUserInfo: UserService.getUserInfo.bind(UserService),
  getUserAvatar: UserService.getUserAvatar.bind(UserService),
  updateUserProfile: UserService.updateUserProfile.bind(UserService),
  updateUserAvatar: UserService.updateUserAvatar.bind(UserService),
  changeUserPassword: UserService.changeUserPassword.bind(UserService),
  sendMessage: UserService.sendMessage.bind(UserService),
  
  // 设备相关服务
  getRobotList: DeviceService.getRobotList.bind(DeviceService),
  getDeviceById: DeviceService.getDeviceById.bind(DeviceService),
  getDeviceName: DeviceService.getDeviceName.bind(DeviceService),
  
  // 任务相关服务
  getTasklist: TaskService.getTasklist.bind(TaskService),
  getTargetlist: TaskService.getTargetlist.bind(TaskService)
};