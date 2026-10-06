# TFTF 智能体能力与角色数据真理源接口规范 (Agent Source of Truth API)

> 本文档专供各类 AI 智能体（Subagents、LLM 编写助手、代码生成工作流）查询使用。
> 编写角色 Ability 代码、战斗 Hook、数值公式及机制判定时，必须以此真理源中的数据为准。

---

## 1. 快速查询端点 (Endpoints)

### 静态真理源 CDN（免鉴权、零延迟、全球 CDN 缓存）

| 资源 | URL | 说明 |
| :--- | :--- | :--- |
| **优先实现能力列表 (待办)** | `https://kmcbest.github.io/tftfr/data/priority_abilities.json` | 当前被标记为优先实现（status='priority'）的能力列表（供智能体直取实现任务） |
| **全角色技能总库** | `https://kmcbest.github.io/tftfr/data/all_abilities.json` | 包含全部 78 位角色、1320 项技能及机制描述的完整字典 |
| **全角色概览与 6/60 属性** | `https://kmcbest.github.io/tftfr/data/overview.json` | 阵营、职业默认倍率、生命值 (HP)、攻击力 (ATK)、评分 (Rating) |
| **单机体详细档案** | `https://kmcbest.github.io/tftfr/data/characters/{bot_id}.json` | 指定机体的所有被动、特殊技 (SP1/SP2/SP3)、觉醒技 (Signature) 与协同羁绊 |
| **PUA 专用字体码表** | `https://kmcbest.github.io/tftfr/data/pua_icons.json` | 游戏中所有派系、职业与战技图标的 Unicode 十六进制码 |

### 动态云数据库（实时在线，支持即时修改）

- **Upstash KV REST URL**: `https://deciding-bulldog-136761.upstash.io`
- **只读 Token (Read-Only Token)**: `ggAAAAAAAhY5AAIgcDG7a511dMnvUap5JjML7kdCMH0hQAG95-3BtwD6YEaFeQ`
- **查询优先实现能力列表**:
  ```bash
  curl -H "Authorization: Bearer ggAAAAAAAhY5AAIgcDG7a511dMnvUap5JjML7kdCMH0hQAG95-3BtwD6YEaFeQ" \
       https://deciding-bulldog-136761.upstash.io/get/tftf:priority_abilities
  ```
- **查询单机体实时数据**:
  ```bash
  curl -H "Authorization: Bearer ggAAAAAAAhY5AAIgcDG7a511dMnvUap5JjML7kdCMH0hQAG95-3BtwD6YEaFeQ" \
       https://deciding-bulldog-136761.upstash.io/get/tftf:char:{bot_id}
  ```

---

## 2. 网页端交互与 Prompt 生成器

- **地址**: `https://kmcbest.github.io/tftfr/api.html`
- **参数支持**:
  - `?bot=grimlock` 或 `?bid=grimlock_gs_mp08`：指定角色名或 ID（支持中文如 `?bot=钢锁`）。
  - `?format=markdown`：生成可直接喂给大模型的 Prompt 格式。
  - `?format=json`：输出标准结构化 JSON。
  - `?format=hooks`：输出 C / Python Hook 代码脚手架。

---

## 3. 智能体代码接入示例 (Python)

### 3.1 获取任意角色的技能与 6/60 数值

```python
import json
import urllib.request

def get_bot_abilities(bot_id: str) -> dict:
    url = f"https://kmcbest.github.io/tftfr/data/characters/{bot_id}.json"
    req = urllib.request.Request(url, headers={"User-Agent": "TFTF-Agent/1.0"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

# 示例：获取钢锁 (Grimlock) 的技能与机制
bot = get_bot_abilities("grimlock_gs_mp08")
print(f"角色: {bot['name_zh']} ({bot['name_en']})")
print(f"5星 6/60 HP: {bot['hp']}, ATK: {bot['attack']}, Rating: {bot['rating']}")
for ab in bot.get("abilities", []):
    print(f"[{ab['category'].upper()}] {ab['title_zh']}: {ab['desc_zh']}")
```

### 3.2 模糊检索（中文名 -> 技能描述）

```python
import json
import urllib.request

def search_bot(keyword: str):
    url = "https://kmcbest.github.io/tftfr/data/all_abilities.json"
    with urllib.request.urlopen(url) as resp:
        data = json.loads(resp.read().decode("utf-8"))["bots"]
    
    keyword = keyword.lower()
    for bid, b in data.items():
        if keyword in bid.lower() or keyword in (b["name_zh"] or "") or keyword in (b["name_en"] or "").lower():
            return b
    return None

# 示例：搜索 "眩晕"
bot = search_bot("眩晕")
print(f"找到角色: {bot['name_zh']} ({bot['bot_id']}), 技能数: {len(bot['abilities'])}")
```

---

## 4. 数据结构规范 (Schema)

```json
{
  "bot_id": "grimlock_gs_mp08",
  "name_zh": "钢锁",
  "name_en": "Grimlock",
  "class": "brawler",
  "faction": "autobot",
  "stats_6_60": {
    "hp": 39256,
    "attack": 2490,
    "rating": 10320,
    "health_mult": 1.15,
    "attack_mult": 1.0,
    "crit_chance": 0.20,
    "crit_damage": 1.50,
    "crit_chance_ranged": 0.20,
    "crit_chance_melee": 0.20,
    "block_proficiency": 0.5
  },
  "abilities": [
    {
      "id": 101,
      "bot_id": "grimlock_gs_mp08",
      "category": "passive",
      "title_zh": "暴龙之怒",
      "title_en": "Dino Fury",
      "desc_zh": "受到近战攻击时累积怒气，怒气满时进入不可阻挡状态，攻击力提升 {{var_atk}}%...",
      "pua_icon": "E104",
      "synergy_bots": ["optimusprime_cin_tf"]
    }
  ]
}
```
