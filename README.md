<p align="center">
<h1 align="center">ddreplayDownloader</h1>
<p align="center">主要用于在钉钉管理员关闭回放下载功能时进行下载</p>

## 基于

  * Python
  * DingTalk
  * ffmpeg

## 前置

​	必须安装 ffmpeg！必须安装 ffmpeg！必须安装 ffmpeg！重要的事情说三遍。

​	安装 `ffmpeg` 是为了能将 ts 切片文件合成为一个完整的 `mp4` 文件。

​	>>> [下载地址](https://www.ffmpeg.org/download.html) <<<

## 食用方式

1. 创建文件夹，`tsDir`用于存放 ts 切片文件。

   ```bash
   # Unix System
   $ mkdir tsDir
   ```
2. 获取直播回放链接。主要是获取两个参数值 `encCid` 与 `liveUuid`。

   > 例如：https://h5.dingtalk.com/group-live-share/index.htm?encCid=&liveUuid=

3. 运行文件，并耐心等待。（默认的下载线程为 16）。

   ```bash
   $ python3 main.py -e <encCid> -l <liveUuid>
   ```

4. 文件下载完成后，清空 `tsDir` 文件夹。

## 工具出现问题？

​	提交ISSUE就好了，有时间的话我肯定更新OvO，后面会更新一些方便的功能。例如自动删除ts文件等。
