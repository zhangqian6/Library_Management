<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <ul>
        <li v-bind:class="{active: currentView === 'DashBoard'}" @click="currentView = 'DashBoard'">仪表盘</li>
        <li v-bind:class="{active: currentView === 'Home'}" @click="currentView = 'Home'">首页</li>
        <li v-bind:class="{active: currentView === 'BookManage'}" @click="currentView = 'BookManage'">图书管理</li>
        <li v-bind:class="{active: currentView === 'UserManage'}" @click="currentView = 'UserManage'">用户管理</li>
        <li v-bind:class="{active: currentView === 'LendRecord'}" @click="currentView = 'LendRecord'">借阅管理</li>
      </ul>
      <button @click="logout">退出登录</button>
    </aside>

    <main class="main-content">
      <component :is="currentComponent"></component>
    </main>
    
    <!-- <button @click="logout">Logout</button> -->
  </div>

</template>

<script setup>
import { ref, computed } from 'vue';
import DashBoard from '../views/DashBoard.vue'
import Home from '../views/Home.vue'
import UserManage from '../views/UserManage.vue'
import BookManage from '../views/BookManage.vue'
import LendRecord from '../views/LendRecord.vue'
import router from '@/router';

// 当前视图标识
const currentView = ref('DashBoard')

//页面组件映射
const currentComponent = computed(() => {
  switch(currentView.value){
    case 'Home':
      return Home
    case 'BookManage':
      return BookManage
    case 'UserManage':
      return UserManage
    case 'LendRecord':
      return LendRecord
    default:
      return DashBoard
  }
})



const logout = () => {
  localStorage.removeItem('token'); // 清除token
  router.push('/Login');
}


</script>

<style scoped>
.admin-layout{
  display: flex;
  height: 100vh;
 
}

.sidebar{
  width: 200px;
  background-color: #f4f4f4;
  border-right: 1px solid #ddd;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  padding: 10px;
  cursor: pointer;
}

.sidebar li.active{
  background-color: #007bff;
  color: white;
  border-radius: 5px;
}

.main-content {
  flex: 1;
  padding: 20px;
}
</style>