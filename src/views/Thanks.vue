<template>
  <div class="main">
    <h1 class="title">感谢您的参与</h1>
    <span style="font-size: 30px;">😘😘😘😘😘😘😘😘😘😘</span>
    <p class="p">您本次填写问卷的ID: {{ formData.id }}</p>
    <p>(●'◡'●)该问卷结果已发送至管理员邮箱(●'◡'●)</p>
    <img style="width: 160px; margin-top: 10px" src="/img/weChat.png" alt="Wechat QR Code">
    <p>联系管理员经审核后获取报酬</p>
    <el-button type="primary" @click="exportToJson">导出备份问卷数据（可选）</el-button>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import { saveAs } from 'file-saver';
import emailjs from 'emailjs-com';

const store = useStore();
const formData = computed(() => store.getters.getFormData);
const startTime = computed(() => store.state.startTime);

const formatDate = (date) => {
  const d = new Date(date);
  const offset = d.getTimezoneOffset() * 60000;
  const localDate = new Date(d.getTime() + offset + 28800000); // Convert to UTC+8
  return localDate.toISOString().replace('T', ' ').substring(0, 19);
};

const generateJsonData = () => {
  const currentTime = new Date();
  const endTime = formatDate(currentTime);
  const duration = (currentTime - new Date(startTime.value)) / 1000; // in seconds

  const data = {
    formData: formData.value,
    startTime: formatDate(startTime.value),
    endTime: endTime,
    duration: `${Math.floor(duration / 60)} minutes ${Math.floor(duration % 60)} seconds`,
    steps: []
  };

  for (let step = 0; step < Object.keys(store.state.groups).length; step++) {
    const stepData = {
      step: step + 1,
      groups: []
    };
    const groups = store.getters.getGroups(step);
    for (const group in groups) {
      stepData.groups.push({
        group: group,
        nodes: groups[group],
        rating: store.getters.getRating(step, group)
      });
    }
    data.steps.push(stepData);
  }

  return data;
};

const exportToJson = () => {
  const data = generateJsonData();
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  saveAs(blob, `${formData.value.id}.json`);
};

const sendEmail = (data) => {
  const emailData = {
    form_id: formData.value.id,
    to_email: 'zxx729149195@163.com',
    subject: `问卷+${formData.value.id}`,
    message: JSON.stringify(data, null, 2)
  };

  emailjs.send('service_w28zafs', 'template_cq4vqhy', emailData, 'zEOYsF4TFcaSSPSsZ')
    .then((response) => {
      console.log('Email sent successfully!', response.status, response.text);
    })
    .catch((error) => {
      console.error('Failed to send email:', error);
    });
};

onMounted(() => {
  const data = generateJsonData();
  sendEmail(data);
});
</script>

<style scoped>
.main {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.el-button {
  margin-top: 20px;
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
  background: linear-gradient(90deg, rgb(21, 250, 250) 0%, rgb(25, 57, 242) 50%, rgba(58, 123, 213, 1) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>
