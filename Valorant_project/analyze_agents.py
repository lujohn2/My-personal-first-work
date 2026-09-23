import pandas as pd
import matplotlib.pyplot as plt

#核心修复：让中文正常显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

#读取你刚生成的CSV文件
df = pd.read_csv("agents.csv")

#统计每个角色的英雄数量
role_counts = df['角色'].value_counts()

#打印统计结果
print("=== 角色统计 ===")
print(role_counts)

#画一个简单的饼图，保存为图片
plt.figure(figsize=(8, 8))
plt.pie(role_counts, labels=role_counts.index, autopct='%1.1f%%', startangle=140)
plt.title("Valorant英雄角色分布")
plt.savefig("role_distribution.png")
print("角色分布图已保存为role_distribution.png")