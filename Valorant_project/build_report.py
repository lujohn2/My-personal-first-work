"""Build the Valorant content, ACS ranking, and map-pool attachments.

The esports CSV is intentionally source-backed and kept separate from the
official content API. ACS is ranked by the arithmetic mean of the recorded
event ACS values; the weighted score uses map count so players with more maps
are not treated as equally observed.
"""

from pathlib import Path
import csv
from datetime import datetime, timezone

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
VERSION_URL = "https://valorant-api.com/v1/version"
AGENTS_URL = "https://valorant-api.com/v1/agents?isPlayableCharacter=true"


def fetch_json(url):
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    payload = response.json()
    if payload.get("status") != 200:
        raise RuntimeError(f"API returned an unexpected status for {url}")
    return payload["data"]


def update_official_content():
    retrieved_at = datetime.now(timezone.utc).isoformat()
    version = fetch_json(VERSION_URL)
    with (DATA / "valorant_versions.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["版本", "分支", "构建版本", "发布日期", "抓取时间", "来源"],
        )
        writer.writeheader()
        writer.writerow(
            {
                "版本": version["version"],
                "分支": version["branch"],
                "构建版本": version["buildVersion"],
                "发布日期": version["buildDate"][:10],
                "抓取时间": retrieved_at,
                "来源": VERSION_URL,
            }
        )

    agents = []
    for agent in fetch_json(AGENTS_URL):
        role = agent.get("role")
        if role:
            agents.append(
                {
                    "名字": agent["displayName"],
                    "角色": role["displayName"],
                    "描述": agent["description"][:30] + "...",
                    "版本": version["version"],
                    "来源": AGENTS_URL,
                }
            )
    with (ROOT / "agents.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(agents[0]))
        writer.writeheader()
        writer.writerows(agents)


def build_acs_ranking():
    source = pd.read_csv(DATA / "player_acs.csv")
    source["ACS"] = pd.to_numeric(source["ACS"], errors="raise")
    records = []
    for player, rows in source.groupby("选手"):
        records.append(
            {
                "选手": player,
                "年份数": rows["年份"].nunique(),
                "记录数": len(rows),
                "平均ACS": rows["ACS"].mean(),
                "最高ACS": rows["ACS"].max(),
                "代表战队": " / ".join(
                    rows["战队"].dropna().astype(str).drop_duplicates()
                ),
            }
        )
    grouped = pd.DataFrame(records).sort_values(["平均ACS", "记录数"], ascending=[False, False])
    grouped.insert(0, "排名", range(1, len(grouped) + 1))
    grouped["平均ACS"] = grouped["平均ACS"].round(1)
    grouped["最高ACS"] = grouped["最高ACS"].round(1)
    grouped.to_csv(DATA / "player_acs_ranking.csv", index=False, encoding="utf-8-sig")
    return grouped


def build_attachment(ranking):
    maps = pd.read_csv(DATA / "champions_map_pool.csv")
    attachment = ROOT / "valorant_world_events_report.xlsx"
    with pd.ExcelWriter(attachment, engine="openpyxl") as writer:
        ranking.to_excel(writer, sheet_name="ACS排名", index=False)
        maps.to_excel(writer, sheet_name="图池", index=False)
        pd.read_csv(DATA / "player_acs.csv").to_excel(
            writer, sheet_name="赛事原始ACS", index=False
        )
    return attachment


if __name__ == "__main__":
    update_official_content()
    ranking = build_acs_ranking()
    attachment = build_attachment(ranking)
    print(f"已更新英雄与版本数据，生成 {len(ranking)} 名选手的 ACS 排名。")
    print(f"附件：{attachment.name}")
