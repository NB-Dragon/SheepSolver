# SheepSolver
> 本项目主要用于计算《羊了个羊》小游戏的解题步骤<br>
> 正版项目开源地址为: [https://github.com/NB-Dragon/SheepSolver](https://github.com/NB-Dragon/SheepSolver)

# 项目公示
> 算法的解题思路为回溯算法，尝试解决的`NP问题`为：是否存在一个解使得游戏通关<br>
> 算法的实现方案为不用道具，无法保证解题的高效率运行，解题时间长短取决于个人运气<br>
> 具体实现逻辑则体现在抽牌策略，不同的抽牌策略将会影响最终的解题效果<br>
> 如果觉得项目晦涩难懂，不知如何安装使用，可向群主付费申请技术支援<br>

# 项目联系渠道
> 游戏交流QQ群: **331240392**<br>
> 售前咨询QQ群: **784678298**<br>

# 使用教程
## 部署当前项目
- 下载开源项目: [NB-Dragon/SheepSolver](https://github.com/NB-Dragon/SheepSolver)
```shell
git clone https://github.com/NB-Dragon/SheepSolver.git
cd SheepSolver && pip install -r requirements.txt
```

## 安装抓包程序的依赖组件: nodejs
> 官方安装指导手册: [官方链接](https://nodejs.org/en/download/package-manager)
```shell
# Debian and Ubuntu based Linux distributions
sudo apt install nodejs
```

## 启动mitmdump程序
```shell
# 启动无交互功能的抓包程序
mitmdump -p 6666 -s capture.py
```

## 把证书文件保存到终端设备
- 方法1: 终端设备设置代理后，访问该链接下载证书文件: [http://mitm.it](http://mitm.it)
- 方法2: 将mitmproxy的证书文件直接拷贝到终端设备

## 终端设备添加证书信任
> 受限于文档篇幅，请自行查阅资料，添加证书信任，这里不再展开说明

## 获取游戏地图数据
- 按照上述步骤提示启动mitmdump程序
- 打开微信小程序并进入游戏界面
- 注意此时本项目根路径下的`online_data.json`文件会更新

## 求解答案和提交答案
- 打开终端并进入到本项目的根路径
- 执行命令`python solve.py -m normal`
- 等到结果成功打印出来后，根据自身需求选择答案格式
> 倒数第二行的结果为卡牌的编号，可用于在第三方项目中显示操作步骤

# 算法的选择
> 本算法目前提供六种选牌方式，可在脚本的启动参数中进行修改
- normal: 默认模式，该模式下取牌顺序由程序进度决定
- index: 序号顺序模式，该模式下取牌顺序由初始化阶段的序号决定
- index-reverse: 序号逆序模式，该模式下取牌顺序由初始化阶段的序号决定
- level-bottom: 底层优先模式，该模式下取牌顺序由卡牌的层数决定
- level-top: 高层优先模式，该模式下取牌顺序由卡牌的层数决定
- random: 随机模式，该模式下取牌顺序完全随机，祝各位好运

# 配置说明
- show_progress: 是否需要显示实时求解进度(布尔值)
- solve_first: 优先消除策略的启动时机(百分比)
- time_limit: 程序最长运行时间(秒)，小于0则无限制
- expect_progress: 在指定时间内达到指定进度则继续求解

# 特别鸣谢
- 地图数据的解析思路: [BugMaker888/sheep](https://github.com/BugMaker888/sheep)
- 通关接口的数据剖析: [Protobuf的正逆向学习和基于python的实现](https://www.52pojie.cn/forum.php?mod=viewthread&tid=1692444)

# 许可证
GNU AFFERO GENERAL PUBLIC LICENSE Version 3, 19 November 2007
