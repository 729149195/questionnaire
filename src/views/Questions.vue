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
          <!-- <div class="right-content">
            <el-button plain @click="infoDialogVisible = true">打开说明<el-icon style='margin-left:5px'>
                <WindPower />
              </el-icon></el-button>
          </div> -->
        </div>
      </el-header>
      <el-main>
        <el-card class="main-card">
          <div style="display: flex;">
            <div class="left-two">
              <el-card class="top-card" shadow="never">
                <div v-html="Svg" class="svg-container"></div>
                <el-button class="top-title" disabled text bg>组合观察区域</el-button>
              </el-card>
              <el-card class="bottom-card" shadow="never">
                <div ref="chartContainer" class="chart-container" v-show="false"></div>
                <div v-html="Svg" class="svg-container2" ref="svgContainer2"></div>
                <el-button @click="toggleCropMode" class="Crop"><el-icon>
                    <Crop />
                  </el-icon></el-button>
                <el-button @click="toggleTrackMode" class="track"><el-icon>
                    <Pointer />
                  </el-icon></el-button>
                <el-button class="bottom-title" disabled text bg>选取交互区域</el-button>
              </el-card>
            </div>
            <el-card class="group-card" shadow="never">
              <div class="select-group">
                <el-select v-model="selectedGroup" placeholder="选择组合" @change="highlightGroup">
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
                <el-scrollbar height="500px">
                  <div class="group-tags">
                    <el-tag v-for="node in currentGroupNodes" :key="node" closable
                      @close="removeFromGroup(selectedGroup, node)" @mousedown="highlightElement(node)"
                      @mouseup="resetHighlight">
                      {{ node }}
                    </el-tag>
                  </div>
                </el-scrollbar>
                <div v-if="ratings[selectedGroup]" ref="rateings" class="rate-container">
                  <el-tooltip class="box-item" effect="dark" content="越先被注意到的组合评分越高" placement="right">
                    <div class="rate-container2">
                      <div class="rate-text">显眼程度：</div>
                      <el-rate :icons="icons" :void-icon="Hide" :colors="['#409eff', '#67c23a', '#FF9900']" :max="3"
                        :texts="['低', '中', '高']" show-text v-model="ratings[selectedGroup].attention" class="rate"
                        @change="updateRating(selectedGroup, ratings[selectedGroup].attention, 'attention')" />
                    </div>
                  </el-tooltip>
                  <el-tooltip class="box-item" effect="dark" content="组合中不可缺少的元素占比越高评分越高" placement="right">
                    <div class="rate-container2">
                      <div class="rate-text">分组组内元素的关联强度：</div>
                      <el-rate :icons="icons" :void-icon="Hide" :colors="['#409eff', '#67c23a', '#FF9900']" :max="3"
                        :texts="['低', '中', '高']" show-text v-model="ratings[selectedGroup].correlation_strength"
                        class="rate"
                        @change="updateRating(selectedGroup, ratings[selectedGroup].correlation_strength, 'correlation_strength')" />
                    </div>
                  </el-tooltip>
                  <el-tooltip class="box-item" effect="dark" content="组外可以划分到该组的元素越少评分越高" placement="right">
                    <div class="rate-container2">
                      <div class="rate-text">分组对组外元素的排斥程度：</div>
                      <el-rate :icons="icons" :void-icon="Hide" :colors="['#409eff', '#67c23a', '#FF9900']" :max="3"
                        :texts="['低', '中', '高']" show-text v-model="ratings[selectedGroup].exclusionary_force"
                        class="rate"
                        @change="updateRating(selectedGroup, ratings[selectedGroup].exclusionary_force, 'exclusionary_force')" />
                    </div>
                  </el-tooltip>
                </div>
              </div>
            </el-card>
          </div>
        </el-card>
        <div class="steps-container">
          <el-button class="previous-button" @click="Previous"><el-icon>
              <CaretLeft />
            </el-icon></el-button>
          <el-steps :active="active" finish-status="success" class="steps">
            <el-step v-for="(step, index) in steps" :key="index" @click.native="goToStep(index)" />
          </el-steps>
          <el-button class="next-button" @click="next" type="primary" v-if="active != steps.length - 1"><el-icon>
              <CaretRight />
            </el-icon></el-button>
          <el-button class="submit-button" @click="submit" type="success"
            v-if="active === steps.length - 1"><el-icon><Select /></el-icon></el-button>
        </div>
      </el-main>

    </el-container>

    <el-dialog v-model="dialogVisible" title="提醒" width="700" align-center @close="handleDialogClose"
      :close-on-click-modal="false">
      <span>
        您已经做了15分钟了，可以稍微闭眼休息一下哦~。
      </span>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">我知道了</el-button>
        </div>
      </template>
    </el-dialog>

    <el-dialog 
      v-model="infoDialogVisible" 
      title="问卷说明" 
      width="800" 
      align-center
      :close-on-click-modal="false"
      class="info-dialog"
    >
      <div class="info-content">
        <h3 class="info-subtitle">在正式开始问卷之前，请仔细阅读以下说明：</h3>
        <ol class="info-list">
          <li>请尽可能多地选出自己认为的合理的图形组合</li>
          <li>这些图形组合大概率会产生重叠，即同一个元素可以同时属于多个图形组合</li>
          <li>虽然显眼程度和分组界限的评分很重要，但请不要过多思考分析，尽量遵循自己的第一印象来进行打分</li>
        </ol>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="infoDialogVisible = false" class="confirm-btn">我已了解</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
  <el-card class="flow">
    <template #header>
      <div class="flow-header">
        <span class="flow-title">操作流程提示</span>
      </div>
    </template>
    <div class="flow-content">
      <div class="step-item">
        <span class="step-number">步骤1:</span>
        <el-card class="step-card" shadow="hover">
          <p>查看组合观察区域（左上角板块）并记下感知到的元素组合。</p>
        </el-card>
      </div>
      <div class="step-item">
        <span class="step-number">步骤2:</span>
        <el-card class="step-card" shadow="hover">
          <p>在选取交互区域选择您感知中可以组成一个组合的所有元素</p>
          <ul class="step-list">
            <li>组合元素较密集的时候，建议使用框选或路径选择功能批量选区元素</li>
            <li>已经被选中的元素再次被选择后，会取消选中状态</li>
            <li>鼠标滚轮可以对互区域选择放大缩小交</li>
          </ul>
        </el-card>
      </div>
      <div class="step-item">
        <span class="step-number">步骤3:</span>
        <el-card class="step-card" shadow="hover">
          <p>选取完一个组后，若还有其他组合未添加，点击组合板块的加号按钮创建新组。</p>
        </el-card>
      </div>
      <div class="step-item">
        <span class="step-number">步骤4:</span>
        <el-card class="step-card" shadow="hover">
          <p>每组元素选完后不要忘记评���嗷~</p>
        </el-card>
      </div>
    </div>
  </el-card>
  <el-card class="flow2">
    <template #header>
      <div class="flow-header">
        <span class="flow-title">友情提示</span>
      </div>
    </template>
    <div class="tips-content">
      <ul class="tips-list">
        <li>请尽可能多地选出自己感知到的图形组合</li>
        <li>相同的元素在不同的组合中可以重复选择</li>
        <li>尽量遵循自己的第一印象</li>
      </ul>
    </div>
  </el-card>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import * as d3 from 'd3';
