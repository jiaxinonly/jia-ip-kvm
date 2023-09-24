<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <TopNavigation></TopNavigation>
      </el-header>
      <el-main id="el-main">
        <video-center></video-center>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import TopNavigation from "@/components/TopNavigation";
import VideoCenter from "@/components/VideoCenter";

export default {
  name: 'App',
  components: {
    TopNavigation,
    VideoCenter
  }
}
</script>

<style>
html, body {
  height: 100vh;
  margin: 0;
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
