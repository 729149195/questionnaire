<template>
  <div class="common-layout">
    <el-container class="full-height">
      <el-header class="header">
        <div class="header-content">
          <div class="left-content">
            <!-- <p class="id">分配ID：{{ formData.id }}</p> -->
            <a href="https://github.com/729149195/questionnaire" target="_blank">
              <img style="width: 30px;" src="/img/favicon.png" alt="Wechat QR Code">
            </a>
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
                <el-button class="top-title" disabled text bg>模式观察区域</el-button>
              </el-card>
              <el-card class="bottom-card" shadow="never">
                <div ref="chartContainer" class="chart-container" v-show="false"></div>
                <div v-html="Svg" class="svg-container2" ref="svgContainer2"></div>
                <el-button @click="toggleCropMode" class="Crop"><el-icon><Crop /></el-icon></el-button>
                <el-button class="bottom-title" disabled text bg>选取交互区域</el-button>
              </el-card>
            </div>
            <el-card class="group-card" shadow="never">
              <div class="select-group">
                <el-select v-model="selectedGroup" placeholder="选择模式" @change="highlightGroup">
                  <el-option v-for="(group, index) in groupOptions" :key="index" :label="group" :value="group" />
                </el-select>
                <el-button @click="addNewGroup"><el-icon>
                    <Plus />
                  </el-icon></el-button>
                <el-button @click="deleteCurrentGroup"><el-icon>
                    <Delete />
                  </el-icon></el-button>
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
                <div v-if="ratings[selectedGroup]" ref="rateings" class="rate-container">
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

    <el-dialog v-model="infoDialogVisible" title="问卷说明" width="1000" align-center>
      <span>
        在正式开始问卷之前，请仔细阅读以下说明：
        <ol>
          <li>图形模式：指由线条、形状、颜色等元素组成的视觉结构</li>
          <li>右侧模式N里对应的所有标签元素代表一个图形模式</li>
          <li>请尽可能多地选出自己认为的合理的图形模式</li>
          <li>这些图形模式大概率会产生重叠，即同一个元素可以同时属于多个图形模式</li>
          <li>虽然显眼程度和分组界限的评分很重要，但请不要过多思考分析，尽量遵循自己的第一印象来进行打分</li>
          <li>报酬获取方式：完成问卷后待系统自动将结果提交后，联系管理员并提交问卷ID，管理员审批后将根据完成情况及质量发放报酬（一般不会低于XX￥）</li>
        </ol>
      </span>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="infoDialogVisible = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import * as d3 from 'd3';
import { Delete, Plus, Hide, View, CaretLeft, CaretRight, Select, WindPower, Crop } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';

const store = useStore();
const router = useRouter();
const formData = computed(() => store.getters.getFormData);
const selectedNodeIds = computed(() => store.state.selectedNodes.nodeIds);
const allVisiableNodes = computed(() => store.state.AllVisiableNodes);
const steps = computed(() => store.state.steps);
const dialogVisible = ref(false);
const infoDialogVisible = ref(true);
const active = ref(0);
const icons = [View, View, View];
const svgContainer2 = ref(null);

const Svg = ref('');
const selectedGroup = ref('模式1');
const ratings = ref({});
let reminderTimerId = null;
const nodeEventHandlers = new Map();
const isCropping = ref(false);

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