import { Delete, Plus, Hide, View, CaretLeft, CaretRight, Select, WindPower, Crop, Pointer } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import { getSubmissionCount } from '../api/counter';

const store = useStore();
const router = useRouter();
// const formData = computed(() => store.getters.getFormData);
const selectedNodeIds = computed(() => store.state.selectedNodes.nodeIds);
const allVisiableNodes = computed(() => store.state.AllVisiableNodes);
const steps = computed(() => store.state.steps);
const dialogVisible = ref(false);
const infoDialogVisible = ref(true);
const active = ref(0);
const icons = [View, View, View];
const svgContainer2 = ref(null);

const Svg = ref('');
const selectedGroup = ref('组合1');
const ratings = ref({});
let reminderTimerId = null;
const nodeEventHandlers = new Map();
const isCropping = ref(false);
const isTracking = ref(false);

const goToStep = async (index) => {
  if (index !== active.value) {
    selectedGroup.value = '组合1';
    active.value = index;
    await fetchSvgContent(active.value + 1); // 加载对应步骤的SVG内容
    await fetchAndRenderTree(); // 加载对应步骤的树形结构
    ensureGroupInitialization(); // 确保组合初始化
    nextTick(() => {
      highlightGroup(); // 确保组合在初始加载时被高亮
    });
    isCropping.value = false;
    svgContainer2.value.classList.remove('crosshair-cursor');
    await loadExampleData();
  }
};


