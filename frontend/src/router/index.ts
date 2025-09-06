import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import CoursesView from '../views/CoursesView.vue'
import CourseDetailView from '../views/CourseDetailView.vue'
import ProductsView from '../views/ProductsView.vue'
import ProductDetailView from '../views/ProductDetailView.vue'
import CartView from '../views/CartView.vue'
import CheckoutView from '../views/CheckoutView.vue'
import PaymentView from '../views/PaymentView.vue'
import PaymentSuccessView from '../views/PaymentSuccessView.vue'
import PaymentTest from '../views/PaymentTest.vue'
import SimplePay from '../views/SimplePay.vue'
import AdminLogin from '../views/AdminLogin.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import AdminLayout from '../views/admin/AdminLayout.vue'
import Dashboard from '../views/admin/Dashboard.vue'
import UserManagement from '../views/admin/UserManagement.vue'
import CourseManagement from '../views/admin/CourseManagement.vue'
import ExpertManagement from '../views/admin/ExpertManagement.vue'
import ProductManagement from '../views/admin/ProductManagement.vue'
import OrderManagement from '../views/admin/OrderManagement.vue'
import ConsultationManagement from '../views/admin/ConsultationManagement.vue'
import DataExport from '../views/admin/DataExport.vue'
import SystemSettings from '../views/admin/SystemSettings.vue'
import ProductAudit from '../views/admin/ProductAudit.vue'
import ProductSubmit from '../views/ProductSubmit.vue'
import LoginView from '../views/LoginView.vue'
import ProfileView from '../views/ProfileView.vue'
import MyView from '../views/MyView.vue'
import TestUpload from '../views/TestUpload.vue'
import AssessmentView from '../views/AssessmentView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    {
      path: '/courses',
      name: 'courses',
      component: CoursesView
    },
    {
      path: '/courses/:id',
      name: 'course-detail',
      component: CourseDetailView
    },
    {
      path: '/assessment',
      name: 'assessment',
      component: AssessmentView
    },
    {
      path: '/products',
      name: 'products',
      component: ProductsView
    },
    {
      path: '/products/:id',
      name: 'product-detail',
      component: ProductDetailView
    },
    {
      path: '/cart',
      name: 'cart',
      component: CartView
    },
    {
      path: '/checkout',
      name: 'checkout',
      component: CheckoutView
    },
    {
      path: '/payment/:orderId',
      name: 'payment',
      component: PaymentView
    },
    {
      path: '/simple-pay/:orderId',
      name: 'simple-pay',
      component: SimplePay
    },
    {
      path: '/payment/success',
      name: 'payment-success',
      component: PaymentSuccessView
    },
    {
      path: '/payment-test',
      name: 'payment-test',
      component: PaymentTest
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true }
    },
    {
      path: '/admin/login',
      name: 'admin-login',
      component: AdminLogin
    },
    {
      path: '/admin',
      component: AdminLayout,
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        {
          path: 'dashboard',
          name: 'admin-dashboard',
          component: Dashboard
        },
        {
          path: 'users',
          name: 'admin-users',
          component: UserManagement
        },
        {
          path: 'courses',
          name: 'admin-courses',
          component: CourseManagement
        },
        {
          path: 'experts',
          name: 'admin-experts',
          component: ExpertManagement
        },
        {
          path: 'products',
          name: 'admin-products',
          component: ProductManagement
        },
        {
          path: 'product-audit',
          name: 'admin-product-audit',
          component: ProductAudit
        },
        {
          path: 'orders',
          name: 'admin-orders',
          component: OrderManagement
        },
        {
          path: 'consultations',
          name: 'admin-consultations',
          component: ConsultationManagement
        },
        {
          path: 'export',
          name: 'admin-export',
          component: DataExport
        },
        {
          path: 'settings',
          name: 'admin-settings',
          component: SystemSettings
        }
      ]
    },
    {
      path: '/my',
      name: 'my',
      component: MyView
    },
    {
      path: '/product-submit',
      name: 'product-submit',
      component: ProductSubmit
    },
    {
      path: '/test-upload',
      name: 'test-upload',
      component: TestUpload
    },
    {
      path: '/admin',
      redirect: '/admin/dashboard'
    }
  ]
})

// 路由守卫 - 使用统一权限验证
import { useUserStore } from '../stores/user'

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // 优先检查管理员权限
  if (to.meta.requiresAdmin) {
    if (!userStore.isLoggedIn) {
      next('/admin/login')
      return
    }
    
    if (!userStore.isAdmin()) {
      next('/admin/login')
      return
    }
    
    next()
    return
  }
  
  // 检查是否需要用户认证
  if (to.meta.requiresAuth) {
    if (!userStore.isLoggedIn) {
      next('/login')
      return
    }
    
    // 检查用户状态
    if (userStore.user && (!userStore.user.is_active || userStore.user.status === 'banned')) {
      userStore.clearUser()
      next('/login')
      return
    }
  }
  
  next()
})

export default router