<template>
  <div class="common-layout">
    <el-container class="full-height">
      <el-header class="header">
        <div class="header-content">
          <div class="left-content">
            <!-- <p class="id">分配ID：{{ formData.id }}</p> -->
          </div>
          <div class="right-content">
            <el-button plain @click="infoDialogVisible = true">打开说明<el-icon style='margin-left:5px'>
                <WindPower />
              </el-icon></el-button>
          </div>
        </div>
      </el-header>
      <el-main>
        <el-card class="main-card">
          <div style="display: flex;">
            <div class="left-two">
              <el-card class="top-card" shadow="never">
                <div v-html="Svg" class="svg-container"></div>
              </el-card>
              <el-card class="bottom-card" shadow="never">
                <div ref="chartContainer" class="chart-container" v-show="false"></div>
                <div v-html="Svg" class="svg-container2"></div>
              </el-card>
            </div>
            <el-card class="group-card" shadow="never">
              <div class="select-group">
                <el-select v-model="selectedGroup" placeholder="选择分组" @change="highlightGroup">
                  <el-option v-for="(group, index) in groupOptions" :key="index" :label="group" :value="group" />
                </el-select>
                <el-button @click="addNewGroup"><el-icon>
                    <Plus />
                  </el-icon></el-button>
                <el-button @click="deleteCurrentGroup"><el-icon>
                    <Delete />
                  </el-icon></el-button>
                <el-button @click="addOtherGroup"><el-icon>
                    <Finished />
                  </el-icon></el-button>
              </div>
              <div v-for="(nodes, group) in filteredGroups" :key="group" class="group">
                <h3>{{ group }}</h3>
                <el-scrollbar height="635px">
                  <div class="group-tags">
                    <el-tag v-for="node in nodes" :key="node" closable @close="removeFromGroup(group, node)"
                      @mousedown="highlightElement(node)" @mouseup="resetHighlight">
                      {{ node }}
                    </el-tag>
                  </div>
                </el-scrollbar>
                <el-rate :icons="icons" :void-icon="Hide" :colors="['#409eff', '#67c23a', '#FF9900']"
                  :texts="['直接无视', '有点感觉', '一般明显', '有点明显', '非常明显']" show-text v-model="ratings[group]" allow-half
                  class="rate" @change="updateRating(group, ratings[group])" />
              </div>
            </el-card>
          </div>
        </el-card>
      </el-main>
      <div class="steps-container">
        <el-button class="previous-button" @click="Previous"><el-icon>
            <CaretLeft />
          </el-icon></el-button>
        <el-steps :active="active" finish-status="success" class="steps">
          <el-step v-for="(step, index) in steps" :key="index" />
        </el-steps>
        <el-button class="next-button" @click="next" type="primary" v-if="active != steps.length - 1"><el-icon>
            <CaretRight />
          </el-icon></el-button>
        <el-button class="submit-button" @click="submit" type="success"
          v-if="active === steps.length - 1"><el-icon><Select /></el-icon></el-button>
      </div>
    </el-container>

    <el-dialog v-model="dialogVisible" title="提醒" width="700" align-center @close="handleDialogClose"
      :close-on-click-modal="false">
      <span>
        您已经做了15分钟了，可以稍微闭眼休息10到30秒以保证问卷效果。
      </span>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">我知道了</el-button>
        </div>
      </template>
    </el-dialog>

    <el-dialog v-model="infoDialogVisible" title="问卷说明" width="700" align-center>
      <span>
        在开始问卷之前，请仔细阅读以下说明：
        <ol>
          <li>(❁´◡`❁)</li>
          <li>(～￣▽￣)～</li>
          <li>╰(*°▽°*)╯</li>
        </ol>
      </span>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="infoDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleDialogConfirm">我明白了</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import * as d3 from 'd3';
import { Finished, Delete, Plus, Hide, View, CaretLeft, CaretRight, Select, WindPower } from '@element-plus/icons-vue';

const store = useStore();
const router = useRouter();
const formData = computed(() => store.getters.getFormData);
const selectedNodeIds = computed(() => store.state.selectedNodes.nodeIds);
const allVisiableNodes = computed(() => store.state.AllVisiableNodes);
const dialogVisible = ref(false);
const infoDialogVisible = ref(false);
const active = ref(0);
const steps = Array.from({ length: 10 });
const icons = [View, View, View];

const Svg = ref('');
const selectedGroup = ref('group1');
const ratings = ref({});
let reminderTimerId = null;

const updateRating = (group, rating) => {
  const step = active.value;
  store.commit('UPDATE_RATING', { step, group, rating });
};

const startTotalTimer = () => {
  setInterval(() => {
    store.commit('UPDATE_TOTAL_TIME_SPENT', store.state.totalTimeSpent + 1);
  }, 1000);
};

const startReminderTimer = () => {
  reminderTimerId = setTimeout(() => {
    dialogVisible.value = true;
  }, 15 * 60 * 1000);
};

const handleDialogClose = () => {
  dialogVisible.value = false;
  clearTimeout(reminderTimerId);
  startReminderTimer();
};

const fetchSvgContent = async (step) => {
  try {
    const svgModule = await import(`../../public/Data/${step}/${step}.svg?raw`);
    Svg.value = svgModule.default;
    turnGrayVisibleNodes();
    addHoverEffectToVisibleNodes();
    addClickEffectToVisibleNodes();
    nextTick(() => {
      highlightGroup();
    });
  } catch (error) {
    console.error('Error loading SVG content:', error);
    Svg.value = '<svg><text x="10" y="20" font-size="20">加载SVG时出错</text></svg>';
  }
};

const turnGrayVisibleNodes = () => {
  const svgContainer = document.querySelector('.svg-container2');
  if (!svgContainer) return;
  const svg = svgContainer.querySelector('svg');
  if (!svg) return;

  svg.querySelectorAll('*').forEach(node => {
    if (allVisiableNodes.value.includes(node.id)) {
      node.style.opacity = '0.2';
      node.style.cursor = 'pointer';
    }
  });
};

const addHoverEffectToVisibleNodes = () => {
  const svgContainer = document.querySelector('.svg-container2');
  if (!svgContainer) return;
  const svg = svgContainer.querySelector('svg');
  if (!svg) return;

  svg.querySelectorAll('*').forEach(node => {
    if (allVisiableNodes.value.includes(node.id)) {
      node.addEventListener('mouseover', () => {
        node.style.opacity = '1';
      });
      node.addEventListener('mouseout', () => {
        node.style.opacity = '0.2';
        highlightGroup();
      });
    }
  });

};

const addClickEffectToVisibleNodes = () => {
  const svgContainer = document.querySelector('.svg-container2');
  if (!svgContainer) return;
  const svg = svgContainer.querySelector('svg');
  if (!svg) return;

  svg.querySelectorAll('*').forEach(node => {
    if (allVisiableNodes.value.includes(node.id)) {
      node.addEventListener('click', () => {
        addToGroupAndHighlight(node.id);
      });
    }
  });
};

const highlightGroup = () => {
  const groupNodes = store.state.groups[active.value]?.[selectedGroup.value] || [];
  const svgContainer = document.querySelector('.svg-container2');
  if (!svgContainer) return;
  const svg = svgContainer.querySelector('svg');
  if (!svg) return;

  svg.querySelectorAll('*').forEach(node => {
    if (groupNodes.includes(node.id)) {
      node.style.opacity = '1';
    } else if (allVisiableNodes.value.includes(node.id)) {
      node.style.opacity = '0.2';
    }
  });
};

const highlightElement = (nodeId) => {
  const svgContainer = document.querySelector('.svg-container2');
  if (!svgContainer) return;
  const svg = svgContainer.querySelector('svg');
  if (!svg) return;
  nextTick(() => {
    svg.querySelectorAll('*').forEach(node => {
      if (node.id === nodeId) {
        node.style.opacity = '1';
      } else if (allVisiableNodes.value.includes(node.id)) {
        node.style.opacity = '0.2';
      }
    });
  });
};

const resetHighlight = () => {
  nextTick(() => {
    highlightGroup();
  });
};

const deleteCurrentGroup = () => {
  const step = active.value;
  store.commit('DELETE_GROUP', { step, group: selectedGroup.value });
  selectedGroup.value = 'group1';
  nextTick(() => {
    highlightGroup();
  });
};

const addOtherGroup = () => {
  const step = active.value;
  const group = 'Other';
  const allNodeIds = allVisiableNodes.value;
  const existingGroupNodeIds = Object.values(store.getters.getGroups(step)).flat();
  const otherNodeIds = allNodeIds.filter(nodeId => !existingGroupNodeIds.includes(nodeId));
  store.commit('ADD_OTHER_GROUP', { step, group, nodeIds: otherNodeIds });
  nextTick(() => {
    highlightGroup();
  });
};

const eleURL = computed(() => {
  const step = active.value + 1;
  return `../../public/Data/${step}/layer_data.json`;
});

const chartContainer = ref(null);

const handleDialogConfirm = () => {
  infoDialogVisible.value = false;
};

const next = async () => {
  if (active.value < steps.length - 1) {
    selectedGroup.value = 'group1';
    active.value++;
    await fetchSvgContent(active.value + 1);
    await fetchAndRenderTree();
    ensureGroupInitialization();
    nextTick(() => {
      highlightGroup();
    });
  }
};

const Previous = async () => {
  if (active.value > 0) {
    selectedGroup.value = 'group1';
    active.value--;
    await fetchSvgContent(active.value + 1);
    await fetchAndRenderTree();
    ensureGroupInitialization();
    nextTick(() => {
      highlightGroup();
    });
  }
};

const submit = () => {
  const totalTimeSpent = store.getters.getTotalTimeSpent;
  console.log(`Total time spent: ${totalTimeSpent} seconds`);
  router.push('/thanks');
};

const fetchAndRenderTree = async () => {
  if (!chartContainer.value) return;
  try {
    const response = await fetch(eleURL.value);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    renderTree(data);
  } catch (error) {
    console.error('There has been a problem with your fetch operation:', error);
  }
};

const renderTree = (data) => {
  const width = 1300;
  const height = 300;

  d3.select(chartContainer.value).select('svg').remove();

  const svg = d3.select(chartContainer.value)
    .append('svg')
    .attr('viewBox', `0 0 ${width} ${height}`)
    .style('width', '100%')
    .style('height', 'auto');

  const root = d3.treemap()
    .size([width, height])
    .padding(1)
    .round(true)
    (d3.hierarchy(data)
      .sum(d => d.value)
      .sort((a, b) => b.value - a.value));

  const leaf = svg.selectAll("g")
    .data(root.leaves())
    .join("g")
    .attr("transform", d => `translate(${d.x0},${d.y0})`);

  const nodeIds = [];
  leaf.each(d => {
    nodeIds.push(d.data.name.split("/").pop());
  });
  store.commit('UPDATE_ALL_VISIABLE_NODES', nodeIds);
  nextTick(() => {
    highlightGroup();
  });
};

const addToGroup = (nodeId) => {
  const step = active.value;
  store.commit('ADD_NODE_TO_GROUP', { step, group: selectedGroup.value, nodeId });
};

const addToGroupAndHighlight = (nodeId) => {
  addToGroup(nodeId);
  nextTick(() => {
    highlightGroup();
  });
};

const removeFromGroup = (group, nodeId) => {
  const step = active.value;
  store.commit('REMOVE_NODE_FROM_GROUP', { step, group, nodeId });
  nextTick(() => {
    highlightGroup();
  });
};

const addNewGroup = () => {
  const step = active.value;
  const newGroup = `group${Object.keys(groups.value).length + 1}`;
  store.commit('ADD_NEW_GROUP', { step, group: newGroup });
  selectedGroup.value = newGroup;
  ratings.value[newGroup] = 1;
  nextTick(() => {
    highlightGroup();
  });
};

const groups = computed(() => store.getters.getGroups(active.value));

const filteredGroups = computed(() => {
  return {
    [selectedGroup.value]: groups.value[selectedGroup.value] || []
  };
});

const groupOptions = computed(() => Object.keys(groups.value));

const ensureGroupInitialization = () => {
  const step = active.value;
  if (!groups.value['group1']) {
    store.commit('ADD_NEW_GROUP', { step, group: 'group1' });
    ratings.value['group1'] = 1;
  }
};

onMounted(async () => {
  await fetchSvgContent(active.value + 1);
  await fetchAndRenderTree();
  ensureGroupInitialization();
  startReminderTimer();
  startTotalTimer(); // Start the total timer
});

onMounted(() => {
  const stepRatings = store.state.ratings[active.value] || {};
  for (const group in groups.value) {
    ratings.value[group] = stepRatings[group] || 1;
  }
  nextTick(() => {
    highlightGroup(); // Ensure the group is highlighted on initial load
  });
});

watch([active, groups], () => {
  ratings.value = {};
  const stepRatings = store.state.ratings[active.value] || {};
  for (const group in groups.value) {
    ratings.value[group] = stepRatings[group] || 1;
  }
  nextTick(() => {
    highlightGroup();
  });
});

watch(active, async () => {
  await fetchSvgContent(active.value + 1);
  await fetchAndRenderTree();
  ensureGroupInitialization();
  nextTick(() => {
    highlightGroup();
  });
});

watch(selectedNodeIds, () => {
  nextTick(() => {
    highlightGroup();
  });
});

watch(allVisiableNodes, () => {
  turnGrayVisibleNodes();
  addHoverEffectToVisibleNodes();
  addClickEffectToVisibleNodes();
  highlightGroup();
});

</script>

<style scoped>
.common-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 85vw;
  margin: 0 auto;
}

.header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  border-bottom: 1px solid #dcdcdc;
}

.header-content {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.left-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  color: #999;
}

.right-content {
  display: flex;
  align-items: center;
}

.id {
  font-size: 16px;
  font-weight: bold;
}

.time {
  font-size: 18px;
  font-weight: bold;
  color: #ff6f6f;
}

.el-main {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  flex-direction: column;
}

.main-card {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;

  .left-two {
    display: flex;
    flex-direction: column;
    width: 250%;
    margin-right: 20px;
    .top-card{
      margin-bottom: 23px;
    }
  }
  .group-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;

  .select-group {
    display: flex;
    align-items: center;

    .el-select {
      margin-right: 10px;
      width: 180px;
    }
  }

  .group {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    margin-top: 10px;

    .group-tags-container {
      width: 100%;
      height: 100%;
    }

    .group-tags {
      display: flex;
      flex-wrap: wrap;
      justify-content: flex-start;
      width: 300px;

      .el-tag {
        margin: 5px;
        flex: 1 0 calc(33.33% - 10px);
        max-width: calc(33.33% - 10px);
        box-sizing: border-box;
        text-align: center;
        cursor: pointer;
      }
    }
  }
}
}

.svg-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.svg-container2 {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 50%;
}

.steps-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin: 35px 0;
}

.steps {
  flex-grow: 1;
  margin: 0 20px;
}

.previous-button,
.next-button,
.submit-button {
  margin: 0 12px;
}
</style>
