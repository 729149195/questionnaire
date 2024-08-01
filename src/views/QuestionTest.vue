<template>
  <div class="common-layout">
    <el-container class="full-height">
      <el-header class="header">
        <div class="header-content">
          <div ref="idandtime" class="left-content">
            <!-- <p class="id">分配ID：666666</p> -->
            <a href="https://github.com/729149195/questionnaire" target="_blank">
              <img style="width: 30px;" src="/img/favicon.png" alt="Wechat QR Code">
            </a>
          </div>
          <div class="right-content">
            <el-button ref="openDialogBtn" plain @click="infoDialogVisible = true">
              打开说明<el-icon style='margin-left:5px'>
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
              <el-card ref="svg1" class="top-card" shadow="never">
                <div v-html="Svg" class="svg-container"></div>
                <el-button class="top-title" disabled text bg>模式观察区域</el-button>
              </el-card>
              <el-card ref="svg2" class="bottom-card" shadow="never">
                <div v-html="Svg" class="svg-container2" ref="svgContainer2"></div>
                <div ref="chartContainer" class="chart-container" v-show="false"></div>
                <el-button @click="toggleCropMode" class="Crop" ref="cropBtn"><el-icon>
                    <Crop />
                  </el-icon></el-button>
                  <el-button @click="toggleTrackMode" class="track" ref="trackBtn"><el-icon><Pointer /></el-icon></el-button>

                <el-button class="bottom-title" disabled text bg>选取交互区域</el-button>
              </el-card>
            </div>
            <el-card ref="groupCard" class="group-card" shadow="never">
              <div class="select-group">
                <el-select ref="groupSelector" v-model="selectedGroup" placeholder="选择模式" @change="highlightGroup">
                  <el-option v-for="(group, index) in groupOptions" :key="index" :label="group" :value="group" />
                </el-select>
                <el-button ref="addGroupBtn" @click="addNewGroup"><el-icon>
                    <Plus />
                  </el-icon></el-button>
                <el-button ref="deleteGroupBtn" @click="deleteCurrentGroup"><el-icon>
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
        <el-button ref="previousBtn" class="previous-button" @click="Previous"><el-icon>
            <CaretLeft />
          </el-icon></el-button>
        <el-steps :active="active" finish-status="success" class="steps" ref="stepsContainer">
          <el-step v-for="(step, index) in steps" :key="index" />
        </el-steps>
        <el-button ref="nextBtn" class="next-button" @click="next" type="primary"
          v-if="active != steps.length - 1"><el-icon>
            <CaretRight />
          </el-icon></el-button>
          <el-tooltip content="进入正式问卷">
        <el-button class="submit-button" @click="submit" type="success"
          v-if="active === steps.length - 1"><el-icon><DArrowRight /></el-icon></el-button></el-tooltip>
      </div>
    </el-container>

    <el-dialog v-model="infoDialogVisible" title="问卷说明" width="1000" align-center>
      <span>
        在正式开始问卷之前，请仔细阅读以下说明：
        <ol>
          <!-- <li>图形模式：指由线条、形状、颜色等元素组成的视觉结构</li>
          <li>右侧模式N里对应的所有标签元素代表一个图形模式</li> -->
          <li>请尽可能多地选出自己认为的合理的图形模式</li>
          <li>图形模式大概率会产生重叠，即同一个元素可以同时属于多个图形模式</li>
          <li>虽然显眼程度和分组界限的评分很重要，但请不要过多思考分析，尽量遵循自己的第一印象来进行打分</li>
          <!-- <li>报酬获取方式：完成问卷后待系统自动将结果提交后，联系管理员并提交问卷ID，管理员审批后将根据完成情况及质量发放报酬（一般不会低于XX￥）</li> -->
        </ol>
      </span>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="infoDialogVisible = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>

    <el-dialog v-model="tourDialogVisible" title="漫游引导" width="500">
      <span>是否需要一个简单的系统使用指南？</span>
      <p>在指南中，您可以直接在高亮区域进行操作。</p>
      <span>如果您已经熟悉该问卷系统，可以选择跳过。</span>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="tourDialogVisible = false">跳过</el-button>
          <el-button @click="startTour">是</el-button>
        </div>
      </template>
    </el-dialog>

    <el-tour v-model="openTour">
      <el-tour-step :target="openDialogBtn?.$el" title="说明按钮">点击这里可以打开说明。<div v-html="getGifHtml('1.gif')"></div>
      </el-tour-step>
      <el-tour-step :target="svg1?.$el" title="模式观察区域" placement="right">您将在这里观察原图并进行图形模式的感知。</el-tour-step>
      <el-tour-step :target="svg2?.$el" placement="right" title="选取交互区域">
        在这里，您可以通过点击元素来添加或删除它们，以构建或修改当前的图形模式。您还可以使用鼠标滚轮进行缩放，以便更好地查看和选择细小的元素。<div v-html="getGifHtml('2.gif')"></div>
      </el-tour-step>
      <el-tour-step :target="cropBtn?.$el" placement="right" title="切换框选按钮"> 当遇到的图形模式中元素较为细小时，可以点击进入选框模式进行元素框选，被框选的元素相当于被点击一下，未被选中的被框选到会被选中，已选中的被框选到会取消选中（再次点击即可退出选框模式，选框模式下也可进行当个元素的点击）。<div
          v-html="getGifHtml('3.gif')"></div></el-tour-step>
      <el-tour-step :target="trackBtn?.$el" placement="right" title="切换路径选择按钮"> 当遇到的图形模式中元素较为密集时，可以点击进入路径选择模式进行元素路径选择，被按住的鼠标经过的元素相当于被点击一下（再次点击即可退出路径选择模式，选框模式下也可进行当个元素的点击）。<div
          v-html="getGifHtml('12.gif')"></div></el-tour-step>
      <el-tour-step :target="groupCard?.$el" title="分组卡片" placement="left">显示选中模式中所包含标签，以及一些操作按钮，点击蓝色标签后可在选取交互区域定位到单一标签所对应的元素，也可通过取消蓝色标签来移除对应元素。
        <div v-html="getGifHtml('4.gif')"></div>
      </el-tour-step>
      <el-tour-step :target="groupSelector?.$el" title="分组选择器">在这里可以下拉选择已创建的模式。<div v-html="getGifHtml('5.gif')"></div>
      </el-tour-step>
      <el-tour-step :target="addGroupBtn?.$el" title="添加分组按钮">点击这里可以添加新的模式。<div v-html="getGifHtml('6.gif')"></div>
      </el-tour-step>
      <el-tour-step :target="deleteGroupBtn?.$el" title="删除分组按钮"> 点击这里可以删除当前模式及其内容，后续模式的内容会往前覆盖同时继承被删除的模式编号。<div
          v-html="getGifHtml('7.gif')"></div></el-tour-step>
      <el-tour-step :target="rateings?.$el" title="模式评分">
        <p>显眼程度：您注意到这个图形模式的快慢。</p>
        <p>分组界限：该图形模式与其它潜在图形模式重叠的多少，重叠得越少，分组界限越清晰。</p>
        <p>请根据第一印象为每一个图形模式估计评分。</p>
        <div v-html="getGifHtml('8.gif')"></div>
        <p>例如：</p>
        <img style="width: 150%; margin-top: 10px" src="/img/example.png" alt="">
        <p>a对应的模式最为显眼，但与其它潜在模式的界限较模糊。</p>
        <p>b对应的模式比较显眼，但因模式中大部分节点都比较集中，因此与潜在模式的界限较为清晰（即与其余潜在模式重叠较少）。</p>
        <p>c对应的模式的显眼程度和分组界限恰好处于a和b之间。</p>
      </el-tour-step>
      <el-tour-step :target="stepsContainer?.$el" title="问卷进度">这里显示了问卷的进度。已完成的示例节点会变绿。<div v-html="getGifHtml('9.gif')">
        </div></el-tour-step>
      <el-tour-step :target="previousBtn?.$el" title="上一个按钮">点击这里可以回到上一个示例节点。<div v-html="getGifHtml('10.gif')"></div>
      </el-tour-step>
      <el-tour-step :target="nextBtn?.$el" title="下一个按钮">点击这里可以前往下一个示例节点。到最后一个节点时该按钮会变为绿色的提交按钮，点击后获取ID并导出图形模式数据。<div
          v-html="getGifHtml('11.gif')"></div></el-tour-step>
      <el-tour-step title="尝试">
        <p>现在可以使用当前示例进行练习</p>
        <p>并在对下一个示例已选好的模式进行浏览（仅供参考）</p>
      </el-tour-step>
    </el-tour>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import * as d3 from 'd3';
