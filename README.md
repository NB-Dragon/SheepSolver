# SheepSolver
> 本项目主要用于计算《羊了个羊》微信小程序的解题步骤

# 项目公示
> 算法的基本思路为回溯算法，尝试解决的`NP问题`为：是否存在一个解使得游戏通关<br>
> 从代码逻辑中体现为卡牌的抽取顺序，不同的优先抽取方式会决定能否在短时间内得到答案<br>
> 如果解题时间超过5分钟，建议放弃挑战并重新开始

# 使用教程
## 部署第三方项目
- 下载[开源项目](https://github.com/BugMaker888/sheep)
```shell
git clone https://github.com/BugMaker888/sheep
cd sheep && git checkout f73548a5e41360da37d7b1877164c7b5f547184c
```

- 按照第三方开源项目的说明进行部署

## 修改本地文件
- 修改`web/sheep.py`文件中第57行代码，将路径修改为本项目的绝对路径，如下面所示
```text
# 替换前
save_path = "path/to/your/SheepSolver/online_data.json"
# 替换后
save_path = "/home/root/SheepSolver/online_data.json"
```

## 替换第三方项目
- 把`web`目录下的`sheep.py`文件，替换到已成功部署的第三方项目的根路径

## 获取游戏地图数据
- 按照说明，启动`mitmweb`服务和`live-server`服务
- 打开小程序并进入游戏
- 注意此时本项目根路径下的`online_data.json`文件会更新

## 求解答案并加载到网页上面
- 打开终端并进入到本项目的根路径
- 执行命令`python main.py`
- 等到结果成功打印出来后，把倒数第二行的数据复制出来
- 按照第三方项目说明，把结果粘贴到对应文件

# 算法的选择
> 本算法目前提供三种选牌方式，可在`main.py`的第5行代码处自行修改
- normal: 默认模式，该模式下取牌顺序由程序进度决定
- reverse: 反转模式，该模式下取牌顺序由卡牌的逆序号决定，序号大的优先
- top-first: 高层优先模式，该模式下取牌顺序由卡牌的层数决定，高层优先

# 许可证
GNU AFFERO GENERAL PUBLIC LICENSE Version 3, 19 November 2007
