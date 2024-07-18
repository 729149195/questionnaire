import { createStore } from 'vuex';

const generateRandomId = () => {
  return Math.floor(100000 + Math.random() * 900000).toString();
};

const store = createStore({
  state() {
    return {
      formData: {},
      selectedNodes: {
        nodeIds: [],
        group: null
      },
      AllVisiableNodes: [],
      groups: {},
      ratings: {},
      startTime: null, // Track start time for calculating duration
      totalTimeSpent: 0 // Total time spent in seconds
    };
  },
  mutations: {
    setFormData(state, data) {
      state.formData = { ...data, id: generateRandomId() };
      state.startTime = new Date().toISOString();
    },
    UPDATE_SELECTED_NODES(state, payload) {
      state.selectedNodes.nodeIds = payload.nodeIds;
      state.selectedNodes.group = payload.group;
    },
    UPDATE_ALL_VISIABLE_NODES(state, nodeIds) {
      state.AllVisiableNodes = nodeIds;
    },
    ADD_NODE_TO_GROUP(state, payload) {
      const { step, group, nodeId } = payload;
      if (!state.groups[step]) {
        state.groups[step] = {};
      }
      if (!state.groups[step][group]) {
        state.groups[step][group] = [];
      }
      if (!state.groups[step][group].includes(nodeId)) {
        state.groups[step][group].push(nodeId);
      }
    },
    REMOVE_NODE_FROM_GROUP(state, payload) {
      const { step, group, nodeId } = payload;
      const index = state.groups[step]?.[group]?.indexOf(nodeId);
      if (index !== -1) {
        state.groups[step][group].splice(index, 1);
      }
    },
    ADD_NEW_GROUP(state, payload) {
      const { step, group } = payload;
      if (!state.groups[step]) {
        state.groups[step] = {};
      }
      if (!state.groups[step][group]) {
        state.groups[step][group] = [];
      }
    },
    UPDATE_RATING(state, payload) {
      const { step, group, rating } = payload;
      if (!state.ratings[step]) {
        state.ratings[step] = {};
      }
      state.ratings[step][group] = rating;
    },
    ADD_OTHER_GROUP(state, payload) {
      const { step, group, nodeIds } = payload;
      if (!state.groups[step]) {
        state.groups[step] = {};
      }
      state.groups[step][group] = nodeIds;
    },
    DELETE_GROUP(state, payload) {
      const { step, group } = payload;
      if (state.groups[step] && state.groups[step][group]) {
        delete state.groups[step][group];
        // Reassign groups and ratings
        const newGroups = {};
        const newRatings = {};
        Object.keys(state.groups[step]).forEach((grp, idx) => {
          const newGroup = `group${idx + 1}`;
          newGroups[newGroup] = state.groups[step][grp];
          newRatings[newGroup] = state.ratings[step][grp];
        });
        state.groups[step] = newGroups;
        state.ratings[step] = newRatings;
      }
    },
    RESET_TRAINING_DATA(state) {
      state.selectedNodes.nodeIds = [];
      state.AllVisiableNodes = [];
      state.groups = {};
      state.ratings = {};
    },
    UPDATE_TOTAL_TIME_SPENT(state, time) {
      state.totalTimeSpent = time;
    }
  },
  actions: {
    submitForm({ commit }, data) {
      commit('setFormData', data);
    },
  },
  getters: {
    getFormData: (state) => state.formData,
    getGroups: (state) => (step) => state.groups[step] || {},
    getRating: (state) => (step, group) => state.ratings[step]?.[group] || 1,
    getTotalTimeSpent: (state) => state.totalTimeSpent
  },
});

export default store;
