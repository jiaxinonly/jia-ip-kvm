<template>
  <el-menu

      class="el-menu-demo"
      mode="horizontal"
      :ellipsis="false"

  >
    <el-menu-item index="0">LOGO</el-menu-item>
    <div class="flex-grow"/>
    <el-menu-item index="1">视频</el-menu-item>
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
      <el-menu-item index="2-3">退出</el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<script>
export default {
  name: "TopNavigation"
}
</script>

<style scoped>
</style>