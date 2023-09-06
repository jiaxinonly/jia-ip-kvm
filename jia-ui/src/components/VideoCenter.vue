<template>
  <el-card id="video-center" shadow="hover" @click="cardClick">
    <img id="video" :src="videoUrl" alt="" :style="{ 'object-fit': 'fill', 'cursor': cursor}">
  </el-card>
</template>

<script>

export default {
  name: "VideoCenter",
  data() {
    return {
      videoUrl: require('@/assets/loading.gif'),
      status: false,
      cursor: 'auto',
      video: null,
      lastExitTime: "",
    }
  },
  mounted() {
    this.$socket.emit('videoMsg', 'start')
    this.sockets.subscribe('videoMsg', data => {
      this.videoUrl = data
    })
    this.video = document.getElementById('video')
    document.addEventListener('pointerlockchange', this.pointerLockChange)
  },
  methods: {
    cardClick() {
      console.log("点击了")
      if (this.status === false) {
        // 保证退出后等待足够的时间再进入
        let waitTime = 1260
        if (this.lastExitTime && Date.now() - this.lastExitTime < waitTime) {
          setTimeout(function () {
            this.video.requestPointerLock()
          }, waitTime - (Date.now() - this.lastExitTime));
        } else {
          this.video.requestPointerLock()
        }
        console.log("锁上了")
      }
    },
    // 鼠标锁点状态改变时
    pointerLockChange: function () {
      if (this.status === true) {
        // 设置状态为false
        this.status = false
        // 恢复鼠标光标
        this.cursor = "auto"
        // 移除监听事件
        window.removeEventListener("keydown", this.keyDown)
        window.removeEventListener('mousemove', this.mouseMove)
        window.removeEventListener('mousedown', this.mouseDown)
        // 恢复右击菜单
        document.oncontextmenu = function () {
          return true;
        }
        this.lastExitTime = Date.now()
        console.log('退出了')
      } else if (this.status === false) {
        // 设置状态为true
        this.status = true
        // 添加监听事件
        window.addEventListener('keydown', this.keyDown)
        window.addEventListener('mousemove', this.mouseMove)
        window.addEventListener('mousedown', this.mouseDown)
        // 关闭右击菜单
        document.oncontextmenu = function () {
          return false;
        }
        console.log('进入')
      }
    },
    // 键盘按下事件
    keyDown: function (keyEvent) {
      console.log(keyEvent)
      keyEvent.preventDefault()
      let keyMsg = ''
      let ctrlTab = ['Control', 'Shift', 'Alt', 'Meta']

      // 单独按下控制键时
      if (ctrlTab.indexOf(keyEvent.key) !== -1) {
        keyMsg = keyEvent.code
      } else {
        // 组合按键
        let ctrlKey = ''
        if (keyEvent.ctrlKey) {
          ctrlKey = ctrlKey + 'ControlLeft+'
        }
        if (keyEvent.shiftKey) {
          ctrlKey = ctrlKey + 'ShiftLeft+'
        }
        if (keyEvent.altKey) {
          ctrlKey = ctrlKey + 'AltLeft+'
        }
        if (keyEvent.metaKey) {
          ctrlKey = ctrlKey + 'MetaLeft+'
        }
        keyMsg = ctrlKey + keyEvent.key
      }
      console.log(keyMsg)

      // 退出
      if (keyMsg === 'Escape') {
        console.log('exit')
      } else {
        this.$socket.emit('keyMsg', keyMsg)
      }
    },
    mouseMove(mouseEvent) {
      let x = mouseEvent.movementX
      let y = mouseEvent.movementY

      let mouseMsg = {
        'key': null,
        'x': x,
        'y': y
      }
      console.log(mouseMsg)
      this.$socket.emit('mouseMsg', mouseMsg)
    },
    mouseDown(mouseEvent) {
      mouseEvent.preventDefault()
      let mouseMsg = {
        'x': 0,
        'y': 0
      }
      if (mouseEvent.button === 0) {
        mouseMsg.key = 'LeftKey'
      } else if (mouseEvent.button === 1) {
        mouseMsg.key = 'MiddleKey'
      } else if (mouseEvent.button === 2) {
        mouseMsg.key = 'RightKey'
      }
      console.log(mouseMsg)
      this.$socket.emit('mouseMsg', mouseMsg)
    }
  }
}
</script>

<style scoped>
/*#video-center {*/
/*  min-height: 600px;*/
/*  min-width: 1280px;*/
/*}*/

#video {
  height: 100%;
  width: 100%;
}
</style>