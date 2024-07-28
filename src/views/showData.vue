<template>
  <div class="grid-container">
    <div v-for="folder in folders" :key="folder" class="svg-container" @click="showSvg(folder)">
      <img :src="`/questionnaire/useData/${folder}.svg`" alt="SVG Image" />
    </div>
    <el-dialog v-model="dialogVisible" width="80%" :before-close="handleClose">
      <img :src="`/questionnaire/useData/${selectedFolder}.svg`" alt="SVG Image" class="large-svg" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const folders = ref(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']); // 手动维护文件名
const dialogVisible = ref(false);
const selectedFolder = ref('');

const showSvg = (folder) => {
  selectedFolder.value = folder;
  dialogVisible.value = true;
};

const handleClose = () => {
  dialogVisible.value = false;
};
</script>


<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
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