import { Delete, Plus, Hide, View, CaretLeft, CaretRight, DArrowRight, WindPower, Crop } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';

const store = useStore();
const router = useRouter();
const selectedNodeIds = computed(() => store.state.selectedNodes.nodeIds);
const allVisiableNodes = computed(() => store.state.AllVisiableNodes);
const dialogVisible = ref(false);
const tourDialogVisible = ref(false);
const infoDialogVisible = ref(false);
const openTour = ref(false);
const active = ref(0);
const steps = Array.from({ length: 2 });
const icons = [View, View, View];

// const formData = computed(() => store.getters.getFormData);
const svgContainer2 = ref(null);

const Svg = ref('');
const selectedGroup = ref('模式1');
const ratings = ref({});

const idandtime = ref(null);
const svg1 = ref(null);
const svg2 = ref(null);
const groupCard = ref(null);
const stepsContainer = ref(null);
const rateings = ref(null);
const openDialogBtn = ref(null);
const groupSelector = ref(null);
const addGroupBtn = ref(null);
const deleteGroupBtn = ref(null);
const previousBtn = ref(null);
const nextBtn = ref(null);
const cropBtn = ref(null);
const trackBtn = ref(null);
const nodeEventHandlers = new Map();
const isCropping = ref(false);
const isTracking = ref(false);


