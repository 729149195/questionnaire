<template>
  <div class="common-layout">
    <el-container class="full-height">
      <el-header class="header">
        <div class="header-content">
          <div class="left-content">
            <!-- <p class="id">分配ID：{{ formData.id }}</p> -->
          </div>
          <div class="right-content">
            <el-button plain @click="infoDialogVisible = true">
              打开说明
              <el-icon style='margin-left:5px'>
                <WindPower />
              </el-icon>
            </el-button>
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
                <div v-html="Svg" class="svg-container2" ref="svgContainer2"></div>
                <div id="overlay" class="overlay"></div>
                <el-button @click="toggleCropMode" class="Crop">
                  <el-icon>
                    <Crop />
                  </el-icon>
                </el-button>
              </el-card>
            </div>
            <el-card class="group-card" shadow="never">
              <div class="select-group">
                <el-select v-model="selectedGroup" placeholder="选择分组" @change="highlightGroup">
                  <el-option v-for="(group, index) in groupOptions" :key="index" :label="group" :value="group" />
                </el-select>
                <el-button @click="addNewGroup">
                  <el-icon>
                    <Plus />
                  </el-icon>
                </el-button>
                <el-button @click="deleteCurrentGroup">
                  <el-icon>
                    <Delete />
                  </el-icon>
                </el-button>
              </div>
              <div v-if="selectedGroup" class="group">
                <h3>{{ selectedGroup }}</h3>
                <el-scrollbar height="420px">
                  <div class="group-tags">
                    <el-tag v-for="node in currentGroupNodes" :key="node" closable
                      @close="removeFromGroup(selectedGroup, node)" @mousedown="highlightElement(node)"
                      @mouseup="resetHighlight">
                      {{ node }}
                    </el-tag>
                  </div>
                </el-scrollbar>
                <div v-if="ratings[selectedGroup]" ref="ratings" class="rate-container">
                  <div class="rate-container2">
                    <span>显眼程度：</span>
                    <el-rate :icons="icons" :void-icon="Hide" :colors="['#409eff', '#67c23a', '#FF9900']"
                      :texts="['一星', '二星', '三星', '四星', '五星']" show-text v-model="ratings[selectedGroup].attention"
                      allow-half class="rate"
                      @change="updateRating(selectedGroup, ratings[selectedGroup].attention, 'attention')" />
                  </div>
                  <div class="rate-container2">
                    <span>分组界限：</span>
                    <el-rate :icons="icons" :void-icon="Hide" :colors="['#409eff', '#67c23a', '#FF9900']"
                      :texts="['一星', '二星', '三星', '四星', '五星']" show-text v-model="ratings[selectedGroup].boundary"
                      allow-half class="rate"
                      @change="updateRating(selectedGroup, ratings[selectedGroup].boundary, 'boundary')" />
                  </div>
                </div>
              </div>
            </el-card>
          </div>
        </el-card>
      </el-main>
      <div class="steps-container">
        <el-button class="previous-button" @click="Previous">
          <el-icon>
            <CaretLeft />
          </el-icon>
        </el-button>
        <el-steps :active="active" finish-status="success" class="steps">
          <el-step v-for="(folder, index) in selectedFolders" :key="index" :title="'Step ' + (index + 1)" />
        </el-steps>
        <el-button class="next-button" @click="next" type="primary" v-if="active != selectedFolders.length - 1">
          <el-icon>
            <CaretRight />
          </el-icon>
        </el-button>
        <el-button class="submit-button" @click="submit" type="success" v-if="active === selectedFolders.length - 1">
          <el-icon>
            <Select />
          </el-icon>
        </el-button>
      </div>
    </el-container>

    <el-dialog v-model="dialogVisible" title="提醒" width="700" align-center @close="handleDialogClose"
      :close-on-click-modal="false">
      <span>您已经做了15分钟了，可以稍微闭眼休息10到30秒以保证问卷效果。</span>
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
          <li>视觉图形模式：即在视觉中感觉上应该分配到一组的元素集群。</li>
          <li>右侧group里对应的所有标签元素代表一个图形模式。</li>
          <li>请尽可能多地选出自己认为的合理的图形模式。</li>
          <li>报酬获取方式：将最后导出的数据文件及ID提交给管理员，管理员审批后根据完成情况及质量发放报酬。</li>
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
import { ref, computed, onMounted, watch, nextTick, onBeforeUnmount } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import * as d3 from 'd3';
import { Finished, Delete, Plus, Hide, View, CaretLeft, CaretRight, Select, WindPower, Crop } from '@element-plus/icons-vue';

