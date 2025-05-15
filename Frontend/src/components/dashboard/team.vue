<template>
  <section class="text-gray-600 body-font">
    <div class="container px-4 sm:px-5 py-6 mx-auto">
      <div class="flex flex-col">
        <!-- 页面标题 -->
        <div class="text-center mb-6">
          <h1 class="text-3xl font-medium title-font mb-4 text-gray-900">About us</h1>
          <p class="lg:w-2/3 mx-auto leading-relaxed text-base">
            We’re a team of innovators and problem-solvers, blending design sensibility with functional precision. From Brooklyn-inspired aesthetics to minimalist details, we value craftsmanship without the pretension.
          </p>
        </div>
        
        <!-- 技术栈滚动展示 -->
        <div class="mb-12">
          <h2 class="text-xl font-medium title-font mb-1 text-center text-gray-900">Tech Stack</h2>
          <div class="tech-stack">
            <div v-for="(row, index) in tagRows" :key="index" class="scroller-group">
              <div class="scroller"
                   :class="{ 'scroll-reverse': row.direction === 'right' }"
                   :style="{ '--duration': row.duration + 's' }">
                <div class="tag-list">
                  <span v-for="tag in row.tags"
                        :key="tag"
                        class="tag"
                        :style="{
                          backgroundColor: row.colors.background,
                          color: row.colors.text
                        }">
                    {{ tag }}
                  </span>
                </div>
                <div class="tag-list" aria-hidden="true">
                  <span v-for="tag in row.tags" :key="tag + '-clone'" class="tag"
                        :style="{
                          backgroundColor: row.colors.background,
                          color: row.colors.text
                        }">{{ tag }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 团队成员展示 -->
        <div class="flex flex-wrap -m-4">
          <!-- 团队成员卡片 -->
          <div v-for="member in team" :key="member.name" class="p-4 lg:w-1/2 md:w-1/2 w-full">
            <div class="team-card bg-white rounded-lg p-6 shadow-sm hover:shadow-lg transition-all duration-300">
              <!-- 头部信息：头像和名字 -->
              <div class="flex items-center mb-4">
                <div class="avatar-container mr-4">
                  <img :src="member.image" alt="team" class="team-avatar w-16 h-16 bg-gray-100 object-cover object-center rounded-full transition-all duration-300">
                </div>
                <div>
                  <h2 class="text-xl text-gray-900 font-medium title-font hover:text-blue-600 transition-colors duration-300">
                    <a :href=member.website target="_blank" class="member-link">{{ member.name }}</a>
                  </h2>
                  <p class="text-gray-500">{{ member.position }}</p>
                </div>
              </div>
              
              <!-- 正文部分 -->
              <div class="border-t border-gray-100 pt-4">
                <div class="mb-4 text-gray-700 member-description">{{ member.description }}</div>
                <div class="flex justify-between items-center">
                  <div class="text-sm text-blue-500">{{ member.position }}</div>
                  <div class="inline-flex">
                    <a :href="member.github" target="_blank" class="social-icon text-gray-500 mr-3 hover:text-gray-700 transform hover:scale-110 transition-all duration-300">
                      <svg class="w-5 h-5" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
                        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.19 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
                      </svg>
                    </a>
                    <a :href="member.telegram" target="_blank" class="social-icon text-gray-500 hover:text-gray-700 transform hover:scale-110 transition-all duration-300">
                      <svg class="w-5 h-5" viewBox="0 0 240 240" fill="currentColor" aria-hidden="true">
                        <path d="M120 0C53.7 0 0 53.7 0 120s53.7 120 120 120 120-53.7 120-120S186.3 0 120 0zm58.1 80.4l-17.8 84.4c-1.3 5.8-4.8 7.3-9.8 4.5l-27.1-20-13 12.5c-1.4 1.4-2.6 2.6-5.3 2.6l1.9-27.4 49.9-45.1c2.2-1.9-.5-3-3.4-1.1l-61.7 38.9-26.6-8.3c-5.8-1.8-5.9-5.8 1.3-8.6l103.9-40.1c4.8-1.8 9-0.2 7.3 8.7z"/>
                      </svg>
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 加入我们卡片 -->
          <div class="p-4 lg:w-1/2 md:w-1/2 w-full">
            <div class="team-card join-card bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 flex flex-col justify-center items-center h-full">
              <svg class="w-16 h-16 text-blue-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path>
              </svg>
              <h2 class="text-xl text-gray-900 font-medium title-font mb-2">加入我们</h2>
              <p class="text-gray-600 text-center mb-4">我们一直在寻找优秀的开发者加入团队</p>
              <a href="mailto:join@example.com" class="inline-flex text-white bg-blue-500 border-0 py-2 px-6 focus:outline-none hover:bg-blue-600 rounded-full text-sm transition-colors duration-300">
                联系我们
              </a>
            </div>
          </div>
          
          <!-- 额外的项目统计卡片 -->
          <div class="p-4 lg:w-1/2 md:w-1/2 w-full">
            <div class="team-card stats-card bg-white rounded-lg p-6 h-full flex flex-col">
              <h3 class="text-lg font-medium text-gray-900 mb-4">项目统计</h3>
              <div class="flex flex-wrap mb-2">
                <div class="w-1/2 mb-4">
                  <div class="text-3xl font-semibold text-blue-600">15+</div>
                  <div class="text-sm text-gray-500">完成项目</div>
                </div>
                <div class="w-1/2 mb-4">
                  <div class="text-3xl font-semibold text-indigo-600">200k+</div>
                  <div class="text-sm text-gray-500">代码行数</div>
                </div>
                <div class="w-1/2">
                  <div class="text-3xl font-semibold text-purple-600">1+</div>
                  <div class="text-sm text-gray-500">年团队经验</div>
                </div>
                <div class="w-1/2">
                  <div class="text-3xl font-semibold text-green-600">24/7</div>
                  <div class="text-sm text-gray-500">技术支持</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'TeamSection',
  data() {
    return {
      tagRows: [
        {
          tags: ['Vue.js', 'Vite', 'HTML', 'CSS', 'CORS', 'Tailwind', 'RESTFUL API', 'yarn', 'i18n'],
          direction: 'left',
          duration: 20,
          colors: {
            background: '#f0fdf4',
            text: '#166534'
          }
        },
        {
          tags: ['JavaScript', 'Python', 'Quart', 'JWT', 'async', 'pydantic', 'asncpg', 'oauth2', 'Wecom'],
          direction: 'right',
          duration: 15,
          colors: {
            background: '#eff6ff',
            text: '#1e40af'
          }
        },
        {
          tags: ['Docker', 'Compose', 'Jenkins', 'Nginx', 'Jumpserver', 'golocproxy', 'PostgreSQL'],
          direction: 'left',
          duration: 22,
          colors: {
            background: '#fdf4ff',
            text: '#86198f'
          }
        }
      ],
      team: [
          {
            name: 'Yuhan Bian',
            position: 'Full-Stack Developer',
            description: '当你不知道做什么的时候，就重构吧',
            image: 'https://weavatar.com/avatar/f42f9f288e5ba41aef369b4edd3c5f5c?d=retro&s=512',
            github: 'https://github.com/AptS-1547',
            telegram: 'https://t.me/AptS1547',
            website: 'https://www.esaps.net'
          },
          {
            name: 'Zhicheng Dong',
            position: 'Full-Stack Developer',
            description: 'Nothing is impossible with Docker.！',
            image: 'https://cn.cravatar.com/avatar/4ca6db8f5673f5f001c5901fc04b2322ff304b13c9b805576ddf47e310a481dc?s=512',
            github: 'https://github.com/cg8-5712',
            telegram: 'http://cg85712.t.me',
            website: 'mailto:5712.cg8@gmail.com'
          },
          {
            name: 'Yuhe Cheng',
            position: 'Backend Developer',
            description: '前OI选手, 技术栈：python、C/C++, 擅长后端代码开发工作，但被强迫转型运维',
            image: 'https://avatars.githubusercontent.com/u/112048581',
            github: 'https://github.com/0515wlx',
            telegram: 'mailto:chengyuhe519@163.com',
            website: 'mailto:chengyuhe519@163.com'
          },
          {
            name: 'Lixuan Wei',
            position: 'Backend Developer',
            description: 'HPCer深度学习研究员，AI agent开发者。技术栈：python、C、cuda、C++擅长开发进程中的人文问题，提高资源利用率',
            image: 'https://avatars.githubusercontent.com/u/162896209',
            github: 'https://github.com/0515wlx',
            telegram: 'mailto:wlx20082022@163.com',
            website: 'mailto:wlx20082022@163.com'
          }
      ]
    }
  }
}
</script>