const currentGroupNodes = computed(() => {
  if (!ratings.value[selectedGroup.value]) {
    ratings.value[selectedGroup.value] = { attention: 1, correlation_strength: 1, exclusionary_force: 1 };
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

  // 创建一个包裹实际SVG内容的组
  let g = svg.select('g.zoom-wrapper');
  if (g.empty()) {
    g = svg.append('g').attr('class', 'zoom-wrapper');
    // 将所有现有内容移动到新的组中
    const children = svg.node().childNodes;
    [...children].forEach(child => {
      if (child.nodeType === 1 && !child.classList.contains('zoom-wrapper')) {
        g.node().appendChild(child);
      }
    });
  }

  const zoom = d3.zoom()
    .scaleExtent([0.5, 10])
    .on('zoom', (event) => {
      if (!isCropping.value) {
        g.attr('transform', event.transform);
      }
    });

  svg.call(zoom);

  // 获取参考 SVG 的位置和尺寸
  const referenceSvg = d3.select('.svg-container svg');
  if (referenceSvg.node()) {
    // 获取两个 SVG 的 viewBox
    const refViewBox = referenceSvg.node().viewBox.baseVal;
    const currentViewBox = svg.node().viewBox.baseVal;

    // 获取实际显示尺寸
    const refRect = referenceSvg.node().getBoundingClientRect();
    const currentRect = svg.node().getBoundingClientRect();

    // 计算缩放比例
    const scaleX = (refRect.width / refViewBox.width) / (currentRect.width / currentViewBox.width);
    const scaleY = (refRect.height / refViewBox.height) / (currentRect.height / currentViewBox.height);
    const scale = Math.min(scaleX, scaleY);

    // 计算偏移量，使两个 SVG 的内容对齐
    const refCenterX = refViewBox.x + refViewBox.width / 2;
    const refCenterY = refViewBox.y + refViewBox.height / 2;
    const currentCenterX = currentViewBox.x + currentViewBox.width / 2;
    const currentCenterY = currentViewBox.y + currentViewBox.height / 2;

    const translateX = (refCenterX - currentCenterX) * scale + (refRect.width - currentRect.width * scale) / 2;
    const translateY = (refCenterY - currentCenterY) * scale + (refRect.height - currentRect.height * scale) / 2;

    // 应用变换
    const initialTransform = d3.zoomIdentity
      .translate(translateX, translateY)
      .scale(scale);

    svg.call(zoom.transform, initialTransform);
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
    if (isTracking.value) {
      isTracking.value = false;
      svgContainer2.value.classList.remove('copy-cursor');
      ElMessage.info('退出路径模式');
      disableTrackMode();
    }
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

const toggleTrackMode = () => {
  isTracking.value = !isTracking.value;
  const svg = d3.select(svgContainer2.value).select('svg');
  if (isTracking.value) {
    nextTick(() => {
      svgContainer2.value.classList.add('copy-cursor');
    });
    if (isCropping.value) {
      isCropping.value = false;
      svgContainer2.value.classList.remove('crosshair-cursor');
      ElMessage.info('退出选框模式');
      disableCropSelection();
    }
    ElMessage.info('进入路径模式');
    enableTrackMode();
    svg.on('.zoom', null); // 禁用缩放事件
  } else {
    svgContainer2.value.classList.remove('copy-cursor');
    ElMessage.info('退出路径组模式');
    disableTrackMode();
    addZoomEffectToSvg(); // 重新启用缩放功能
  }
};

const enableTrackMode = () => {
  let isMouseDown = false;
  let clickedElements = new Set();
  const svg = svgContainer2.value.querySelector('svg');

  const handleMouseDown = () => {
    isMouseDown = true;
    clickedElements.clear(); // 重置点击元素集合
  };

  const handleMouseUp = () => {
    isMouseDown = false;
  };

  const handleMouseMove = (event) => {
    if (isMouseDown) {
      const point = svg.createSVGPoint();
      point.x = event.clientX;
      point.y = event.clientY;
      const svgPoint = point.matrixTransform(svg.getScreenCTM().inverse());

      const node = document.elementFromPoint(event.clientX, event.clientY);
      if (node && allVisiableNodes.value.includes(node.id) && !clickedElements.has(node)) {
        clickedElements.add(node); // 记录已点击的元素
        node.dispatchEvent(new Event('click', { bubbles: true })); // 模拟点击事件
      }
    }
  };

  svg.addEventListener('mousedown', handleMouseDown);
  svg.addEventListener('mouseup', handleMouseUp);
  svg.addEventListener('mousemove', handleMouseMove);

  nodeEventHandlers.set(svg, { handleMouseDown, handleMouseUp, handleMouseMove });
};

const disableTrackMode = () => {
  const svg = svgContainer2.value.querySelector('svg');
  if (svg) {
    const handlers = nodeEventHandlers.get(svg);
    if (handlers) {
      svg.removeEventListener('mousedown', handlers.handleMouseDown);
      svg.removeEventListener('mouseup', handlers.handleMouseUp);
      svg.removeEventListener('mousemove', handlers.handleMouseMove);
    }
    nodeEventHandlers.delete(svg);
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
      // if(isCropping.value === false && isTracking.value === false){
      // node.style.cursor = 'pointer';
      // }
      // node.style.cursor = 'pointer';
    }
  });
};
//isTracking.valueisCropping.value
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
  selectedGroup.value = '组合1';
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
  const count = await getSubmissionCount();
  if (count >= 5) {
    router.push('/limit-reached');
    return;
  }

  if (steps.value && active.value < steps.value.length - 1) {
    selectedGroup.value = '组合1';
    active.value++;
    await fetchSvgContent(steps.value[active.value]);
    await fetchAndRenderTree();
    ensureGroupInitialization();
    nextTick(() => {
      highlightGroup();
    });
    isCropping.value = false;
    svgContainer2.value.classList.remove('crosshair-cursor');
    svgContainer2.value.classList.remove('copy-cursor');
  }
};

const Previous = async () => {
  const count = await getSubmissionCount();
  if (count >= 5) {
    router.push('/limit-reached');
    return;
  }

  if (steps.value && active.value > 0) {
    selectedGroup.value = '组合1';
    active.value--;
    await fetchSvgContent(steps.value[active.value]);
    await fetchAndRenderTree();
    ensureGroupInitialization();
    nextTick(() => {
      highlightGroup();
    });
    isCropping.value = false;
    svgContainer2.value.classList.remove('crosshair-cursor');
    svgContainer2.value.classList.remove('copy-cursor');
  }
};

const submit = () => {
  const count = getSubmissionCount();
  if (count >= 5) {
    router.push('/limit-reached');
    return;
  }

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
  const newGroup = `组合${Object.keys(groups.value).length + 1}`;
  store.commit('ADD_NEW_GROUP', { step, group: newGroup });
  selectedGroup.value = newGroup;
  ratings.value[newGroup] = { attention: 1, correlation_strength: 1, exclusionary_force: 1 };
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
      ratings.value[group] = { attention: 1, correlation_strength: 1, exclusionary_force: 1 };
    }
  }
  return result;
});

