import requests
import csv # Python内置的CSV处理库
#1.获取数据（和昨天一样）
url="https://valorant-api.com/v1/agents"
response = requests.get(url)
data = response.json()
#2.准备一个空列表，用来存放我们要提取的信息
agents_list = []
#3.循环遍历每一个英雄
for agent in data['data']:
    #过滤掉“训练假人”(没有角色的哪些数据)
    if agent.get("role") is not None:
        name = agent['displayName']
        role = agent['role']['displayName']
        description = agent['description']
        #把这三个信息打包成字典，然后添加到列表中
        agents_list.append({
            "名字": name,
            "角色": role,
            "描述": description[:30] + "..."
        })
#4.把列表写入CSV文件
with open("agents.csv", mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.DictWriter(file, fieldnames=["名字", "角色", "描述"])
    writer.writeheader()  # 写入表头
    writer.writerows(agents_list)  # 写入数据
print(f"成功保存{len(agents_list)}个英雄的数据到agents.csv文件中。")