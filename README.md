## TODO-List

1. [x] 确定模型
2. [x] 算法部分完成
3. [ ] UI 设计
4. [ ] UI 完成
5. [ ] 测试





## 求什么？

约束：

1. 车辆最多跑 35km
2. 多车型（载重）
3. *时间窗口（hard）*
4. *多起点（从 A 点出发，最终必须回到 A 点）*
5. time(A, B) = dis(A, B) / speed + unload_time

目标：

1. Min 总路径长度

 	2. Max 装载率
 	3. Min 时间（即 Min 单词路径长度）

目标函数：

1. 最小化 $\sum_{i=1}^n V_i * D_i + I_i$（V 表示第 i 辆车的每公里运营成本，目前就是最大载重。D 代表第 i 辆车的路径长度，I 代表第 i 辆 车的初始成本）
2. 最大化 $\min \{ \frac{L_1}{W_1}, \frac{L_2}{W_2}, \cdots, \frac{L_n}{W_n} \}$ （L 代表实际载重，W 代表最大载重）
3. 最小化 $\max \{ D_1, D_2, \cdots, D_n \}$





## 资料

#### ortools 资料

1. [线性规划](https://zhuanlan.zhihu.com/p/55496624)
2. [谷歌的文档](https://developers.google.com/optimization/routing)



​	