const props = defineProps(['data']);
const emits = defineEmits(['change', 'prev', 'next']);

const currentGroupNodes = computed(() => {
  if (!ratings.value[selectedGroup.value]) {
    ratings.value[selectedGroup.value] = { attention: 1, boundary: 1 };
  }
  return groups.value[selectedGroup.value] || [];
});

const getGifHtml = (filename) => {
  const gifPath = `./gif/${filename}`;
  return `<img src="${gifPath}" alt="GIF" style="max-width: 100%; height: auto;">`;
};

const updateRating = (group, rating, type) => {
  const step = active.value;
  store.commit('UPDATE_RATING', { step, group, rating, type });
};

// 加载并提交 example.json 数据
const loadExampleData = async () => {
  if (active.value === 1) {
    try {
      const response = await fetch(`./TestData/2/example.json`);
      if (!response.ok) {
        throw new Error('Failed to fetch example data');
      }
      const data = await response.json();

      data.groups.forEach((groupData, index) => {
        const groupName = `模式${index + 1}`;
        // console.log(groupData.ratings.boundary);

        store.commit('ADD_NEW_GROUP', { step: 1, group: groupName });
        store.commit('ADD_OTHER_GROUP', { step: 1, group: groupName, nodeIds: groupData[groupName] });
        store.commit('UPDATE_RATING', {
          step: 1,
          group: groupName,
          rating: groupData.ratings.attention,
          type: 'attention'
        });
        store.commit('UPDATE_RATING', {
          step: 1,
          group: groupName,
          rating: groupData.ratings.boundary,
          type: 'boundary'
        });
      });

      nextTick(() => {
        highlightGroup();
      });
    } catch (error) {
      console.error('Error loading example data:', error);
    }
  }
};


const fetchSvgContent = async (step) => {
  try {
    nodeEventHandlers.forEach((handler, node) => {
      node.removeEventListener('click', handler);
    });
    nodeEventHandlers.clear();

    const response = await fetch(`./TestData/${step}/${step}.svg`);
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
  await loadExampleData();  
};

const addZoomEffectToSvg = () => {
  const svgContainer = svgContainer2.value;
  if (!svgContainer) return;
  const svg = d3.select(svgContainer).select('svg');
  if (!svg) return;

  const zoom = d3.zoom()
    .scaleExtent([1, 10])
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
    if(isTracking.value){
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
    if(isCropping.value){
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
    ElMessage.info('退出路径模式');
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
      // node.style.cursor = 'pointer';
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
  const step = active.value + 1;
  return `./TestData/${step}/layer_data.json`;
});

const chartContainer = ref(null);

const next = async () => {
  if (active.value < steps.length - 1) {
    selectedGroup.value = '模式1';
    active.value++;
    await fetchSvgContent(active.value + 1);
    await fetchAndRenderTree();
    ensureGroupInitialization();
    nextTick(() => {
      highlightGroup();
    });
    isCropping.value = false;
    svgContainer2.value.classList.remove('crosshair-cursor');
    await loadExampleData();  
  }
};

const Previous = async () => {
  if (active.value > 0) {
    selectedGroup.value = '模式1';
    active.value--;
    await fetchSvgContent(active.value + 1);
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
  resetTrainingData();
  router.push('/questions');
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
};

const addToGroup = (nodeId) => {
  const step = active.value;
  store.commit('ADD_NODE_TO_GROUP', { step, group: selectedGroup.value, nodeId });
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

const resetTrainingData = () => {
  store.commit('RESET_TRAINING_DATA');
};

const startTour = () => {
  tourDialogVisible.value = false;
  openTour.value = true;
};

onMounted(async () => {
  tourDialogVisible.value = true; // Show the tour dialog on mount
  await fetchSvgContent(active.value + 1);
  await fetchAndRenderTree();
  ensureGroupInitialization();
});

onMounted(() => {
  const stepRatings = store.state.ratings[active.value] || {};
  for (const group in groups.value) {
    ratings.value[group] = stepRatings[group] || { attention: 1, boundary: 1 };
  }
  nextTick(() => {
    highlightGroup(); // Ensure the group is highlighted on initial load
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
  overflow: hidden;
}

.svg-container2 svg {
  width: 100%;
  height: 100%;
  cursor: pointer;
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

.drag-selection {
  position: absolute;
  border: 1px dashed #999;
  background-color: rgba(150, 150, 150, 0.3);
}

.crosshair-cursor {
  cursor: crosshair;
}

.copy-cursor {
  cursor: copy !important;
}

.rate-container {
  display: flex;
  flex-direction: column;
  font-size: 14px;

  .rate-container2 {
    display: flex;
    align-items: center;
  }
}

.bottom-card {
  position: relative;

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

.top-card {
  position: relative;

  .top-title {
    position: absolute;
    top: 5px;
    left: -5px;
  }
}
</style>
