<template>
  <div id="KVM-page">
    <el-container id="el-container">
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
#el-container{
  height: 100vh;
}

#el-main{
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>