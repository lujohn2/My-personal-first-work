# Valorant 历史项目扩展

在原有英雄角色统计的基础上，项目现在包含：

- `agents.csv`：从 `valorant-api.com` 拉取的当前可用英雄、角色和版本号；
- `data/player_acs.csv`：VLR 国际 VCT 年度筛选的可核验 ACS 样本；
- `data/player_acs_ranking.csv`：基于公开样本的选手 ACS 排名，不冒充单届 Champions 排名；
- `data/champions_map_pool.csv`：2021--2025 图池重建值（待复核），以及官方已公布但尚未开赛的 2026 Champions Shanghai；
- `valorant_world_events_report.xlsx`：附件，包含 `ACS排名`、`图池`、`赛事原始ACS` 三个工作表。

## 运行

```powershell
python build_report.py
python analyze_agents.py
```

`build_report.py` 会更新官方版本和英雄数据，并重新生成排名及 Excel 附件。赛事 ACS 与图池数据不由
`valorant-api.com` 提供，因此保留来源 URL 和备注，避免把官方英雄 API 与赛事统计混为一谈。

ACS 排名采用已核验样本的简单平均值；`赛事原始ACS` 工作表保留每条记录，便于复核。
这些数据来自 VLR 的公开筛选页，不是 Riot 官方 ACS 导出，也不是单届全球冠军赛完整选手表。
截至 2026-09-23，已核验的官方资料指向 Champions Shanghai，而不是“London Masters 2026”；
因此项目不再把 London Masters 作为已确认赛事，也不填入未开赛 Champions 的图池。
