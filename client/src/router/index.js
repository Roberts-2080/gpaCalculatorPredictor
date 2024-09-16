import { createRouter, createWebHistory } from 'vue-router'
import Rank from '../views/Rank.vue'
import Predict from '../views/Predict.vue'
import ToPredict from '../views/ToPredict.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/rank'
    },
    {
      path: '/rank',
      name: 'Rank',
      component: Rank
    },
    {
      path: '/predict',
      name: 'Predict',
      component: Predict
    },
    {
      path: '/to_predict',
      name: 'ToPredict',
      component: ToPredict
    },
  ]
})

export default router
