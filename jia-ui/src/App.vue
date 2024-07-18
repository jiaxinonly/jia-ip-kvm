<template>
  <div class="common-layout">
    <LoginForm></LoginForm>
<!--    <el-container>-->
<!--      <el-header>-->
<!--        <TopNavigation></TopNavigation>-->
<!--      </el-header>-->
<!--      <el-main id="el-main">-->
<!--        <video-center></video-center>-->
<!--      </el-main>-->
<!--    </el-container>-->
  </div>
</template>

<script>
// import TopNavigation from "@/components/TopNavigation";
// import VideoCenter from "@/components/VideoCenter";
import LoginForm from '@/components/LoginForm.vue'

export default {
  name: 'App',
  components: {
    // TopNavigation,
    // VideoCenter,
    LoginForm
  }
}
</script>

<style>
html {
  height: 100vh;
  margin: 0;
  background-image: linear-gradient(to bottom right, rgb(114, 135, 254), rgb(130, 88, 186));
}

#el-main {
  text-align: center;
  margin: 0 auto;
}

/* 顶部菜单栏挂到右侧 */
.flex-grow {
  flex-grow: 1;
}
</style>
