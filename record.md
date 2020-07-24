# 记录
 The filtering effect on the nonlinear noise:

1.  有影响

  2. 没有影响

filtering effect on ANC and PNC：

​		   1.  真实的ANC，PNC

   			2. 受到滤波影响的ANC 和 PNC

修正方案：滤波与非线性的联合监测

​		   1.  非线性： 理论模型：GN model

   			2.  滤波：     频谱信息
                        			3.  DSP：      抽头系数

**总信噪比，频谱和DSP 提供滤波信噪比，差值为非线性信噪比，需要计算真实信噪比**



**NN: 输入为GN model信噪比，信号在光纤入口处的注入功率**


**CNN：信号频谱特征**



**输出为非线性信噪比**

![image-20200716160944631](/Users/lun/Library/Application Support/typora-user-images/image-20200716160944631.png)



就可以得到真实的非线性







1. 确认滤波对非线性的影响，固定链路长度：12 跨段，滤波器个数分布：
2. 信号功率分布 0dBm，1dBm，2dBm，3dBm，4dBm 
   1. 每一个跨段后面一个滤波器
   2. 每两个跨段后面一个滤波器
   3. 每三个跨段后面一个滤波器
   4. 每四个跨段后面一个滤波器
   5. 每 六个跨段后面一个滤波器