const groupOptions = computed(() => Object.keys(groups.value));

const ensureGroupInitialization = () => {
  const step = active.value;
  if (!groups.value['组合1']) {
    store.commit('ADD_NEW_GROUP', { step, group: '组合1' });
    ratings.value['组合1'] = { attention: 1, correlation_strength: 1, exclusionary_force: 1 };
  }
};

const generateRandomArray = () => {
  const numbers = Array.from({ length: 53 }, (_, index) => index + 1);
  const randomArray = [];
  while (randomArray.length < 10) {
    const randomIndex = Math.floor(Math.random() * numbers.length);
    const number = numbers.splice(randomIndex, 1)[0];
    randomArray.push(number);
  }
  return randomArray;
};

onMounted(async () => {
  const count = await getSubmissionCount();
  if (count >= 5) {
    router.push('/limit-reached');
  }
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
    ratings.value[group] = stepRatings[group] || { attention: 1, correlation_strength: 1, exclusionary_force: 1 };
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
  height: 98vh;
  width: 70vw;
  margin: auto;
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

.main-card {
  width: 100%;
  height: auto;

  .left-two {
    display: flex;
    flex-direction: column;
    width: 200%;
    margin-right: 10px;

    .top-card {
      margin-bottom: 10px;
      height: 100%;
    }

    .bottom-card {
      position: relative;
      height: 105%;

      .Crop {
        position: absolute;
        top: 10px;
        right: 10px;
      }

      .track {
        position: absolute;
        top: 10px;
        right: 65px;
      }

      .bottom-title {
        position: absolute;
        top: 5px;
        left: -15px;
      }
    }
  }

  .group-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    height: auto;

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
          box-sizing: border-box;
          text-align: center;
          cursor: pointer;
        }
      }
    }
  }
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

