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
      video: null
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
      this.video.requestPointerLock()
    },
    pointerLockChange: function () {
      if (this.status === true) {
        this.status = false
        this.cursor = "auto"
        window.removeEventListener("keydown", this.keyDown)
        window.removeEventListener('mousemove', this.mouseMove)
        window.removeEventListener('mousedown', this.mouseDown)
        document.oncontextmenu = function () {
          return true;
        }
        console.log('退出了')
      } else if (this.status === false) {
        this.status = true
        window.addEventListener('keydown', this.keyDown)
        window.addEventListener('mousemove', this.mouseMove)
        window.addEventListener('mousedown', this.mouseDown)
        document.oncontextmenu = function () {
          return false;
        }
        console.log('进入')
      }
    },
    keyDown: function (keyEvent) {
      console.log(keyEvent)
      keyEvent.preventDefault()
      let keyMsg = ''
      let ctrlTab = ['Control', 'Shift', 'Alt', 'Meta']

      // 单独按下控制键
      if (ctrlTab.indexOf(keyEvent.key) !== -1) {
        keyMsg = keyEvent.code
      } else {
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

      if (keyMsg === 'Escape') {
        console.log('exit')
      } else {
        if (keyMsg === 'ControlLeft+`') {
          keyMsg = 'Escape'
        }
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