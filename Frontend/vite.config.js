import { defineConfig } from 'vite'
import tailwindcss from "@tailwindcss/vite";
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig(() => {
  return {
    plugins: [
      tailwindcss(),
      vue()
    ],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
        'vue-cropperjs/dist/vue-cropper.css': path.resolve(__dirname, 'node_modules/vue-cropperjs/node_modules/cropperjs/dist/cropper.css')
      }
    },
  }
})