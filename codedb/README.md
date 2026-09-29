# 本地视频资料库（DevArtifact Registry）静态索引系统

根据本地磁盘 `tree /F` 导出的文本（`haa.txt` 与 `qaa.txt`）构建的个人静态检索库。
完全**脱机运行**，不需要请求外部在线网站，支持**多磁盘文件合并、番号识别、女优分类归集、极速模糊检索**与**增量更新比对**。

---

## 一、核心特性

1. **开发者控制台极客风 UI**
   - 界面整体伪装为开发者资产与构建跟踪平台（`DevArtifact Registry`），低调暗黑风格，无任何露骨或敏感主标题。
   - 部署到外网服务器/托管平台时，具备密码防护拦截层。

2. **访问密码拦截**
   - **默认访问密码**：`kmc:1ere`
   - 支持浏览器 `localStorage` 自动记忆，无需每次刷新重复输入，右上角提供快速锁定（Lock）按钮。

3. **数据整理与归并**
   - **优先番号主键去重**：如同一番号在不同路径存在时间戳剪片、多清晰度切片、或分属两个磁盘，会自动合并到一个卡片下，归并展示所有关联文件。
   - **女优大类联动**：左侧侧边栏按女优（分类）动态聚合作品数量，点击即可瞬间过滤。
   - **未分类（Misc）归集**：无番号、纯中文/英文日常标题的视频统一归入“未分类（Uncategorized）”，依然支持路径与文件名全文检索。
   - **磁盘来源标注**：清晰标识文件来自 `16Tdata3` (haa) 还是 `4000WD` (qaa)。

4. **单文件静态发布**
   - 生成的 [index.html](file:///d:/Agent/personal/TREE/index.html) 为纯静态独立单文件（内嵌压缩索引），无任何外部数据库服务依赖，双击即可本地浏览器打开，也可直接上传到任意静态托管平台（GitHub Pages / Cloudflare Pages / Vercel / Nginx 等）。

---

## 二、文件结构

```text
D:\Agent\personal\TREE\
├── haa.txt            # 磁盘 16Tdata3 的原始 tree /F 文本文件 (GB2312)
├── qaa.txt            # 磁盘 4000WD 的原始 tree /F 文本文件 (GB2312)
├── parse_tree.py      # 文本解析引擎：抽取视频、识别番号与女优、清洗标题与去重
├── db.json            # 生成的标准 JSON 数据集（真实数据源）
├── build_site.py      # 静态网站生成器：将 db.json 打包进 index.html
├── diff_update.py     # 差异比对与增量更新工具
├── index.html         # 生成好的最终静态网站（单文件即开即用）
└── README.md          # 本说明文档
```

---

## 三、常用操作指令

### 1. 浏览查看网页
直接在文件管理器中双击 [index.html](file:///d:/Agent/personal/TREE/index.html)，输入密码 `kmc:1ere` 即可使用。

### 2. 重新全量构建
如果修改了解析规则或重新配置：
```bash
python parse_tree.py
python build_site.py
```

### 3. 当硬盘有新增视频时（差异更新）

当你往移动硬盘或本地磁盘添加了新视频后：

1. **重新导出该磁盘的 tree 文件**（在对应的盘符根目录下执行，例如导出到 D 盘）：
   ```cmd
   # 针对 16Tdata3 盘:
   tree /F H:\ > haa_new.txt

   # 针对 4000WD 盘:
   tree /F Q:\ > qaa_new.txt
   ```

2. **运行智能体增量比对工具**：
   ```bash
   # 更新 16Tdata3 盘：
   python diff_update.py --vol haa --new haa_new.txt

   # 更新 4000WD 盘：
   python diff_update.py --vol qaa --new qaa_new.txt
   ```
   **脚本会自动执行以下流程**：
   - 自动读取并对比新旧文件指纹（识别新增了哪些视频文件）；
   - 自动识别番号，已有番号自动把新文件追加进条目，新番号创建新条目，无番号归入 Misc；
   - 更新保存 `db.json`；
   - **自动重新编译打包 `index.html`**，完成数据更新！

---

## 四、外网部署建议

如需将 `index.html` 部署至外网：
1. **GitHub Pages / Gitee Pages**：直接将 `index.html` 放入仓库根目录启用 Pages 即可；
2. **Cloudflare Pages / Vercel**：将项目文件夹关联或拖拽上传，免服务器免配置；
3. **自建 Nginx / Apache**：将 `index.html` 拷贝至 Web 根目录即可。
4. **修改密码**：如需更换密码，可直接编辑 `build_site.py` 中的 `AUTH_KEY = '你的新密码'`，重新执行 `python build_site.py` 即可。
