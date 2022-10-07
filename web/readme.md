
### 一、运行环境

#### 1、Python3

推荐使用`Anaconda`进行安装，官网：[https://www.anaconda.com](https://www.anaconda.com/) 。

#### 2、Node.js

为了运行`three.js`网页，官网：[https://nodejs.org/zh-cn/download](https://nodejs.org/zh-cn/download/) 。

---

### 二、克隆本项目

使用以下命令将本项目克隆到本地，并进入项目目录：
```
git clone https://github.com/BugMaker888/sheep.git
cd sheep/
```

> MacOS系统使用终端执行，Windows系统使用Powershell。

---

### 三、Three.js的配置

`Three.js`是一个开源的网页3D渲染库，项目地址为：[https://github.com/mrdoob/three.js](https://github.com/mrdoob/three.js) 。

#### 1、安装

按顺序逐行执行以下命令：
```
git clone https://github.com/mrdoob/three.js.git
cd three.js/
npm install
npm start
```

打开 [http://localhost:8080/examples/](http://localhost:8080/examples/) 就可以看到示例了，我的3d地图就是拿其中一个示例改的。

#### 2、使用

把本项目下的`html`目录里的所有内容拷贝到`three.js/examples/`目录里，这样就可以访问 [http://localhost:8080/examples/sheep.html](http://localhost:8080/examples/sheep.html) 了。

---

### 四、mitmproxy的配置

`mitmproxy`是一个开源的抓包工具，项目地址为：[https://github.com/mitmproxy/mitmproxy](https://github.com/mitmproxy/mitmproxy) ，最大的优点是可以加载自己写的python代码进行数据处理。

#### 1、安装

安装Python3后，执行以下命令安装mitmproxy与pyExecJs：
```
pip install mitmproxy pyExecJs
```

#### 2、启动

因为`three.js`和`mitmproxy`都默认使用`8080`端口，所以需要改一下端口运行。

将终端切换到本项目目录，执行以下命令加载`sheep.py`插件：
```
mitmweb -p 6666 -s sheep.py
```

执行后浏览器会弹出一个抓包的网页界面。


#### 3、安装证书

接下来使用手机连接电脑的ip以及使用`6666`端口作为代理，就可以抓包了。

设置代理可以参考视频教程 [【4分钟教会你Charles抓包设置抓取电脑HTTPS以及IOS手机抓包-哔哩哔哩】](https://b23.tv/S0d8iYa) 两分钟的地方。

使用手机浏览器访问 [http://mitm.it](http://mitm.it) 安装`mitmproxy`的证书。

苹果手机需要在 <kbd>设置</kbd> - <kbd>通用</kbd> - <kbd>关于本机</kbd> - <kbd>证书信任设置</kbd> 里信任证书。

如果安卓手机安装不了证书，也可以使用电脑的安卓模拟器。


#### 4、使用

因为关卡数据每天只会请求一次，所以可以先删除游戏再重新进入。

手机进入游戏后，电脑刷新网页，就可以看到最新的游戏3d地图了。

> 因为`sheep.py`默认将地图数据保存到`./three.js/examples/map_data.js`里，如果`three.js/`没放到`sheep/`目录里的话，需要修改`sheep.py`里的路径。

---

### 五、游戏数据

文件`three.js/examples/map_data.js`里面保存着游戏的关卡数据。

大致说明一下字段的含义：

``` json
{
    "widthNum": 8,
    "heightNum": 10,
    "levelKey": 90029,
    "blockTypeData": {  //图案类型对应组数
        "1": 6,         //图案1有6*3=18个
        "2": 6,
        "3": 6,
        "4": 6,
        "5": 5
    },
    "levelData": {  //关卡数据
        "1": [      //第1层，也就是最底层
            {
                "id": "1-24-8",
                "type": 2,      //图案类型
                "rolNum": 24,   //x坐标
                "rowNum": 8,    //y坐标
                "layerNum": 1,  //层数
                "moldType": 1,
                "blockNode": null
            }

            //......
        ]
    },
    "layers": [     //排序后的层数
        "1",
        "2",
        "3",
        "4",
        "5"
    ]
}
```

地图原点在左上角，方块的大小是`8 * 8`，有了这些数据就可以尝试写算法求解了。
