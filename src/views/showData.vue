<template>
  <el-card shadow="always" >
    <div v-if="loading && files.length === 0">
      <el-skeleton :rows="15" animated />
    </div>
    <div v-infinite-scroll="loadMoreFiles" :infinite-scroll-disabled="loading" infinite-scroll-distance="50" class="grid-container" style="height: 700px; overflow-y: auto;">
      <div v-for="file in files" :key="file" class="svg-container" @click="showSvg(file)">
        <img :src="`/questionnaire/newData/${file}.svg`" alt="SVG Image" />
        <span class="svgid">{{file}}</span>
      </div>
    </div>
    <el-dialog v-model="dialogVisible" width="60%" :before-close="handleClose">
      <img :src="`/questionnaire/newData/${selectedFile}.svg`" alt="SVG Image" class="large-svg" />
      <span>no.{{ selectedFile }}</span>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const files = ref([]);
const dialogVisible = ref(false);
const selectedFile = ref('');
const maxFiles = 540;
const loading = ref(false);  // 初始状态设置为 false
const batchSize = 20;
let currentFileIndex = 0;

const loadMoreFiles = async () => {
  if (loading.value) return;
  console.log("Loading more files..."); // 调试信息
  loading.value = true;
  const loadedFiles = [];
  for (let i = 0; i < batchSize; i++) {
    const fileIndex = currentFileIndex + i + 1;
    if (fileIndex > maxFiles) {
      loading.value = false;
      return;
    }

    const fileName = `${fileIndex}.svg`;
    try {
      const response = await fetch(`/questionnaire/newData/${fileName}`);
      if (response.ok) {
        loadedFiles.push(fileIndex.toString());
      } else {
        console.log(`File ${fileName} not found.`); // 文件未找到时的调试信息
        break;
      }
    } catch (error) {
      console.error('Error fetching file:', error);
      break;
    }
  }

  files.value.push(...loadedFiles);
  currentFileIndex += loadedFiles.length;
  loading.value = false;
  // console.log("Current files:", files.value); // 当前文件列表的调试信息
};

const showSvg = (file) => {
  selectedFile.value = file;
  dialogVisible.value = true;
};

const handleClose = () => {
  dialogVisible.value = false;
};

onMounted(() => {
  loadMoreFiles(); // 初次加载
});
</script>

<style scoped>
/* 滚动条整体宽度 */
.grid-container::-webkit-scrollbar {
  width: 8px;
}

/* 滚动条轨道 */
.grid-container::-webkit-scrollbar-track {
  background-color: #f1f1f1; /* 滚动条轨道的背景色 */
  border-radius: 10px; /* 圆角 */
}

/* 滚动条滑块 */
.grid-container::-webkit-scrollbar-thumb {
  background-color: #999; /* 滑块的颜色 */
  border-radius: 10px; /* 圆角 */
}

/* 滑块悬停状态 */
.grid-container::-webkit-scrollbar-thumb:hover {
  background-color: #666; /* 悬停时滑块的颜色 */
}

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
  position: relative;
}

.svgid {
  position: absolute;
  top: 0px;
  left: 5px;
  font-size: 0.7em;
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
