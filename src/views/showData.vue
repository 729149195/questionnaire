<template>
  <div v-if="loading">
      <el-skeleton :rows="15" animated />
    </div>
  <div class="grid-container">
    <div v-for="file in files" :key="file" class="svg-container" @click="showSvg(file)">
      <img :src="`/questionnaire/newData/${file}.svg`" alt="SVG Image" />
    </div>
    <el-dialog v-model="dialogVisible" width="80%" :before-close="handleClose">
      <img :src="`/questionnaire/newData/${selectedFile}.svg`" alt="SVG Image" class="large-svg" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const files = ref([]);
const dialogVisible = ref(false);
const selectedFile = ref('');
const maxFiles = 53; // 假设最多有53个文件
const loading = ref(true)

const checkFiles = async () => {
  const loadedFiles = [];
  for (let i = 1; i <= maxFiles; i++) {
    const fileName = `${i}.svg`;
    try {
      // 尝试加载文件
      const response = await fetch(`/questionnaire/newData/${fileName}`);
      if (response.ok) {
        loadedFiles.push(i.toString());
      } else {
        // 如果文件不存在，则停止查找
        break;
      }
    } catch (error) {
      // 网络错误或其他问题
      console.error('Error fetching file:', error);
      break;
    }
  }
  files.value = loadedFiles;
  loading.value = false;
};

const showSvg = (file) => {
  selectedFile.value = file;
  dialogVisible.value = true;
};

const handleClose = () => {
  dialogVisible.value = false;
};

onMounted(checkFiles);
</script>

<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 10px;
  padding: 20px;
  width: 90vw;
  box-sizing: border-box;
}

.svg-container {
  border: 1px solid #ccc;
  padding: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #fff;
  cursor: pointer;
}

.svg-container img {
  max-width: 100%;
  max-height: 100%;
}

.el-dialog__body {
  display: flex;
  align-items: center;
  justify-content: center;
}

.large-svg {
  max-width: 100%;
  max-height: 100%;
}
</style>
