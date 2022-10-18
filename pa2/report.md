# 作业2. 调制与解调

**周雨豪  2018013399  软件92**



## I. 作业目标

1. 理解物联网无线通信的基本流程和原理
2. 掌握常用的无线信号调制、解调方法(如振幅调制(ASK)、频率调制(FSK)、相位调制(PSK)等)



## II. 实验环境

操作系统: macOS 12.6

编程语言: Python 3.9

CPU: Apple M1

内存: 16GB



## III. 实验结果

源码位于 `src/`，所有音频文件保存于 `wav/`

1. 示例二进制序列 `11110000101010`，调制前和解调后波形如图所示，由波形一致得知调制函数与解调函数有效

   <img src="/Users/krzhck/Library/Application Support/typora-user-images/image-20221018200855690.png" alt="image-20221018200855690" style="zoom:30%;" />

2. 加入高斯白噪声，信噪比分别为 20dB，10dB，0dB，传输成功率如下图所示：

   <img src="/Users/krzhck/Library/Application Support/typora-user-images/image-20221018200919614.png" alt="image-20221018200919614" style="zoom:30%;" />