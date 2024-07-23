<template>
  <div id="login-page">
    <div class="login-container">
      <div class="left-container">
        <div class="title"><span>登录</span></div>
        <div class="input-container">
          <input type="text" v-model="username" placeholder="用户名">
          <input type="password" v-model="password" placeholder="密码">
        </div>
        <div class="action-container">
          <span @click="loginSubmit">提交</span>
        </div>
      </div>
      <div class="right-container">
        <div class="regist-container">
          <span class="regist">jia-ip-kvm</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoginForm",
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    loginSubmit() {
      this.axios.post('/api/login/', {
        username: this.username,
        password: this.password
      }).then(response => {
        if (response.data.status === 'success') {
          this.$message.success("登录成功！")
          localStorage.setItem('username', this.username)
          localStorage.setItem('password', this.password)
          this.$router.push('/kvm')
        } else {
          this.$message.error("用户名或密码错误！")
        }
      })
    }
  }
}
</script>

<style scoped>
#login-page {
  height: 100vh;
  background-image: linear-gradient(to bottom right, rgb(114, 135, 254), rgb(130, 88, 186));
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
}

.login-container {
  width: 600px;
  border-radius: 15px;
  box-shadow: 0 10px 50px 0px rgb(59, 45, 159);
  background-color: rgb(95, 76, 194);
}

.left-container {
  display: inline-block;
  width: 330px;
  border-top-left-radius: 15px;
  border-bottom-left-radius: 15px;
  padding: 60px;
  background-image: linear-gradient(to bottom right, rgb(118, 76, 163), rgb(92, 103, 211));
}

.title {
  color: #fff;
  font-size: 18px;
  font-weight: 200;
}

.input-container {
  padding: 20px 0;
}

input {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
  border: none;
  border-radius: 5px;
  outline: none;
  font-size: 16px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

input:hover {
  border-bottom-color: #fff;
}

::-webkit-input-placeholder {
  color: rgb(199, 191, 219);
}

.right-container {
  width: 145px;
  display: inline-block;
  height: calc(100% - 120px);
  vertical-align: top;
  padding: 60px 0;
}

.regist-container {
  text-align: center;
  color: #fff;
  font-size: 18px;
  font-weight: 200;
}

.action-container {
  font-size: 10px;
  color: #fff;
  text-align: center;
  position: relative;
  top: 40px;
}

.action-container span {
  border: 1px solid rgb(237, 221, 22);
  padding: 10px;
  display: inline;
  line-height: 20px;
  border-radius: 20px;
  position: absolute;
  bottom: 10px;
  transition: .2s;
  cursor: pointer;
}

.action-container span:hover {
  background-color: rgb(237, 221, 22);
  color: rgb(95, 76, 194);
}
</style>
