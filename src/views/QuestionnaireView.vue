<template>
  <div class="common-layout">
    <el-container class="full-height">
      <el-header class="header">
        <h2 class="title">图形模式感知问卷</h2>
      </el-header>
      <el-divider>
        <el-icon><star-filled/></el-icon>
      </el-divider>
      <el-main>
        <div class="personal-info">
          <h2>个人信息</h2>
          <p class="confidentiality">您的信息将被保密。( •̀ ω •́ )✧</p>
          <el-form label-position="top" class="form" @submit.prevent="handleSubmit">
            <el-form-item label="年龄">
              <el-input v-model="form.age" placeholder="输入您的年龄" class="input-field"></el-input>
            </el-form-item>
            <el-form-item label="性别">
              <el-radio-group v-model="form.gender" class="input-field">
                <el-radio :value="'male'">男</el-radio>
                <el-radio :value="'female'">女</el-radio>
                <el-radio :value="OTHER">其他</el-radio>
              </el-radio-group>
              <span v-if="form.gender === OTHER">你确定吗？(ﾟДﾟ*)ﾉ</span>
            </el-form-item>
            <el-form-item label="您是否有看过可视化作品（比如折线图、柱状图）？">
              <el-radio-group v-model="form.visualizationExperience" class="input-field">
                <el-radio :value="'yes'">有</el-radio>
                <el-radio :value="'no'">没有</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item class="form-button">
              <div>
                <el-button @click="handleClean">清空</el-button>
                <el-button type="primary" @click="handleSubmit">下一步</el-button>
              </div>
            </el-form-item>
          </el-form>
        </div>
      </el-main>
      <el-divider border-style="double" />
      <el-footer>{{ currentTime }}</el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { StarFilled } from '@element-plus/icons-vue';

const store = useStore();
const router = useRouter();

const currentTime = ref(new Date().toLocaleTimeString());

const updateCurrentTime = () => {
  currentTime.value = new Date().toLocaleTimeString();
};

let timer = null;

onMounted(() => {
  timer = setInterval(updateCurrentTime, 1000);
});

onUnmounted(() => {
  clearInterval(timer);
});

const form = ref({
  age: '',
  gender: '',
  visualizationExperience: '',
});

const OTHER = 'other';  // Define a constant for 'other'

const handleSubmit = () => {
  store.dispatch('submitForm', form.value);
  const formData = store.getters.getFormData;
  // ElNotification({
  //   title: '成功',
  //   message: `编号：${formData.id} 初始化成功`,
  //   type: 'success',
  //   duration: 3000,
  // });
  router.push('/questionstest');
};

const handleClean = () => {
  form.value = {
    age: '',
    gender: '',
    visualizationExperience: '',
  };
};
</script>

<style lang="scss" scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.common-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 80vw;
  margin: 0 auto;
}

.full-height {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.el-header,
.el-footer {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.el-main {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: start;
  position: relative;
  top: 10px;
  flex-direction: column;
  padding: 20px;
}

.personal-info {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.personal-info h2 {
  font-size: 2rem;
  text-align: center;
  color: #333;
}

.confidentiality {
  font-size: 1.1rem;
  color: #666;
  text-align: center;
  margin-bottom: 20px;
}

.form-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  .el-button {
    width: 16rem;
    height: 40px;
    font-size: 18px;
  }
}

.el-radio {
  margin-right: 30px;
}

.el-form-item {
  margin-bottom: 20px;
}

.el-select-dropdown__item{
  padding-left: 10px;
}

.title {
  font-size: 2.7rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 2px;
  text-align: center;
  background: linear-gradient(90deg, rgb(21, 250, 250) 0%, rgb(25, 57, 242) 50%, rgba(58, 123, 213, 1) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 5px;
}
</style>
