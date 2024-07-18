import { createRouter, createWebHistory } from 'vue-router'
import QuestionnaireView from '../views/QuestionnaireView.vue'
import Questions from '../views/Questions.vue'
import Thanks from '../views/Thanks.vue'
import QuestionTest from '../views/QuestionTest.vue'
import showData from '../views/showData.vue'

const routes = [
  {
    path: '/',
    name: 'Questionnaire',
    component: QuestionnaireView
  },
  {
    path: '/questionstest',
    name: 'Questionstest',
    component: QuestionTest
  }
  ,
  {
    path: '/questions',
    name: 'Questions',
    component: Questions
  },
  {
    path: '/thanks',
    name: 'Thanks',
    component: Thanks
  },
  {
    path: '/showdata',
    name: 'showData',
    component: showData
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
