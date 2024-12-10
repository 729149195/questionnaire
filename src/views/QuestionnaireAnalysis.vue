<template>
  <div class="questionnaire-analysis">
    <div class="control-panel">
      <div class="group-controls">
        <button 
          v-for="(group, index) in groups" 
          :key="index"
          :class="['group-btn', { active: currentGroup === index }]"
          @click="selectGroup(index)"
        >
          组 {{ index + 1 }}
        </button>
        <button @click="addNewGroup" class="add-group-btn">添加新组</button>
      </div>
    </div>

    <div class="svg-container">
      <div 
        v-for="(svgPath, index) in currentStepSvgs" 
        :key="index" 
        class="svg-item"
        :class="{ highlighted: isHighlighted(index) }"
        @click="toggleSelection(index)"
      >
        <img :src="svgPath" :alt="'Step ' + (index + 1)" />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import fs from 'fs'
import path from 'path'

export default {
  name: 'QuestionnaireAnalysis',
  setup() {
    const groups = ref([new Set()])
    const currentGroup = ref(0)
    const currentStepSvgs = ref([])
    const questionnaireData = ref(null)

    const loadQuestionnaireData = async () => {
      try {
        // 从newData2目录加载问卷数据
        const dataPath = path.join(process.cwd(), 'QuestionnaireData', 'newData2')
        const files = await fs.promises.readdir(dataPath)
        
        // 加载对应的SVG文件
        const svgFiles = files
          .filter(file => file.endsWith('.svg'))
          .map(file => `/QuestionnaireData/newData2/${file}`)
        currentStepSvgs.value = svgFiles
        
        // 加载问卷数据
        const stepFiles = files.filter(file => file.startsWith('stepID'))
        const data = {}
        for (const file of stepFiles) {
          const content = await fs.promises.readFile(path.join(dataPath, file), 'utf-8')
          data[file] = JSON.parse(content)
        }
        questionnaireData.value = data
      } catch (error) {
        console.error('加载问卷数据失败:', error)
      }
    }

    const selectGroup = (index) => {
      currentGroup.value = index
    }

    const addNewGroup = () => {
      groups.value.push(new Set())
      currentGroup.value = groups.value.length - 1
    }

    const toggleSelection = (index) => {
      const currentGroupSet = groups.value[currentGroup.value]
      if (currentGroupSet.has(index)) {
        currentGroupSet.delete(index)
      } else {
        currentGroupSet.add(index)
      }
    }

    const isHighlighted = (index) => {
      return groups.value[currentGroup.value].has(index)
    }

    onMounted(() => {
      loadQuestionnaireData()
    })

    return {
      groups,
      currentGroup,
      currentStepSvgs,
      selectGroup,
      addNewGroup,
      toggleSelection,
      isHighlighted
    }
  }
}
</script>

<style scoped>
.questionnaire-analysis {
  padding: 20px;
}

.control-panel {
  margin-bottom: 20px;
}

.group-controls {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.group-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
}

.group-btn.active {
  background: #4CAF50;
  color: white;
}

.add-group-btn {
  padding: 8px 16px;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.svg-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.svg-item {
  border: 2px solid transparent;
  padding: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.svg-item.highlighted {
  border-color: #4CAF50;
  background: rgba(76, 175, 80, 0.1);
}

.svg-item img {
  width: 100%;
  height: auto;
}
</style> 