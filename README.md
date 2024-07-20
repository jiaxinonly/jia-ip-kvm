# jia-ip-kvm
> 适用于家用的远程web kvm  
  
目前支持修改分辨率和帧率  

存在的问题：
1. 画面显示存在一定延迟
2. 鼠标移动不顺畅（一是画面有延迟，二是鼠标位移刷新不够快，存在鼠标跳动的情况）

后续：
1. 支持登录 进行中
2. 兼容其他设备
3. 支持读取剪切板复制
4. ~~优化esc进入和退出~~ 浏览器限制，不支持禁止esc退出锁定
## jia-sever
> python flask后台

启动方式：python app.py

## jia-ui
> vue前端

## 设备依赖
> 视频采集卡
>
> HID设备：usb转ttl模块 ch9329模块

## 类似项目
[pikvm](https://github.com/pikvm/pikvm)   
[Open IP-KVM](https://github.com/Nihiue/open-ip-kvm)