<template>
  <div class="common-layout">
    <el-container class="full-height">
      <el-header class="header">
        <div class="header-content">
          <div class="left-content">
            <p>Assigned ID:</p>
            <p class="id">{{ formData.id }}</p>
          </div>
          <div class="right-content">
            <el-button plain @click="dialogVisible = true">Open Instructions</el-button>
          </div>
        </div>
      </el-header>
      <el-main>
        <el-card class="main-card">
          <div class="top">
            <el-card class="top-card" shadow="never">
              <div v-html="Svg" class="svg-container"></div>
            </el-card>
            <el-card class="group-card" shadow="never">
              <div class="select-group">
                <el-select v-model="selectedGroup" placeholder="Select Group">
                  <el-option v-for="(group, index) in groupOptions" :key="index" :label="group" :value="group" />
                </el-select>
                <el-button @click="addNewGroup"><el-icon>
                    <Plus />
                  </el-icon></el-button>
              </div>
              <div v-for="(nodes, group) in filteredGroups" :key="group" class="group">
                <h3>{{ group }}</h3>
                <el-scrollbar height="240px">
                  <div class="group-tags">
                    <el-tag v-for="node in nodes" :key="node" closable @close="removeFromGroup(group, node)">
                      {{ node }}
                    </el-tag>
                  </div>
                </el-scrollbar>
                <el-rate v-if="selectedGroup !== 'allgroup'" v-model="ratings[group]" allow-half />
              </div>
            </el-card>
          </div>
          <el-card class="bottom-card" shadow="never">
            <div ref="chartContainer" class="chart-container"></div>
          </el-card>
        </el-card>
      </el-main>
      <div class="op-buttons">
        <el-button style="margin-top: 12px" @click="Previous">Previous one</el-button>
        <el-button style="margin-top: 12px" @click="next" type="primary" v-if="active != steps.length - 1">Next one</el-button>
        <el-button style="margin-top: 12px" @click="submit" type="success" v-if="active === steps.length - 1">Submit</el-button>
      </div>
      <el-divider border-style="double" />
      <el-footer>
        <el-steps :active="active" finish-status="success" class="steps">
          <el-step v-for="(step, index) in steps" :key="index" />
        </el-steps>
      </el-footer>
    </el-container>

    <el-dialog v-model="dialogVisible" title="Questionnaire Instructions" width="700" align-center>
      <span>
        Please read the following instructions carefully before starting the questionnaire:
        <ol>
          <li>(❁´◡`❁)</li>
          <li>(～￣▽￣)～</li>
          <li>╰(*°▽°*)╯</li>
        </ol>
      </span>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="handleDialogConfirm">I Understand</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import * as d3 from 'd3';
import { Plus } from '@element-plus/icons-vue';

const store = useStore();
const router = useRouter();
const formData = computed(() => store.getters.getFormData);
const selectedNodeIds = computed(() => store.state.selectedNodes.nodeIds);
const allVisiableNodes = computed(() => store.state.AllVisiableNodes);
const dialogVisible = ref(false);
const active = ref(0);
const steps = Array.from({ length: 3 });

const Svg = ref('');
const selectedGroup = ref('group1');
const ratings = ref({});

const fetchSvgContent = async (step) => {
  try {
    const svgModule = await import(`../../public/Data/${step}/${step}.svg?raw`);
    Svg.value = svgModule.default;
  } catch (error) {
    console.error('Error loading SVG content:', error);
    Svg.value = '<svg><text x="10" y="20" font-size="20">Error loading SVG</text></svg>';
  }
};

const eleURL = computed(() => {
  const step = active.value + 1;
  return `../../public/Data/${step}/layer_data.json`;
});

const chartContainer = ref(null);

const customColorMap = {
  "rect": "#E6194B",
  "path": "#3CB44B",
  "circle": "#FFE119",
  "line": "#4363D8",
  "polygon": "#F58231",
  "polyline": "#911EB4",
  "text": "#46F0F0",
  "ellipse": "#F032E6",
  "image": "#BCF60C",
  "clipPath": "#FABEBE",
};

const handleDialogConfirm = () => {
  dialogVisible.value = false;
};

const next = async () => {
  if (active.value < steps.length - 1) {
    selectedGroup.value = 'group1'
    active.value++;
    await fetchSvgContent(active.value + 1);
    fetchAndRenderTree();
    ensureGroupInitialization();
  }
};

const Previous = async () => {
  if (active.value > 0) {
    selectedGroup.value = 'group1'
    active.value--;
    await fetchSvgContent(active.value + 1);
    fetchAndRenderTree();
    ensureGroupInitialization();
  }
};

const submit = () => {
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

  const color = d3.scaleOrdinal(data.children.map(d => d.name), d3.schemeTableau10);

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

  // Update all visible nodes
  const nodeIds = [];
  leaf.each(d => {
    nodeIds.push(d.data.name.split("/").pop());
  });
  store.commit('UPDATE_ALL_VISIABLE_NODES', nodeIds);

  leaf.append("title")
    .text(d => d.data.name.split("/").pop());

  leaf.append("rect")
    .attr("fill", d => {
      const lastName = d.data.name.split("/").pop();
      const nameWithoutNumber = lastName.replace(/_.*$/, '');
      return customColorMap[nameWithoutNumber] || "#000";
    })
    .attr("fill-opacity", 0.6)
    .attr("width", d => d.x1 - d.x0)
    .attr("height", d => d.y1 - d.y0)
    .attr('stroke-width', 0.3)
    .attr("style", "cursor: pointer;")
    .on("mouseover", function (event, d) {
      const nodeName = d.data.name.split("/").pop();
      store.commit('UPDATE_SELECTED_NODES', { nodeIds: [nodeName], group: null });
    })
    .on("mouseout", function () {
      const svgContainer = document.querySelector('.svg-container');
      if (!svgContainer) return;
      const svg = svgContainer.querySelector('svg');
      if (!svg) return;
      svg.querySelectorAll('*').forEach(node => {
        node.style.opacity = '1';
      });
    })
    .on("click", function (event, d) {
      const nodeId = d.data.name.split("/").pop();
      addToGroup(nodeId);
    });

  leaf.append("text")
    .attr("x", 3)
    .attr("pointer-events", "none")
    .attr("y", "1em")
    .text(d => abbreviateText(d.data.name.split("/").pop(), d.x1 - d.x0, 10))
    .append("title")
    .text(d => d.data.name.split("/").pop());

  function abbreviateText(text, maxWidth, fontSize) {
    const avgCharWidth = fontSize * 0.7;
    const maxChars = Math.floor(maxWidth / avgCharWidth);

    if (text.length > maxChars) {
      return text.substr(0, maxChars - 1) + "…";
    }
    return text;
  }
};

const addToGroup = (nodeId) => {
  const step = active.value;
  store.commit('ADD_NODE_TO_GROUP', { step, group: selectedGroup.value, nodeId });
};

const removeFromGroup = (group, nodeId) => {
  const step = active.value;
  store.commit('REMOVE_NODE_FROM_GROUP', { step, group, nodeId });
};

const addNewGroup = () => {
  const step = active.value;
  const newGroup = `group${Object.keys(groups.value).length + 1}`;
  store.commit('ADD_NEW_GROUP', { step, group: newGroup });
  selectedGroup.value = newGroup;
};

const groups = computed(() => store.getters.getGroups(active.value));

const filteredGroups = computed(() => {
  if (selectedGroup.value === 'allgroup') {
    return groups.value;
  }
  return {
    [selectedGroup.value]: groups.value[selectedGroup.value] || []
  };
});

const groupOptions = computed(() => ['allgroup', ...Object.keys(groups.value)]);

const ensureGroupInitialization = () => {
  const step = active.value;
  if (!groups.value['group1']) {
    store.commit('ADD_NEW_GROUP', { step, group: 'group1' });
  }
};

onMounted(async () => {
  dialogVisible.value = true;
  await fetchSvgContent(active.value + 1);
  fetchAndRenderTree();
  ensureGroupInitialization(); // Initialize with group1
});

watch(active, async () => {
  await fetchSvgContent(active.value + 1);
  fetchAndRenderTree();
  ensureGroupInitialization();
});

watch(selectedNodeIds, () => {
  const svgContainer = document.querySelector('.svg-container');
  if (!svgContainer) return;
  const svg = svgContainer.querySelector('svg');
  if (!svg) return;
  svg.querySelectorAll('*').forEach(node => {
    node.style.opacity = '1';
  });
  svg.querySelectorAll('*').forEach(node => {
    if (allVisiableNodes.value.includes(node.id) && !selectedNodeIds.value.includes(node.id)) {
      node.style.opacity = '0.2';
    }
  });
});
</script>

<style scoped>
.group-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 300px;

  .select-group {
    display: flex;
    align-items: center;

    .el-select {
      margin-right: 10px;
      width: 110px;
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
      width: 100%;

      .el-tag {
        margin: 5px;
        flex: 1 0 calc(33.33% - 10px);
        max-width: calc(33.33% - 10px);
        box-sizing: border-box;
        text-align: center;
      }
    }
  }
}

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
}

.right-content {
  display: flex;
  align-items: center;
}

.id {
  font-size: 18px;
  font-weight: bold;
}

.el-main {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  flex-direction: column;
}

.el-footer {
  --el-footer-height: 50px;
}

.main-card {
  display: flex;
  flex-direction: column;
  padding: 0;
  margin: 0;
  width: 100%;
  height: 100%;

  .top {
    display: flex;
    flex-direction: row;
    margin-bottom: 20px;
    width: 100%;
  }

  .top-card {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 50%;
    flex-grow: 1;
    margin-right: 20px;

    .el-card__body {
      height: 100%;
      width: 100%;
    }
  }

  .bottom-card {
    display: flex;
    justify-content: center;
    align-items: center;
  }
}

.svg-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.chart-container {
  width: 1300px;
  height: 300px;
  overflow: hidden;
}

.op-buttons {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}
</style>