const store = useStore();
const router = useRouter();
const formData = computed(() => store.getters.getFormData);
const selectedNodeIds = computed(() => store.state.selectedNodes.nodeIds);
const allVisiableNodes = computed(() => store.state.AllVisiableNodes);
const dialogVisible = ref(false);
const infoDialogVisible = ref(false);
const active = ref(0);
const icons = [View, View, View];
const svgContainer2 = ref(null);
const Svg = ref('');
const selectedGroup = ref('group1');
const ratings = ref({});
let reminderTimerId = null;
const nodeEventHandlers = new Map();
const selectedFolders = ref([]);
const steps = ref([]);

// 这里直接定义所有可能的文件夹列表
const availableFolders = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'];

const currentGroupNodes = computed(() => {
  if (!ratings.value[selectedGroup.value]) {
    ratings.value[selectedGroup.value] = { attention: 1, boundary: 1 };
  }
  return groups.value[selectedGroup.value] || [];
});

const updateRating = (group, rating, type) => {
  const step = active.value;
  store.commit('UPDATE_RATING', { step, group, rating, type });
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

const fetchSvgContent = async (folder) => {
  try {
    // 清理旧的事件处理器
    nodeEventHandlers.forEach((handler, node) => {
      node.removeEventListener('click', handler);
    });
    nodeEventHandlers.clear();

    const response = await fetch(`./Data/${folder}/${folder}.svg`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const svgContent = await response.text();
    Svg.value = svgContent;
    turnGrayVisibleNodes();
    addHoverEffectToVisibleNodes();
    addClickEffectToVisibleNodes();
    nextTick(() => {
      if (!isCropping.value) {
        addZoomEffectToSvg();
      }
      highlightGroup();
    });
  } catch (error) {
    console.error('Error loading SVG content:', error);
    Svg.value = '<svg><text x="10" y="20" font-size="20">加载SVG时出错</text></svg>';
  }
};

const fetchJsonData = async (folder) => {
  try {
    const response = await fetch(`./Data/${folder}/layer_data.json`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    renderTree(data);
  } catch (error) {
    console.error('Error loading JSON data:', error);
  }
};

const addZoomEffectToSvg = () => {
  const svgContainer = svgContainer2.value;
  if (!svgContainer) return;
  const svg = d3.select(svgContainer).select('svg');
  if (!svg) return;

  const zoom = d3.zoom()
    .scaleExtent([1, 10])
    .on('zoom', (event) => {
      svg.attr('transform', event.transform);
      limitPan(event.transform, svgContainer);
    });

  svg.call(zoom)
    .call(zoom.transform, d3.zoomIdentity.translate(svgContainer.clientWidth / 2, svgContainer.clientHeight / 2));

  function limitPan(transform, container) {
    const scale = transform.k;
    const width = container.clientWidth;
    const height = container.clientHeight;
    const maxX = (width / 2) * (scale - 1);
    const maxY = (height / 2) * (scale - 1);
    const limitedTransform = d3.zoomIdentity
      .translate(
        Math.max(Math.min(transform.x, maxX), -maxX),
        Math.max(Math.min(transform.y, maxY), -maxY)
      )
      .scale(scale);
    svg.attr('transform', limitedTransform);
  }
};

const isCropping = ref(false);
const startPoint = ref({ x: 0, y: 0 });
const currentRect = ref(null);

const toggleCropMode = () => {
  isCropping.value = !isCropping.value;
  if (isCropping.value) {
    svgContainer2.value.classList.add('crosshair-cursor');
    d3.select(svgContainer2.value).select('svg').on('.zoom', null);
  } else {
    svgContainer2.value.classList.remove('crosshair-cursor');
    addZoomEffectToSvg();
  }
};

const handleMouseDown = (event) => {
  if (!isCropping.value) return;

  const overlay = document.getElementById('overlay');
  if (!overlay) return;

  const rect = overlay.getBoundingClientRect();
  startPoint.value = {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top
  };

  currentRect.value = document.createElement('div');
  currentRect.value.classList.add('drag-selection');
  currentRect.value.style.left = `${startPoint.value.x}px`;
  currentRect.value.style.top = `${startPoint.value.y}px`;
  overlay.appendChild(currentRect.value);

  overlay.addEventListener('mousemove', handleMouseMove);
  overlay.addEventListener('mouseup', handleMouseUp);
};

const handleMouseMove = (event) => {
  if (!currentRect.value) return;

  const overlay = document.getElementById('overlay');
  if (!overlay) return;

  const rect = overlay.getBoundingClientRect();
  const currentPoint = {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top
  };

  const width = Math.abs(currentPoint.x - startPoint.value.x);
  const height = Math.abs(currentPoint.y - startPoint.value.y);
  const left = Math.min(currentPoint.x, startPoint.value.x);
  const top = Math.min(currentPoint.y, startPoint.value.y);

  currentRect.value.style.width = `${width}px`;
  currentRect.value.style.height = `${height}px`;
  currentRect.value.style.left = `${left}px`;
  currentRect.value.style.top = `${top}px`;
};

const handleMouseUp = () => {
  const overlay = document.getElementById('overlay');
  if (!overlay) return;

  overlay.removeEventListener('mousemove', handleMouseMove);
  overlay.removeEventListener('mouseup', handleMouseUp);

  currentRect.value = null;
};

const turnGrayVisibleNodes = () => {
  const svgContainer = svgContainer2.value;
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
  const svgContainer = svgContainer2.value;
  if (!svgContainer) return;
  const svg = svgContainer.querySelector('svg');
  if (!svg) return;

  svg.querySelectorAll('*').forEach(node => {
    if (allVisiableNodes.value.includes(node.id)) {
      const handleMouseOver = () => {
        node.style.opacity = '1';
      };
      const handleMouseOut = () => {
        node.style.opacity = '0.2';
        highlightGroup();
      };

      node.removeEventListener('mouseover', handleMouseOver);
      node.removeEventListener('mouseout', handleMouseOut);

      node.addEventListener('mouseover', handleMouseOver);
      node.addEventListener('mouseout', handleMouseOut);
    }
  });
};

const addClickEffectToVisibleNodes = () => {
  const svgContainer = svgContainer2.value;
  if (!svgContainer) return;
  const svg = svgContainer.querySelector('svg');
  if (!svg) return;

  svg.querySelectorAll('*').forEach(node => {
    if (allVisiableNodes.value.includes(node.id)) {
      const oldHandler = nodeEventHandlers.get(node);

      if (oldHandler) {
        node.removeEventListener('click', oldHandler);
      }

      const handleNodeClick = () => {
        const groupNodes = store.state.groups[active.value]?.[selectedGroup.value] || [];
        if (groupNodes.includes(node.id)) {
          store.commit('REMOVE_NODE_FROM_GROUP', { step: active.value, group: selectedGroup.value, nodeId: node.id });
        } else {
          store.commit('ADD_NODE_TO_GROUP', { step: active.value, group: selectedGroup.value, nodeId: node.id });
        }
        nextTick(() => {
          highlightGroup();
        });
      };

      nodeEventHandlers.set(node, handleNodeClick);
      node.addEventListener('click', handleNodeClick);
    }
  });
};

const highlightGroup = () => {
  const groupNodes = store.state.groups[active.value]?.[selectedGroup.value] || [];
  const svgContainer = svgContainer2.value;
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
  const svgContainer = svgContainer2.value;
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

const chartContainer = ref(null);

const handleDialogConfirm = () => {
  infoDialogVisible.value = false;
};

const next = async () => {
  if (active.value < selectedFolders.value.length - 1) {
    selectedGroup.value = 'group1';
    active.value++;
    const folder = selectedFolders.value[active.value];
    await fetchSvgContent(folder);
    await fetchJsonData(folder);
    ensureGroupInitialization();
    nextTick(() => {
      highlightGroup();
    });
    isCropping.value = false;
    svgContainer2.value.classList.remove('crosshair-cursor');
  }
};

const Previous = async () => {
  if (active.value > 0) {
    selectedGroup.value = 'group1';
    active.value--;
    const folder = selectedFolders.value[active.value];
    await fetchSvgContent(folder);
    await fetchJsonData(folder);
    ensureGroupInitialization();
    nextTick(() => {
      highlightGroup();
    });
    isCropping.value = false;
    svgContainer2.value.classList.remove('crosshair-cursor');
  }
};

const submit = () => {
  const totalTimeSpent = store.getters.getTotalTimeSpent;
  console.log(`Total time spent: ${totalTimeSpent} seconds`);
  router.push('/thanks');
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
  ratings.value[newGroup] = { attention: 1, boundary: 1 };
  nextTick(() => {
    highlightGroup();
  });
};

const groups = computed(() => store.getters.getGroups(active.value));

const filteredGroups = computed(() => {
  const result = {};
  for (const group of Object.keys(groups.value)) {
    result[group] = groups.value[group];
    if (!ratings.value[group]) {
      ratings.value[group] = { attention: 1, boundary: 1 };
    }
  }
  return result;
});

const groupOptions = computed(() => Object.keys(groups.value));

const ensureGroupInitialization = () => {
  const step = active.value;
  if (!groups.value['group1']) {
    store.commit('ADD_NEW_GROUP', { step, group: 'group1' });
    ratings.value['group1'] = { attention: 1, boundary: 1 };
  }
};

const loadData = async () => {
  // 随机选择 5 个文件夹
  const shuffled = availableFolders.sort(() => 0.5 - Math.random());
  selectedFolders.value = shuffled.slice(0, 5);
  steps.value = Array(selectedFolders.value.length).fill({});
  const folder = selectedFolders.value[active.value];
  await fetchSvgContent(folder);
  await fetchJsonData(folder);
  ensureGroupInitialization();
  startReminderTimer();
  startTotalTimer();
};

onMounted(async () => {
  await loadData();
});

onMounted(() => {
  const overlay = document.getElementById('overlay');
  if (overlay) {
    overlay.addEventListener('mousedown', handleMouseDown);
  }

  const stepRatings = store.state.ratings[active.value] || {};
  for (const group in groups.value) {
    ratings.value[group] = stepRatings[group] || { attention: 1, boundary: 1 };
  }
  nextTick(() => {
    highlightGroup();
  });
});

watch([active, groups], () => {
  ratings.value = {};
  const stepRatings = store.state.ratings[active.value] || {};
  for (const group in groups.value) {
    ratings.value[group] = stepRatings[group] || { attention: 1, boundary: 1 };
  }
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

onBeforeUnmount(() => {
  const overlay = document.getElementById('overlay');
  if (overlay) {
    overlay.removeEventListener('mousedown', handleMouseDown);
    overlay.removeEventListener('mousemove', handleMouseMove);
    overlay.removeEventListener('mouseup', handleMouseUp);
  }
});
</script>

<style scoped>
.common-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 80vw;
  margin: 0 auto;
}

.header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 10px;
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

.el-main {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  flex-direction: column;
  margin-bottom: -10px;
}

.main-card {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;

  .left-two {
    display: flex;
    flex-direction: column;
    width: 200%;
    margin-right: 20px;

    .top-card {
      margin-bottom: 20px;
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
        width: 200px;
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
  position: relative;
}

.steps-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin: 25px 0;
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

.bottom-card {
  position: relative;

  .Crop {
    position: absolute;
    top: 10px;
    right: 10px;
  }
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.drag-selection {
  position: absolute;
  border: 3px solid black;
  background-color: rgba(0, 0, 0, 0.3);
}

.crosshair-cursor {
  cursor: crosshair !important;
}

.rate-container {
  display: flex;
  flex-direction: column;

  .rate-container {
    display: flex;
    align-items: center;
    font-size: 14px;
  }
}
</style>
