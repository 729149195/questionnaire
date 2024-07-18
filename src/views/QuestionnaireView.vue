<template>
  <div class="common-layout">
    <Particles id="tsparticles" :options="particlesOptions" />
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
            <el-form-item label="1、年龄" label-for="age">
              <el-input id="age" v-model="form.age" placeholder="输入您的年龄" class="input-field"></el-input>
            </el-form-item>
            <el-form-item label="2、性别" label-for="gender">
              <el-radio-group id="gender" v-model="form.gender" class="input-field">
                <el-radio :value="'male'">男</el-radio>
                <el-radio :value="'female'">女</el-radio>
                <el-radio :value="OTHER">其他</el-radio>
              </el-radio-group>
              <span v-if="form.gender === OTHER">你确定吗？(ﾟДﾟ*)ﾉ</span>
            </el-form-item>
            <el-form-item label="3、您是否有看过可视化作品（比如折线图、柱状图）？" label-for="visualizationExperience">
              <el-radio-group id="visualizationExperience" v-model="form.visualizationExperience" class="input-field">
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
  router.push('/questionstest');
};

const handleClean = () => {
  form.value = {
    age: '',
    gender: '',
    visualizationExperience: '',
  };
};

// 定义粒子背景的配置
const particlesOptions = ref({
  particles: {
    number: {
      value: 50,
      density: {
        enable: true,
        value_area: 800
      }
    },
    color: {
      value: ["#4285f4", "#ea4335", "#fbbc05", "#34a853"]
    },
    shape: {
      type: "circle",
      stroke: {
        width: 0,
        color: "#000000"
      },
      polygon: {
        nb_sides: 5
      }
    },
    opacity: {
      value: 0.5,
      random: false,
      anim: {
        enable: false,
        speed: 1,
        opacity_min: 0.1,
        sync: false
      }
    },
    size: {
      value: 5,
      random: true,
      anim: {
        enable: false,
        speed: 40,
        size_min: 0.1,
        sync: false
      }
    },
    line_linked: {
      enable: true,
      distance: 150,
      color: "#000000",
      opacity: 0.4,
      width: 1
    },
    move: {
      enable: true,
      speed: 6,
      direction: "none",
      random: false,
      straight: false,
      out_mode: "out",
      bounce: false,
      attract: {
        enable: false,
        rotateX: 600,
        rotateY: 1200
      }
    }
  },
  interactivity: {
    detect_on: "canvas",
    events: {
      onhover: {
        enable: true,
        mode: "grab"
      },
      onclick: {
        enable: true,
        mode: "push"
      },
      resize: true
    },
    modes: {
      grab: {
        distance: 140,
        line_linked: {
          opacity: 1
        }
      },
      bubble: {
        distance: 400,
        size: 40,
        duration: 2,
        opacity: 8,
        speed: 3
      },
      repulse: {
        distance: 200,
        duration: 0.4
      },
      push: {
        particles_nb: 4
      },
      remove: {
        particles_nb: 2
      }
    }
  },
  retina_detect: true
});
</script>

<style lang="scss" scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#tsparticles {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: -1;
}

.common-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 80vw;
  margin: 0 auto;
  position: relative;  // Ensure the layout is positioned correctly
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
  padding: 10px;
}

.personal-info {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  padding: 30px;
  background: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.personal-info h2 {
  font-size: 1.7rem;
  text-align: center;
  color: #333;
}

.confidentiality {
  font-size: 0.8rem;
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
    width: 14rem;
    height: 40px;
    font-size: 16px;
  }
}

.el-radio {
  margin-right: 30px;
}

.el-form-item {
  margin-bottom: 20px;
}

.el-select-dropdown__item {
  padding-left: 10px;
}

.title {
  font-size: 2.5rem;
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
