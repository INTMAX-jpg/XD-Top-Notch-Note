import matplotlib.pyplot as plt
from pymoo.problems import get_problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.indicators.igd import IGD

# 实例化 ZDT1 测试问题,其内部已封装好 30个变量、[0, 1]的边界限制以及 f1, f2 的计算逻辑
problem = get_problem("zdt1")

# pop_size=100 意味着每代有 100 个解在互相竞争和繁衍
algorithm = NSGA2(pop_size=100)

# ('n_gen', 200) 表示迭代 200 代，seed=1 锁定随机种子，保证每次运行结果一致
res = minimize(problem,
               algorithm,
               ('n_gen', 200),
               seed=1,
               verbose=False)

# res.F 是算法最终找到的 Pareto 前沿
our_front = res.F
# 调用 pymoo 内置的 pareto_front 方法获取 ZDT1 的真实理论前沿
true_front = problem.pareto_front()

# 5. 计算量化评价指标: IGD (反向世代距离)
# 用理论前沿去评估我们的解集，值越小越好
metric = IGD(true_front)
igd_value = metric.do(our_front)
print(f"求得的 IGD 指标值为: {igd_value:.6f}")

# 用 matplotlib 可视化库对实验结果进行可视化分析
plt.figure(figsize=(8, 6))
# 画理论前沿 (黑色实线)
plt.plot(true_front[:, 0], true_front[:, 1], color="black", linewidth=2, label="True Pareto Front")
# 画算法求出的解 (红色散点)
plt.scatter(our_front[:, 0], our_front[:, 1], color="red", s=30, alpha=0.7, label="NSGA-II Solutions")

plt.title("NSGA-II on ZDT1 Test Problem")
plt.xlabel("Objective 1 (f1)")
plt.ylabel("Objective 2 (f2)")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()