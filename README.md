介绍
============
littlerabbit是【小兔跳铃铛】这个小游戏的外挂

制作于大二暑假

用外挂最高打过150亿分，说实话并不是很高，主要原因是一个关键问题受图片识别方式所限无法解决

所以这个外挂的意义更多在于学习思路，而不是实用


程序思路
============
一次循环一共四步

1. 截屏并处理图片（灰度化、二值化）
2. 判断是否触发动作（判断兔子是否是跳起状态，如果是则触发下一步，如果不是则结束循环）
3. 如果触发动作，对图片进行轮廓提取并与标准图片进行比对，识别出铃铛、兔子和鸟
4. 选择一个铃铛作为目标铃铛，移动鼠标到铃铛的坐标

环境
============
以下是我的开发环境，仅供参考：
* Mac OS X 10.7.5
* Python 2.7.5
* Pyobjc
* python-opencv
* Numpy

注意事项
============
* 我使用的是百度游戏的【小兔跳铃铛】，具体进入方法为：在百度搜索“小兔跳铃铛”，然后点击第一个游戏
* 请将part_x1,part_y1和part_x2,part_y2这两对变量赋值为您屏幕上【小兔跳铃铛】游戏界面的左上角坐标和右下角坐标；坐标一定不能超出游戏界面
* 外挂运行时将占用鼠标
* 请自行修改 **opencv-version.py** 中121、123、125三行的路径为您系统上对应的路径
* 请自行修改 **testhotkey.py** 中23、26两行中的路径为您系统上对应的路径
* 请自行配置好需要的环境

使用方式
============
1. 在终端运行 `$ python testhotkey.py`
2. 等待终端出现 **Let's go!** 字样后，切换到游戏界面
3. 按 **CTRL+1** 组合键启动外挂，按 **CTRL+⌘+K**组合键关闭外挂

系列教程
============
还没顾上写。。。最近有时间会详细写教程的，请关注 [我的技术博客](http://www.cnblogs.com/numbbbbb/)

关于我
============
* [我的技术博客](http://www.cnblogs.com/numbbbbb/)
* [我的个人博客](http://for-never.name)
* [个人简介](http://for-never.name/?page_id=2)
* [我的项目](http://for-never.name/?page_id=11)

联系我
============
* 邮箱：lj925184928@gmail.com
* 微信关注我：![微信关注我](http://images.cnblogs.com/cnblogs_com/numbbbbb/512440/o_qrcode_for_gh_c5b8e57da986_430.jpg)