.copy-cursor {
  cursor: copy !important;
}

.flow {
  position: absolute;
  left: 10px;
  top: 100px;
  width: 15vw;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.flow2 {
  position: absolute;
  right: 10px;
  top: 100px;
  width: 15vw;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.flow-header {
  padding: 0;
  margin: 0;
}

.flow-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.flow-content {
  padding: 10px 0;
}

.step-item {
  margin-bottom: 15px;
}

.step-number {
  display: block;
  font-size: 14px;
  color: #409EFF;
  margin-bottom: 8px;
  font-weight: 500;
}

.step-card {
  margin: 0;
  border: none;
  background-color: #f5f7fa;
  
  :deep(.el-card__body) {
    padding: 12px;
  }

  p {
    margin: 0;
    font-size: 14px;
    color: #606266;
    line-height: 1.6;
  }
}

.step-list {
  margin: 8px 0 0 0;
  padding-left: 20px;
  
  li {
    color: #606266;
    font-size: 13px;
    line-height: 1.6;
    margin-bottom: 4px;
    
    &:last-child {
      margin-bottom: 0;
    }
  }
}

.tips-content {
  padding: 5px 0;
}

.tips-list {
  margin: 0;
  padding-left: 20px;
  
  li {
    color: #606266;
    font-size: 14px;
    line-height: 1.8;
    margin-bottom: 8px;
    
    &:last-child {
      margin-bottom: 0;
    }
  }
}

.buzhou {
  font-size: 12px;
  color: #999;
}

.rate-container2 {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin: 10px 0;
}

.rate-text {
  text-align: left;
  min-width: 200px;
}

.rate {
  margin-left: auto;
}

.info-dialog :deep(.el-dialog__header) {
  padding: 20px;
  margin-right: 0;
  background-color: #f5f7fa;
  border-bottom: 1px solid #e4e7ed;
}

.info-dialog :deep(.el-dialog__title) {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.info-content {
  padding: 30px 20px;
}

.info-subtitle {
  font-size: 16px;
  color: #606266;
  margin: 0 0 20px 0;
  font-weight: 500;
}

.info-list {
  margin: 0;
  padding-left: 25px;
}

.info-list li {
  color: #606266;
  line-height: 2;
  margin-bottom: 15px;
  font-size: 15px;
  position: relative;
  padding-left: 5px;
}

.info-list li:last-child {
  margin-bottom: 0;
}

.dialog-footer {
  padding: 20px;
  text-align: right;
  background-color: #f5f7fa;
  border-top: 1px solid #e4e7ed;
}

.confirm-btn {
  padding: 12px 25px;
  font-size: 14px;
}

.info-dialog :deep(.el-dialog) {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.info-dialog :deep(.el-dialog__body) {
  padding: 0;
}

.svg-container, .svg-container2 {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.svg-container svg, .svg-container2 svg {
  width: 100%;
  height: 100%;
  display: block;
}
</style>
