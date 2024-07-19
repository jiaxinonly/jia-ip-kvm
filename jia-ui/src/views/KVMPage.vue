<template>
  <div id="KVM-page">
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
  name: "KVMPage",
  components: {
    TopNavigation,
    VideoCenter
  }
}

</script>

<style scoped>

</style>