<template>
  <el-card id="video-center" shadow="hover" @click="cardClick">
    <img id="video" :class="{loading: loading}" :src="videoUrl" alt="">
  </el-card>
</template>

<script>

export default {
  name: "VideoCenter",
  data() {
    return {
      videoUrl: require('@/assets/loading.gif'),
      mouse_status: false,
      key_status: false,
      video: null,
      lastExitTime: "",
      loading: false
    }
  },
  mounted() {
    this.axios.get("/api/userinfo/").then(respose => {
      if (respose.data.status === "success") {
        this.$socket.open()
      }
    })
    this.$socket.emit('videoMsg')
    this.sockets.subscribe('videoMsg', data => {
      if (this.loading === false) {
        this.loading = true
      }
      this.videoUrl = data
    })
    this.video = document.getElementById('video')
    document.addEventListener('pointerlockchange', this.pointerLockChange)
  },
  methods: {
    cardClick() {
      if (this.loading) {
        console.log("点击了")
        if (this.mouse_status === false) {
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
      }
    },
    // 鼠标锁点状态改变时
    pointerLockChange: function () {
      if (this.mouse_status === true) {
        // 设置状态为false
        this.mouse_status = false
        // 恢复鼠标光标
        this.cursor = "auto"
        // 移除监听事件
        window.removeEventListener('mousemove', this.mouseMove)
        window.removeEventListener('mousedown', this.mouseDown)
        // 恢复右击菜单
        document.oncontextmenu = function () {
          return true;
        }
        this.lastExitTime = Date.now()
        console.log('退出了')
      } else if (this.mouse_status === false) {
        // 设置状态为true
        this.mouse_status = true
        if (this.key_status === false) {
          console.log("键盘监听")
          this.key_status = true
          window.addEventListener('keydown', this.keyDown)
        }
        // 添加监听事件
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
      keyEvent.stopPropagation()
      let keyMsg = ''
      let ctrlTab = ['Control', 'Shift', 'Alt', 'Meta']
      let keyMap = {
        ':': ';',
        '+': '=',
        '<': ',',
        '_': '-',
        '>': '.',
        '?': '/',
        '~': '`',
        '{': '[',
        '}': ']',
        '|': '\\',
        '"': '\'',
        ')': '0',
        '!': '1',
        '@': '2',
        '#': '3',
        '$': '4',
        '%': '5',
        '^': '6',
        '&': '7',
        '*': '8',
        '(': '9',
      }

      // 单独按下控制键时
      if (ctrlTab.indexOf(keyEvent.key) !== -1) {
        keyMsg = keyEvent.code
      } else {
        // 组合按键
        let ctrlKey = ''
        if (keyEvent.ctrlKey) {
          ctrlKey += 'ControlLeft+'
        }
        if (keyEvent.shiftKey) {
          ctrlKey += 'ShiftLeft+'
        }
        if (keyEvent.altKey) {
          ctrlKey += 'AltLeft+'
        }
        if (keyEvent.metaKey) {
          ctrlKey += 'MetaLeft+'
        }
        if (keyEvent.key in keyMap) {
          keyMsg = ctrlKey + keyMap[keyEvent.key]
        } else {
          keyMsg = ctrlKey + keyEvent.key
        }
      }

      console.log(keyMsg)

      // 退出
      if (keyMsg === 'ControlLeft+ShiftLeft+`') {
        console.log('退出键盘控制')
        if (this.key_status) {
          this.key_status = false
          window.removeEventListener("keydown", this.keyDown)
        }

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
#video-center {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
}

#video {
  width: 100%;
  height: 100%;
  object-fit: none;
  position: absolute;
  top: 0;
  left: 0;
}

#video.loading {
  object-fit: fill;
}
</style>