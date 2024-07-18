<template>
  <div class="grid-container">
    <div v-for="folder in folders" :key="folder" class="svg-container" @click="showSvg(folder)">
      <img :src="`../../public/Data/${folder}/${folder}.svg`" alt="SVG Image" />
    </div>
    <el-dialog v-model="dialogVisible" width="80%" :before-close="handleClose">
      <img :src="`../../public/Data/${selectedFolder}/${selectedFolder}.svg`" alt="SVG Image" class="large-svg" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { ElDialog } from 'element-plus';
import 'element-plus/theme-chalk/el-dialog.css';

const folders = ref([]);
const dialogVisible = ref(false);
const selectedFolder = ref('');

onMounted(() => {
  const folderFiles = import.meta.glob('../../public/Data/*/*.svg', { eager: true });
  const folderSet = new Set();
  for (const path in folderFiles) {
    const match = path.match(/Data\/(\d+)\//);
    if (match) {
      folderSet.add(match[1]);
    }
  }
  folders.value = Array.from(folderSet).sort((a, b) => a - b);
});

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