<style scoped>
.tech-stack {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.scroller-group {
  position: relative;
  width: 100%;
  overflow: hidden;
  mask: linear-gradient(90deg, transparent, white 10%, white 90%, transparent);
  -webkit-mask: linear-gradient(90deg, transparent, white 10%, white 90%, transparent);
}

.scroller {
  display: flex;
  animation: scroll var(--duration) linear infinite;
}

.scroll-reverse {
  animation-direction: reverse;
}

.tag-list {
  display: flex;
  gap: 1rem;
  padding: 0.5rem 0;
}

.tag {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.tag:hover {
  transform: translateY(-1px);
  filter: brightness(0.95);
}

.scroller-group:hover .scroller {
  animation-play-state: paused;
}

@keyframes scroll {
  from {
    transform: translateX(0);
  }
  to {
    transform: translateX(-50%);
  }
}

/* 确保滚动元素有足够的空间 */
.scroller > * {
  flex-shrink: 0;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .tag {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }
  
  .scroller-group {
    margin-bottom: 0.5rem;
  }
}

/* 为团队成员描述添加省略处理，防止过长 */
@media (max-width: 640px) {
  .flex-grow p {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

/* 团队成员卡片样式增强 */
.team-card {
  border: 1px solid rgba(229, 231, 235, 0.5);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.team-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border-color: rgba(209, 213, 219, 1);
}

.team-card:hover::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #2563eb, #7c3aed, #db2777);
  animation: border-glow 2s ease-in-out infinite;
}

.avatar-container {
  position: relative;
  display: inline-block;
  border-radius: 50%;
  transition: all 0.3s ease;
  overflow: hidden;
}

.avatar-container::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: transparent;
  border: 0px solid transparent;
  transition: all 0.3s ease;
}

.team-card:hover .avatar-container::after {
  border: 2px solid #3b82f6;
  box-shadow: 0 0 15px rgba(59, 130, 246, 0.5);
}

.team-avatar {
  transition: all 0.3s ease;
}

.team-card:hover .team-avatar {
  filter: brightness(1.1);
  transform: scale(1.05);
}

.member-link {
  position: relative;
  display: inline-block;
  text-decoration: none;
}

.member-link::after {
  content: '';
  position: absolute;
  width: 0;
  height: 2px;
  bottom: -2px;
  left: 0;
  background-color: #3b82f6;
  transition: width 0.3s ease;
}

.member-link:hover::after {
  width: 100%;
}

.social-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: rgba(243, 244, 246, 0.6);
  transition: all 0.3s ease;
}

.social-icon:hover {
  background-color: rgba(229, 231, 235, 1);
}

.member-description {
  position: relative;
  transition: all 0.3s ease;
}

.team-card:hover .member-description {
  color: #1f2937;
}

@keyframes border-glow {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .tag {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }
  
  .scroller-group {
    margin-bottom: 0.5rem;
  }
  
  .team-card {
    padding: 1rem;
  }
}

@media (max-width: 640px) {
  .member-description {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}
</style>