const fetchSvgContent = async (step) => {
  try {
    nodeEventHandlers.forEach((handler, node) => {
      node.removeEventListener('click', handler);
    });
    nodeEventHandlers.clear();

    const response = await fetch(`./Data2/${step}/${step}.svg`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const svgContent = await response.text();
    Svg.value = svgContent;
    turnGrayVisibleNodes();
    addHoverEffectToVisibleNodes();
    addClickEffectToVisibleNodes();
    nextTick(() => {
      highlightGroup();
      addZoomEffectToSvg();
    });
  } catch (error) {
    console.error('Error loading SVG content:', error);
    Svg.value = '<svg><text x="10" y="20" font-size="20">加载SVG时出错</text></svg>';
  }
};

const addZoomEffectToSvg = () => {
  const svgContainer = svgContainer2.value;
  if (!svgContainer) return;
  const svg = d3.select(svgContainer).select('svg');
  if (!svg) return;

  const zoom = d3.zoom()
    .scaleExtent([1, 20])
    .on('zoom', (event) => {
      if (!isCropping.value) {
        svg.attr('transform', event.transform);
        limitPan(event.transform, svgContainer);
      }
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

let isDrawing = false; // 标志是否正在绘制
let rectElement; // 矩形元素
let handleMouseClick, handleMouseMove, handleMouseUp; // 事件处理程序

const toggleCropMode = () => {
  isCropping.value = !isCropping.value;
  const svg = d3.select(svgContainer2.value).select('svg');
  if (isCropping.value) {
    nextTick(() => {
      svgContainer2.value.classList.add('crosshair-cursor');
    });
    ElMessage.info('进入选框模式');
    enableCropSelection();
    svg.on('.zoom', null); // 禁用缩放事件
  } else {
    svgContainer2.value.classList.remove('crosshair-cursor');
    ElMessage.info('退出选框模式');
    disableCropSelection();
    addZoomEffectToSvg(); // 重新启用缩放功能
  }
};

const enableCropSelection = () => {
  let startX, startY;
  const svg = svgContainer2.value.querySelector('svg');

  handleMouseClick = (event) => {
    if (!isDrawing) {
      isDrawing = true;
      const point = svg.createSVGPoint();
      point.x = event.clientX;
      point.y = event.clientY;
      const svgPoint = point.matrixTransform(svg.getScreenCTM().inverse());

      startX = svgPoint.x;
      startY = svgPoint.y;

      rectElement = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      rectElement.setAttribute('x', startX);
      rectElement.setAttribute('y', startY);
      rectElement.setAttribute('stroke', 'red');
      rectElement.setAttribute('stroke-width', '2');
      rectElement.setAttribute('fill', 'none');
      svg.appendChild(rectElement);

      svg.addEventListener('mousemove', handleMouseMove);
      svg.addEventListener('mouseup', handleMouseUp);
    }
  };

  handleMouseMove = (event) => {
    if (isDrawing) {
      const point = svg.createSVGPoint();
      point.x = event.clientX;
      point.y = event.clientY;
      const svgPoint = point.matrixTransform(svg.getScreenCTM().inverse());

      const endX = svgPoint.x;
      const endY = svgPoint.y;
      const rectWidth = Math.abs(endX - startX);
      const rectHeight = Math.abs(endY - startY);
      const rectX = Math.min(startX, endX);
      const rectY = Math.min(startY, endY);

      rectElement.setAttribute('width', rectWidth);
      rectElement.setAttribute('height', rectHeight);
      rectElement.setAttribute('x', rectX);
      rectElement.setAttribute('y', rectY);
    }
  };

  const handleMouseUp = (event) => {
  if (isDrawing) {
    isDrawing = false;

    const rectX = parseFloat(rectElement.getAttribute('x'));
    const rectY = parseFloat(rectElement.getAttribute('y'));
    const rectWidth = parseFloat(rectElement.getAttribute('width'));
    const rectHeight = parseFloat(rectElement.getAttribute('height'));

    const svg = svgContainer2.value.querySelector('svg');
    svg.querySelectorAll('*').forEach(node => {
      if (typeof node.getBBox === 'function') {
        const bbox = node.getBBox();
        const isTouched =
          (bbox.x + bbox.width) >= rectX &&
          bbox.x <= (rectX + rectWidth) &&
          (bbox.y + bbox.height) >= rectY &&
          bbox.y <= (rectY + rectHeight);

        if (isTouched) {
          node.dispatchEvent(new Event('click')); // 模拟点击事件
        }
      }
    });

    rectElement.remove(); // 移除选框
    svg.removeEventListener('mousemove', handleMouseMove);
    svg.removeEventListener('mouseup', handleMouseUp);
  }
};

  svg.addEventListener('mousedown', handleMouseClick);
};

const disableCropSelection = () => {
  const svg = svgContainer2.value.querySelector('svg');
  if (svg) {
    svg.removeEventListener('mousedown', handleMouseClick);
    svg.removeEventListener('mousemove', handleMouseMove);
    svg.removeEventListener('mouseup', handleMouseUp);
  }
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
          console.log("REMOVE_NODE_FROM_GROUP", node.id);  // 调试用，检查节点移除
        } else {
          store.commit('ADD_NODE_TO_GROUP', { step: active.value, group: selectedGroup.value, nodeId: node.id });
          console.log("ADD_NODE_TO_GROUP", node.id);  // 调试用，检查节点添加
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
  selectedGroup.value = '模式1';
  nextTick(() => {
    highlightGroup();
  });
};

const eleURL = computed(() => {
  const step = store.state.steps[active.value];
  return `./Data2/${step}/layer_data.json`;
});

const chartContainer = ref(null);

const next = async () => {
  if (steps.value && active.value < steps.value.length - 1) {
    selectedGroup.value = '模式1';
    active.value++;
    await fetchSvgContent(steps.value[active.value]);
    await fetchAndRenderTree();
    ensureGroupInitialization();
    nextTick(() => {
      highlightGroup();
    });
    isCropping.value = false;
    svgContainer2.value.classList.remove('crosshair-cursor');
  }
};

const Previous = async () => {
  if (steps.value && active.value > 0) {
    selectedGroup.value = '模式1';
    active.value--;
    await fetchSvgContent(steps.value[active.value]);
    await fetchAndRenderTree();
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

const removeFromGroup = (group, nodeId) => {
  const step = active.value;
  store.commit('REMOVE_NODE_FROM_GROUP', { step, group, nodeId });
  nextTick(() => {
    highlightGroup();
  });
};

const addNewGroup = () => {
  const step = active.value;
  const newGroup = `模式${Object.keys(groups.value).length + 1}`;
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
  if (!groups.value['模式1']) {
    store.commit('ADD_NEW_GROUP', { step, group: '模式1' });
    ratings.value['模式1'] = { attention: 1, boundary: 1 };
  }
};

const generateRandomArray = () => {
  const numbers = Array.from({ length: 53 }, (_, index) => index + 1);
  const randomArray = [];
  while (randomArray.length < 20) {
    const randomIndex = Math.floor(Math.random() * numbers.length);
    const number = numbers.splice(randomIndex, 1)[0];
    randomArray.push(number);
  }
  return randomArray;
};

onMounted(() => {
  const randomSteps = generateRandomArray();
  store.commit('setSteps', randomSteps);
  store.dispatch('initializeSteps');
  if (steps.value && steps.value.length > 0) {
    fetchSvgContent(steps.value[active.value]);
  }
  fetchAndRenderTree();
  ensureGroupInitialization();
  startReminderTimer();
  startTotalTimer();
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

watch(steps, (newSteps) => {
  if (newSteps && newSteps.length > 0) {
    nextTick(() => {
      fetchSvgContent(newSteps[active.value]);
    });
  }
});

watch(active, async () => {
  await fetchSvgContent(store.state.steps[active.value]);
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
}

.svg-container2 {
  display: flex;
  justify-content: center;
  align-items: center;
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
  .bottom-title {
    position: absolute;
    top: 5px;
    left: -15px;
  }
}

.top-card {
  position: relative;

  .top-title {
    position: absolute;
    top: 5px;
    left: -5px;
  }
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
