<template>
  <div class="main">
    <h1 class="title">感谢您的参与</h1>
    <span style="font-size: 30px;">😘😘😘😘😘😘😘😘😘😘</span>
    <p class="p">您本次填写问卷的ID: <span class="highlight-id">{{ submitId }}</span></p>
    <p>(●'◡'●)该问卷结果已自动上传(●'◡'●)</p>
    <el-button type="primary" @click="exportToJson">👍导出备份问卷数据（可选）👍</el-button>
    <el-card><img style="width: 140px; margin-top: 10px" src="/img/weChat.png" alt="Wechat QR Code"></el-card>
    <p>联系管理员经审核后获取报酬</p>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { saveAs } from 'file-saver';

const store = useStore();
const router = useRouter();
const submitId = ref('');

onMounted(() => {
  // 检查是否有提交ID
  const storedSubmitId = localStorage.getItem('submitId');
  if (!storedSubmitId) {
    ElMessage.error('用户id失效，请重新进入');
    router.push('/');
    return;
  }
  submitId.value = storedSubmitId;
});

const exportToJson = () => {
  const data = JSON.parse(localStorage.getItem('submittedData'));
  if (!data) {
    ElMessage.error('数据不存在');
    return;
  }
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  saveAs(blob, `${submitId.value}.json`);
};
</script>

<style scoped>
.main {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.el-button {
  margin-top: 10px;
  margin-bottom: 10px;
}

.title {
  font-size: 3rem;
  color: #333;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 2px;
  text-align: center;
  background: linear-gradient(90deg, rgb(21, 250, 250) 0%, rgb(25, 57, 242) 50%, rgba(58, 123, 213, 1) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.p {
  font-size: 1.7rem;
  color: #333;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 2px;
  text-align: center;
  background: linear-gradient(90deg, rgb(17, 162, 240) 0%, rgb(25, 57, 242) 50%, rgba(58, 123, 213, 1) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.highlight-id {
  text-decoration: underline wavy red;
  font-weight: bold;
  font-size: 1.7rem; /* 可调整文字大小 */
  color: #d9534f; /* 文字颜色 */
}

</style>
