import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterPage from '../views/RegisterPage.vue'
import LoginPage from '../views/LoginPage.vue'
import CreateSection from '@/views/CreateSection.vue'
import UpdateSection from '@/views/UpdateSection.vue'
import AllSections from '@/views/AllSections.vue'
import AddBook from '@/views/AddBook.vue'
import UpdateBook from '@/views/UpdateBook.vue'
import ViewSection from '@/views/ViewSection.vue'
import IssuedBook from '@/views/IssuedBook.vue'
import BookRequested from '@/views/BookRequested.vue'
import RevokeBook from '@/views/RevokeBook.vue'
import AdminSummaryPage from '@/views/AdminSummaryPage.vue'
import Feedback from '@/views/Feedback.vue'


const routes = [
  {
    path: '/home',
    name: 'home',
    component: HomeView
  },
  {
    path: '/userregister',
    name: 'userRegister',
    component: RegisterPage
  },
  {
    path: '/',
    name: 'userLogin',
    component: LoginPage
  },
  {
    path: '/section/add',
    name: 'createSection',
    component: CreateSection
  },
  {
    path: '/section/update/:id',
    name: 'updateSection',
    component: UpdateSection
  },
  {
    path: '/section/:id/book',
    name: 'viewSection',
    component: ViewSection
  },
  {
    path: '/sections',
    name: 'sections',
    component: AllSections
  },
  {
    path: '/section/:id/book/add',
    name: 'addBook',
    component: AddBook
  },
  {
    path: '/book/update/:id',
    name: 'updateBook',
    component: UpdateBook
  },
  {
    path: '/issued',
    name: 'issuedBook',
    component: IssuedBook
  },
  {
    path: '/bookrequested',
    name: 'bookRequested',
    component: BookRequested
  },
  {
    path: '/bookstatus',
    name: 'bookStatus',
    component: RevokeBook
  },
  {
    path: '/summary',
    name: 'adminStats',
    component: AdminSummaryPage
  },
  {
    path: '/feedback/:id',
    name: 'Feedback',
    component: Feedback
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
