# 作业4. 傅立叶变换

**周雨豪  2018013399  软件92**



## I. 作业目标

掌握采样理论、傅立叶变换等基本信号处理方法



## II. 实验环境

操作系统: macOS 12.6

编程语言: Python 3.9

CPU: Apple M1

内存: 16GB



## III. 实验结果

源码位于 `src/`，音频文件保存于 `wav/`

1. 

   *(a)*

   <img src="/Users/krzhck/Library/Application Support/typora-user-images/image-20221027044206173.png" alt="image-20221027044206173" style="zoom:30%;" />

   <div style="page-break-after: always;"></div>

   *(b)*

   <img src="/Users/krzhck/Library/Application Support/typora-user-images/image-20221027044218998.png" alt="image-20221027044218998" style="zoom:30%;" />

   *(c)*

   <img src="/Users/krzhck/Library/Application Support/typora-user-images/image-20221027044230978.png" alt="image-20221027044230978" style="zoom:30%;" />

   <div style="page-break-after: always;"></div>

2. 

   *(a)* 信号频谱图如下图**左**侧所示。

   <img src="/Users/krzhck/Library/Application Support/typora-user-images/image-20221027044327764.png" alt="image-20221027044327764" style="zoom:30%;" />

   *(b)* 补零后的信号频谱图如上图**右**侧所示。补零增加了采样的点数且改变了采样点的位置，显示出原信号频谱的更多细节，包括一些次要的低频和高频分量，在频谱上产生毛刺。

   

   *(c)* 分别使用 256 和 48 作为窗口长度。观测到窗口越宽时频图越窄，频率分辨率越高，能看到频谱快的变化；窗宽越窄时频图越宽，频率分辨率越低，看不到频谱快的变化。

   <img src="/Users/krzhck/Library/Application Support/typora-user-images/image-20221027044412567.png" alt="image-20221027044412567" style="zoom:30%;" />