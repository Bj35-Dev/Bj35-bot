<template>
  <section class="text-gray-600 body-font">
    <div class="container px-5 py-3 mx-auto">
      <div class="flex">
        <!-- 左侧技术栈滚动展示 -->
        <div class="w-3/8 pr-8 flex flex-col justify-center"> <!-- 添加 flex 和居中 -->
          <h2 class="text-xl font-medium title-font mb-8 text-gray-900">Tech Stack</h2>
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
                  <span v-for="tag in row.tags" :key="tag + '-clone'" class="tag">{{ tag }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧团队展示部分 -->
        <div class="w-3/4 pl-12"> <!-- 添加 pl-12 向右平移 -->
          <div class="flex flex-col text-center w-full mb-20">
            <h1 class="text-2xl font-medium title-font mb-4 text-gray-900 tracking-widest">OUR TEAM</h1>
            <p class="lg:w-2/3 mx-auto leading-relaxed text-base">
              Whatever cardigan tote bag tumblr hexagon brooklyn asymmetrical gentrify, subway tile poke farm-to-table.
              Franzen you probably haven't heard of them.
            </p>
          </div>
          <div class="flex flex-wrap -m-4">
            <div v-for="member in team" :key="member.name" class="p-4 lg:w-1/2">
              <div class="h-full flex sm:flex-row flex-col items-center sm:justify-start justify-center text-center sm:text-left">
                <img
                  alt="team"
                  class="flex-shrink-0 rounded-lg w-48 h-48 object-cover object-center sm:mb-0 mb-4"
                  :src="member.image"
                />
                <div class="flex-grow sm:pl-8">
                  <h2 class="title-font font-medium text-lg text-gray-900">{{ member.name }}</h2>
                  <h3 class="text-gray-500 mb-3">{{ member.position }}</h3>
                  <p class="mb-4">{{ member.description }}</p>
                  <span class="inline-flex">
                    <a :href="member.github" target="_blank" class="text-gray-500">
                      <svg class="w-5 h-5" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
                        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.19 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
                      </svg>
                    </a>
                    <a :href="member.telegram" target="_blank" class="ml-2 text-gray-500">
                      <svg class="w-5 h-5" viewBox="0 0 240 240" fill="currentColor" aria-hidden="true">
                        <path d="M120 0C53.7 0 0 53.7 0 120s53.7 120 120 120 120-53.7 120-120S186.3 0 120 0zm58.1 80.4l-17.8 84.4c-1.3 5.8-4.8 7.3-9.8 4.5l-27.1-20-13 12.5c-1.4 1.4-2.6 2.6-5.3 2.6l1.9-27.4 49.9-45.1c2.2-1.9-.5-3-3.4-1.1l-61.7 38.9-26.6-8.3c-5.8-1.8-5.9-5.8 1.3-8.6l103.9-40.1c4.8-1.8 9-0.2 7.3 8.7z"/>
                      </svg>
                    </a>
                    <a :href="member.website" target="_blank" class="ml-2 text-gray-500">
                      <svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="w-5 h-5" viewBox="0 0 24 24">
                        <path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/>
                      </svg>
                    </a>
                  </span>
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
            image: 'https://cn.cravatar.com/avatar/f42f9f288e5ba41aef369b4edd3c5f5c?d=retro&s=512',
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
          },
      ]
    }
  }
}
</script>

<style scoped>
.tech-stack {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.scroller-group {
  position: relative;
  width: 100%;
  overflow: hidden;
  mask: linear-gradient(90deg, transparent, white 20%, white 80%, transparent);
  -webkit-mask: linear-gradient(90deg, transparent, white 20%, white 80%, transparent);
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
</style>