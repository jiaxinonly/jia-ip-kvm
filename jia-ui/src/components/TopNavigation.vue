<template>
  <el-menu

      class="el-menu-demo"
      mode="horizontal"
      :ellipsis="false"

  >
    <el-menu-item index="0">LOGO</el-menu-item>
    <div class="flex-grow"/>
    <el-sub-menu index="video">
      <template #title>
        <el-icon>
          <Setting/>
        </el-icon>
        视频
      </template>
      <el-sub-menu index="resolution">
        <template #title>分辨率</template>
        <el-menu-item index="720p" @click="frame('resolution', '720p')">720p</el-menu-item>
        <el-menu-item index="1080p" @click="frame('resolution', '1080p')">1080p</el-menu-item>
      </el-sub-menu>
      <el-sub-menu index="fps">
        <template #title>帧率</template>
        <el-menu-item index="30fps" @click="frame('fps', 30)">30fps</el-menu-item>
        <el-menu-item index="60fps" @click="frame('fps', 60)">60fps</el-menu-item>
      </el-sub-menu>
    </el-sub-menu>

    <el-menu-item index="2">电源</el-menu-item>
    <el-menu-item index="3">挂载</el-menu-item>
    <el-sub-menu index="4">
      <template #title>
        <el-icon>
          <Setting/>
        </el-icon>
        设置
      </template>
      <el-menu-item index="2-1">用户密码</el-menu-item>
      <el-sub-menu index="2-2">
        <template #title>设备</template>
        <el-menu-item index="2-2-1">视频采集器</el-menu-item>
        <el-menu-item index="2-4-2">HID设备</el-menu-item>
      </el-sub-menu>
      <el-menu-item index="2-3" @click="logout">退出</el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<script>
export default {
  name: "TopNavigation",
  methods: {
    frame(type, value) {
      let frameMsg
      if (type === "resolution") {
        if (value === "720p") {
          frameMsg = {
            type: type,
            height: 720,
            width: 1280
          }
        } else if (value === "1080p") {
          frameMsg = {
            type: type,
            height: 1080,
            width: 1920
          }
        }
      } else if (type === "fps") {
        frameMsg = {
          type: type,
          fps: value
        }
      }
      console.log(frameMsg)
      this.$socket.emit('frameMsg', frameMsg)
    },
    logout() {
      this.axios.get("/api/logout/")
      localStorage.removeItem('username')
      localStorage.removeItem('password')
      this.$router.push("/")
    }
  }
}

</script>

<style scoped>
</style>