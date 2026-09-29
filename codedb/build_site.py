#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_site.py
读取 db.json，生成伪装成程序员开发者平台（DevAsset Registry / Code Trace Explorer）的单文件静态网页 index.html。
包含：
1. 默认密码保护 (默认密码: kmc:1ere，带记忆功能)
2. 程序员极客 UI（VS Code / Terminal 暗黑风格，低调标题）
3. 女优大类分类筛选、按番号搜索、快捷过滤（Coded / Uncategorized）、多磁盘标识 (16Tdata3 / 4000WD)
4. 去重合并后关联文件明细展示
"""

import json
import os
import sys
import io

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def build_html():
    db_file = os.path.join(os.path.dirname(__file__), 'db.json')
    if not os.path.exists(db_file):
        print(f"Error: {db_file} not found. Run parse_tree.py first.")
        sys.exit(1)

    with open(db_file, 'r', encoding='utf-8') as f:
        db_data = json.load(f)

    # 压缩 JSON 注入页面
    db_json_str = json.dumps(db_data, ensure_ascii=False, separators=(',', ':'))

    html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DevArtifact Registry &amp; Build Trace</title>
  <style>
    :root {{
      --bg: #121417;
      --panel: #1a1d24;
      --panel-border: #2b303c;
      --text: #c9d1d9;
      --text-muted: #6e7681;
      --accent: #388bfd;
      --accent-hover: #58a6ff;
      --tag-bg: #21262d;
      --tag-border: #30363d;
      --badge-actress: #1f6feb33;
      --badge-actress-txt: #79c0ff;
      --badge-vol-haa: #23863633;
      --badge-vol-haa-txt: #7ee787;
      --badge-vol-qaa: #9e6a0333;
      --badge-vol-qaa-txt: #e3b341;
      --font-mono: 'Consolas', 'Courier New', monospace;
      --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-mono);
      font-size: 13px;
      line-height: 1.5;
      min-height: 100vh;
    }}

    /* Password Modal / Gate */
    #auth-overlay {{
      position: fixed;
      inset: 0;
      background: #0d1117;
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 99999;
    }}
    .auth-box {{
      background: var(--panel);
      border: 1px solid var(--panel-border);
      border-radius: 6px;
      padding: 24px;
      width: 360px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }}
    .auth-header {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 14px;
      font-weight: 600;
      color: #58a6ff;
      margin-bottom: 16px;
      border-bottom: 1px solid var(--panel-border);
      padding-bottom: 8px;
    }}
    .auth-input {{
      width: 100%;
      background: #0d1117;
      border: 1px solid var(--panel-border);
      border-radius: 4px;
      padding: 8px 12px;
      color: #fff;
      font-family: var(--font-mono);
      margin-bottom: 12px;
      outline: none;
    }}
    .auth-input:focus {{
      border-color: var(--accent);
    }}
    .auth-btn {{
      width: 100%;
      background: #238636;
      border: none;
      border-radius: 4px;
      padding: 8px;
      color: #fff;
      cursor: pointer;
      font-family: var(--font-mono);
      font-weight: bold;
    }}
    .auth-btn:hover {{ background: #2ea043; }}
    .auth-error {{
      color: #f85149;
      font-size: 12px;
      margin-top: 8px;
      display: none;
    }}

    /* Main Layout */
    #app {{ display: none; min-height: 100vh; }}
    header {{
      background: var(--panel);
      border-bottom: 1px solid var(--panel-border);
      padding: 10px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 100;
    }}
    .logo-area {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .logo-icon {{
      width: 16px;
      height: 16px;
      border-radius: 3px;
      background: #3fb950;
      display: inline-block;
    }}
    .logo-title {{
      font-weight: 600;
      font-size: 14px;
      color: #f0f6fc;
      letter-spacing: 0.5px;
    }}
    .logo-badge {{
      background: #30363d;
      color: #8b949e;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 11px;
    }}

    .container {{
      display: grid;
      grid-template-columns: 280px 1fr;
      min-height: calc(100vh - 49px);
    }}

    /* Sidebar / Category View */
    sidebar {{
      background: #14171d;
      border-right: 1px solid var(--panel-border);
      padding: 16px;
      overflow-y: auto;
      height: calc(100vh - 49px);
      position: sticky;
      top: 49px;
    }}
    .sidebar-title {{
      font-size: 12px;
      font-weight: bold;
      text-transform: uppercase;
      color: var(--text-muted);
      margin-bottom: 10px;
      letter-spacing: 0.5px;
      display: flex;
      justify-content: space-between;
    }}
    .actress-search {{
      width: 100%;
      background: #0d1117;
      border: 1px solid var(--panel-border);
      border-radius: 4px;
      padding: 6px 10px;
      color: #fff;
      font-family: var(--font-mono);
      font-size: 12px;
      margin-bottom: 12px;
      outline: none;
    }}
    .actress-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 2px;
      max-height: calc(100vh - 180px);
      overflow-y: auto;
    }}
    .actress-item {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 5px 8px;
      border-radius: 4px;
      cursor: pointer;
      color: #8b949e;
      font-size: 12px;
    }}
    .actress-item:hover {{
      background: #1c2128;
      color: #c9d1d9;
    }}
    .actress-item.active {{
      background: #1f6feb22;
      color: #58a6ff;
      font-weight: 600;
    }}
    .actress-count {{
      font-size: 11px;
      background: #21262d;
      padding: 1px 6px;
      border-radius: 10px;
      color: #6e7681;
    }}

    /* Content Area */
    main {{
      padding: 20px;
      overflow-y: auto;
    }}
    .toolbar {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 16px;
      align-items: center;
    }}
    .search-input {{
      flex: 1;
      min-width: 260px;
      background: var(--panel);
      border: 1px solid var(--panel-border);
      border-radius: 4px;
      padding: 8px 12px;
      color: #fff;
      font-family: var(--font-mono);
      outline: none;
    }}
    .search-input:focus {{
      border-color: var(--accent);
    }}
    .filter-tabs {{
      display: flex;
      gap: 4px;
      background: #0d1117;
      padding: 3px;
      border-radius: 6px;
      border: 1px solid var(--panel-border);
    }}
    .filter-btn {{
      background: transparent;
      border: none;
      color: #8b949e;
      padding: 5px 12px;
      border-radius: 4px;
      cursor: pointer;
      font-family: var(--font-mono);
      font-size: 12px;
    }}
    .filter-btn.active {{
      background: #21262d;
      color: #58a6ff;
      font-weight: 600;
    }}
    .stats-bar {{
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 12px;
      display: flex;
      gap: 16px;
    }}

    /* Item Grid / List */
    .item-list {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .entry-card {{
      background: var(--panel);
      border: 1px solid var(--panel-border);
      border-radius: 6px;
      padding: 8px 14px;
      transition: all 0.18s ease;
      cursor: pointer;
      user-select: none;
    }}
    .entry-card:hover {{
      border-color: #58a6ff;
      background: #1e222b;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }}
    .card-top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }}
    .card-id {{
      font-size: 13px;
      font-weight: bold;
      color: #58a6ff;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .card-id.misc-id {{
      color: #8b949e;
      font-weight: normal;
      font-style: italic;
    }}
    .file-pill {{
      font-size: 10px;
      background: #21262d;
      color: #8b949e;
      padding: 1px 6px;
      border-radius: 10px;
      font-weight: normal;
    }}
    .badges {{
      display: flex;
      gap: 6px;
      align-items: center;
    }}
    .card-toggle-icon {{
      font-size: 11px;
      color: #6e7681;
      transition: transform 0.2s ease;
      margin-left: 6px;
    }}
    .entry-card:hover .card-toggle-icon,
    .entry-card.is-expanded .card-toggle-icon {{
      transform: rotate(180deg);
      color: #58a6ff;
    }}

    /* Anti-Peek Collapsible Content (Default Hidden) */
    .card-body {{
      display: none;
      margin-top: 10px;
      padding-top: 8px;
      border-top: 1px solid #282e39;
      user-select: text;
    }}
    /* Hover on desktop */
    @media (hover: hover) {{
      .entry-card:hover .card-body {{
        display: block;
      }}
    }}
    /* Tap or clicked state on all devices */
    .entry-card.is-expanded .card-body {{
      display: block !important;
    }}

    .badge {{
      font-size: 11px;
      padding: 1px 6px;
      border-radius: 3px;
      border: 1px solid transparent;
    }}
    .badge-actress {{
      background: var(--badge-actress);
      color: var(--badge-actress-txt);
      border-color: #388bfd44;
    }}
    .badge-vol-haa {{
      background: var(--badge-vol-haa);
      color: var(--badge-vol-haa-txt);
      border-color: #2ea04344;
    }}
    .badge-vol-qaa {{
      background: var(--badge-vol-qaa);
      color: var(--badge-vol-qaa-txt);
      border-color: #d2992244;
    }}
    .card-title {{
      font-size: 12px;
      color: #e6edf3;
      margin-bottom: 8px;
      line-height: 1.5;
      word-break: break-all;
    }}
    .file-details {{
      background: #111419;
      border-radius: 4px;
      padding: 6px 10px;
      margin-top: 6px;
      border: 1px solid #21262d;
    }}
    .file-row {{
      font-size: 11px;
      color: #8b949e;
      display: flex;
      justify-content: space-between;
      padding: 2px 0;
      border-bottom: 1px dashed #21262d;
    }}
    .file-row:last-child {{ border-bottom: none; }}
    .file-name {{
      color: #c9d1d9;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      max-width: 75%;
    }}

    .pagination {{
      margin-top: 20px;
      display: flex;
      justify-content: center;
      gap: 8px;
      align-items: center;
    }}
    .page-btn {{
      background: var(--panel);
      border: 1px solid var(--panel-border);
      color: #c9d1d9;
      padding: 4px 10px;
      border-radius: 4px;
      cursor: pointer;
      font-family: var(--font-mono);
    }}
    .page-btn:disabled {{
      opacity: 0.4;
      cursor: not-allowed;
    }}

    /* Mobile Responsive Optimizations */
    .drawer-btn {{
      display: none;
      background: #21262d;
      border: 1px solid var(--panel-border);
      color: #58a6ff;
      padding: 4px 10px;
      border-radius: 4px;
      font-size: 12px;
      cursor: pointer;
      font-family: var(--font-mono);
      align-items: center;
      gap: 6px;
    }}
    .drawer-btn:active {{ background: #30363d; }}

    #sidebar-backdrop {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(2px);
      z-index: 998;
    }}

    @media (max-width: 768px) {{
      .drawer-btn {{ display: inline-flex; }}

      .container {{
        grid-template-columns: 1fr;
      }}

      sidebar {{
        position: fixed;
        left: -300px;
        top: 0;
        bottom: 0;
        width: 285px;
        height: 100vh;
        z-index: 999;
        box-shadow: 6px 0 24px rgba(0,0,0,0.7);
        transition: left 0.24s cubic-bezier(0.4, 0, 0.2, 1);
        padding: 16px 14px;
      }}
      sidebar.open {{
        left: 0;
      }}
      #sidebar-backdrop.active {{
        display: block;
      }}

      header {{
        padding: 8px 12px;
        flex-wrap: wrap;
        gap: 8px;
      }}
      .logo-title {{
        font-size: 13px;
      }}
      #disk-info {{
        display: none;
      }}

      main {{
        padding: 12px 10px;
      }}

      .toolbar {{
        flex-direction: column;
        align-items: stretch;
        gap: 8px;
      }}
      .search-input {{
        width: 100%;
        padding: 9px 12px;
        font-size: 13px;
      }}
      .filter-tabs {{
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        width: 100%;
      }}
      .filter-btn {{
        text-align: center;
        padding: 6px 2px;
        font-size: 11px;
      }}

      .stats-bar {{
        font-size: 11px;
        flex-direction: column;
        gap: 4px;
      }}

      .entry-card {{
        padding: 10px 12px;
      }}
      .card-id {{
        font-size: 13px;
      }}
      .file-row {{
        flex-direction: column;
        align-items: flex-start;
        gap: 2px;
        padding: 5px 0;
      }}
      .file-name {{
        max-width: 100%;
        white-space: normal;
        word-break: break-all;
      }}

      .page-btn {{
        padding: 8px 16px;
        font-size: 13px;
      }}
    }}
  </style>
</head>
<body>

  <!-- Password Shield -->
  <div id="auth-overlay">
    <div class="auth-box">
      <div class="auth-header">
        <span style="font-size:16px;">&#128274;</span>
        <span>Internal Developer Console</span>
      </div>
      <div style="font-size: 12px; color: #8b949e; margin-bottom: 12px;">
        Authentication required to access local build trace &amp; asset catalog.
      </div>
      <form id="auth-form" onsubmit="handleAuth(event)">
        <input type="password" id="auth-pwd" class="auth-input" placeholder="Access Token / Secret" autofocus>
        <button type="submit" class="auth-btn">Verify Access</button>
        <div id="auth-msg" class="auth-error">Invalid access token.</div>
      </form>
    </div>
  </div>

  <!-- Main System Explorer -->
  <div id="app">
    <div id="sidebar-backdrop" onclick="toggleSidebar(false)"></div>
    <header>
      <div class="logo-area">
        <button class="drawer-btn" onclick="toggleSidebar(true)">&#9776; Categories</button>
        <span class="logo-icon"></span>
        <span class="logo-title">DevArtifact Registry</span>
        <span class="logo-badge">v1.2-build</span>
      </div>
      <div style="display:flex; align-items:center; gap: 14px;">
        <span id="kv-status" style="font-size:11px;color:#8b949e;display:flex;align-items:center;gap:5px;">
          <span id="kv-dot" style="display:inline-block;width:7px;height:7px;border-radius:50%;background:#d29922;"></span>
          <span id="kv-text">Syncing KV...</span>
        </span>
        <span id="disk-info" style="color: var(--text-muted); font-size: 11px;">Mounted: 16Tdata3, 4000WD</span>
        <button onclick="logout()" class="filter-btn" style="border: 1px solid var(--panel-border);">Lock</button>
      </div>
    </header>

    <div class="container">
      <sidebar id="main-sidebar">
        <div class="sidebar-title">
          <span>Categories (Actresses)</span>
          <div style="display:flex;align-items:center;gap:8px;">
            <span id="actress-total-count" style="font-weight:normal;">0</span>
            <button onclick="toggleSidebar(false)" class="drawer-btn" style="padding:1px 6px;font-size:11px;color:#8b949e;">✕</button>
          </div>
        </div>
        <input type="text" id="actress-filter" class="actress-search" placeholder="Filter category..." oninput="renderActressList()">
        <ul id="actress-list" class="actress-list"></ul>
      </sidebar>

      <main>
        <div class="toolbar">
          <input type="text" id="global-search" class="search-input" placeholder="Search by Code (番号), Title, or Path... (Regex supported)" oninput="handleSearch()">
          <div class="filter-tabs">
            <button class="filter-btn active" id="tab-all" onclick="setTab('all')">All (<span id="count-all">0</span>)</button>
            <button class="filter-btn" id="tab-coded" onclick="setTab('coded')">Coded 番号 (<span id="count-coded">0</span>)</button>
            <button class="filter-btn" id="tab-misc" onclick="setTab('misc')">Uncategorized (<span id="count-misc">0</span>)</button>
          </div>
        </div>

        <div class="stats-bar">
          <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
            <span id="result-stats">Showing 0 entries</span>
            <span id="filter-tag-hint" style="color:#58a6ff;"></span>
            <button id="btn-clear-filter" onclick="selectActress(null)" style="display:none;background:#21262d;border:1px solid #30363d;color:#f85149;padding:1px 6px;border-radius:3px;font-size:10px;cursor:pointer;">Clear ✕</button>
          </div>
        </div>

        <div id="item-list" class="item-list"></div>

        <div class="pagination">
          <button id="btn-prev" class="page-btn" onclick="changePage(-1)">&lt; Prev</button>
          <span id="page-indicator" style="font-size: 12px; color: var(--text-muted);">Page 1 / 1</span>
          <button id="btn-next" class="page-btn" onclick="changePage(1)">Next &gt;</button>
        </div>
      </main>
    </div>
  </div>

  <script>
    // Embedded Local Cache Data
    let RAW_DB = {db_json_str};

    // Upstash / Vercel KV Online Config
    const KV_API_URL = "https://deciding-bulldog-136761.upstash.io/get/codedb:all";
    const KV_RO_TOKEN = "ggAAAAAAAhY5AAIgcDG7a511dMnvUap5JjML7kdCMH0hQAG95-3BtwD6YEaFeQ";

    // Auth logic
    const AUTH_KEY = 'kmc:1ere';
    const STORAGE_KEY = 'dev_registry_token';

    function initAuth() {{
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved === AUTH_KEY) {{
        unlock();
      }}
    }}

    function handleAuth(e) {{
      e.preventDefault();
      const val = document.getElementById('auth-pwd').value;
      if (val === AUTH_KEY) {{
        localStorage.setItem(STORAGE_KEY, AUTH_KEY);
        unlock();
      }} else {{
        document.getElementById('auth-msg').style.display = 'block';
      }}
    }}

    function unlock() {{
      document.getElementById('auth-overlay').style.display = 'none';
      document.getElementById('app').style.display = 'block';
      initApp();
      syncOnlineKV();
    }}

    function syncOnlineKV() {{
      const dot = document.getElementById('kv-dot');
      const txt = document.getElementById('kv-text');
      dot.style.background = '#d29922';
      txt.innerText = 'Syncing KV...';

      fetch(KV_API_URL, {{
        headers: {{ 'Authorization': 'Bearer ' + KV_RO_TOKEN }}
      }})
      .then(res => {{
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      }})
      .then(data => {{
        if (data && data.result) {{
          const remoteDB = typeof data.result === 'string' ? JSON.parse(data.result) : data.result;
          if (remoteDB && remoteDB.coded) {{
            RAW_DB = remoteDB;
            dot.style.background = '#3fb950';
            txt.innerText = 'Live KV Online';
            initApp();
            return;
          }}
        }}
        dot.style.background = '#8b949e';
        txt.innerText = 'Local Cache';
      }})
      .catch(err => {{
        console.warn('KV offline / using local cache:', err);
        dot.style.background = '#8b949e';
        txt.innerText = 'Local Cache';
      }});
    }}

    function logout() {{
      localStorage.removeItem(STORAGE_KEY);
      location.reload();
    }}

    // App Data State
    let currentTab = 'all'; // all, coded, misc
    let selectedActress = null;
    let searchQuery = '';
    let currentPage = 1;
    const PAGE_SIZE = 50;

    let allEntries = [];
    let filteredEntries = [];
    let actressCounts = {{}};

    function initApp() {{
      // 合并 coded 和 misc 形成统一扁平集合
      const coded = (RAW_DB.coded || []).map(item => ({{ ...item, isCoded: true }}));
      const misc = (RAW_DB.misc || []).map(item => ({{ ...item, isCoded: false }}));
      allEntries = [...coded, ...misc];

      document.getElementById('count-all').innerText = allEntries.length;
      document.getElementById('count-coded').innerText = coded.length;
      document.getElementById('count-misc').innerText = misc.length;

      // 统计所有女优
      actressCounts = {{}};
      allEntries.forEach(item => {{
        if (item.actresses && item.actresses.length > 0) {{
          item.actresses.forEach(a => {{
            actressCounts[a] = (actressCounts[a] || 0) + 1;
          }});
        }}
      }});

      renderActressList();
      applyFilters();
    }}

    function renderActressList() {{
      const query = (document.getElementById('actress-filter').value || '').toLowerCase();
      const listEl = document.getElementById('actress-list');
      listEl.innerHTML = '';

      // All actresses
      const allItem = document.createElement('li');
      allItem.className = 'actress-item' + (!selectedActress ? ' active' : '');
      allItem.innerHTML = `<span>[All Categories]</span><span class="actress-count">${{allEntries.length}}</span>`;
      allItem.onclick = () => selectActress(null);
      listEl.appendChild(allItem);

      const sortedNames = Object.keys(actressCounts).sort((a,b) => actressCounts[b] - actressCounts[a]);
      let visibleCount = 0;

      sortedNames.forEach(name => {{
        if (query && !name.toLowerCase().includes(query)) return;
        visibleCount++;
        const li = document.createElement('li');
        li.className = 'actress-item' + (selectedActress === name ? ' active' : '');
        li.innerHTML = `<span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="${{escapeHtml(name)}}">${{escapeHtml(name)}}</span><span class="actress-count">${{actressCounts[name]}}</span>`;
        li.onclick = () => selectActress(name);
        listEl.appendChild(li);
      }});

      document.getElementById('actress-total-count').innerText = `${{visibleCount}} / ${{sortedNames.length}}`;
    }}

    function toggleSidebar(open) {{
      const sb = document.getElementById('main-sidebar');
      const bd = document.getElementById('sidebar-backdrop');
      if (open === undefined) {{
        const isOpen = sb.classList.contains('open');
        toggleSidebar(!isOpen);
      }} else if (open) {{
        sb.classList.add('open');
        bd.classList.add('active');
      }} else {{
        sb.classList.remove('open');
        bd.classList.remove('active');
      }}
    }}

    function selectActress(name) {{
      selectedActress = name;
      currentPage = 1;
      renderActressList();
      applyFilters();
      if (window.innerWidth <= 768) {{
        toggleSidebar(false);
      }}
    }}

    function setTab(tab) {{
      currentTab = tab;
      currentPage = 1;
      document.querySelectorAll('.filter-tabs .filter-btn').forEach(btn => btn.classList.remove('active'));
      document.getElementById('tab-' + tab).classList.add('active');
      applyFilters();
    }}

    function handleSearch() {{
      searchQuery = document.getElementById('global-search').value.trim();
      currentPage = 1;
      applyFilters();
    }}

    function applyFilters() {{
      const q = searchQuery.toLowerCase();

      filteredEntries = allEntries.filter(item => {{
        // Tab filter
        if (currentTab === 'coded' && !item.isCoded) return false;
        if (currentTab === 'misc' && item.isCoded) return false;

        // Actress filter
        if (selectedActress) {{
          if (!item.actresses || !item.actresses.includes(selectedActress)) return false;
        }}

        // Text Search (id, title, files)
        if (q) {{
          const idMatch = item.id && item.id.toLowerCase().includes(q);
          const titleMatch = item.title && item.title.toLowerCase().includes(q);
          const actressMatch = item.actresses && item.actresses.some(a => a.toLowerCase().includes(q));
          let fileMatch = false;
          if (item.files) {{
            fileMatch = item.files.some(f => (f.name && f.name.toLowerCase().includes(q)) || (f.dir && f.dir.toLowerCase().includes(q)));
          }}
          if (!idMatch && !titleMatch && !actressMatch && !fileMatch) return false;
        }}

        return true;
      }});

      // 更新状态文字与快速清除按钮
      const hint = selectedActress ? `[Category: ${{selectedActress}}]` : '';
      document.getElementById('filter-tag-hint').innerText = hint;
      document.getElementById('btn-clear-filter').style.display = selectedActress ? 'inline-block' : 'none';
      document.getElementById('result-stats').innerText = `Matched ${{filteredEntries.length}} records`;

      renderPage();
    }}

    function renderPage() {{
      const totalPages = Math.ceil(filteredEntries.length / PAGE_SIZE) || 1;
      if (currentPage > totalPages) currentPage = totalPages;
      if (currentPage < 1) currentPage = 1;

      document.getElementById('page-indicator').innerText = `Page ${{currentPage}} / ${{totalPages}}`;
      document.getElementById('btn-prev').disabled = currentPage <= 1;
      document.getElementById('btn-next').disabled = currentPage >= totalPages;

      const start = (currentPage - 1) * PAGE_SIZE;
      const pageData = filteredEntries.slice(start, start + PAGE_SIZE);

      const listEl = document.getElementById('item-list');
      listEl.innerHTML = '';

      if (pageData.length === 0) {{
        listEl.innerHTML = '<div style="color:var(--text-muted);text-align:center;padding:40px;">No matching records found.</div>';
        return;
      }}

      pageData.forEach(item => {{
        const card = document.createElement('div');
        card.className = 'entry-card';

        const idText = item.id || '(Uncategorized / No Code)';
        const idClass = item.id ? 'card-id' : 'card-id misc-id';

        let volBadgesHtml = '';
        if (item.vols && item.vols.length > 0) {{
          volBadgesHtml = item.vols.map(v => {{
            const cls = v === 'haa' ? 'badge-vol-haa' : 'badge-vol-qaa';
            const label = v === 'haa' ? '16Tdata3' : '4000WD';
            return `<span class="badge ${{cls}}">${{label}}</span>`;
          }}).join('');
        }}

        let actressBadgesHtml = '';
        if (item.actresses && item.actresses.length > 0) {{
          actressBadgesHtml = `<div style="margin-bottom:6px;display:flex;gap:4px;flex-wrap:wrap;">` +
            item.actresses.map(a => `<span class="badge badge-actress">${{escapeHtml(a)}}</span>`).join('') +
            `</div>`;
        }}

        let filesHtml = '';
        if (item.files && item.files.length > 0) {{
          filesHtml = `<div class="file-details">
            <div style="font-size:10px;color:var(--text-muted);margin-bottom:4px;">ATTACHED FILES (${{item.files.length}}):</div>
            ${{item.files.map(f => `
              <div class="file-row">
                <span class="file-name" title="${{escapeHtml(f.dir + '/' + f.name)}}">&#128196; ${{escapeHtml(f.name)}}</span>
                <span style="color:#6e7681;">${{escapeHtml(f.dir || '')}}</span>
              </div>
            `).join('')}}
          </div>`;
        }}

        const fileCount = item.files ? item.files.length : 0;
        const fileCountPill = fileCount > 1 ? `<span class="file-pill">${{fileCount}} parts</span>` : '';

        let subBadge = item.is_sub ? '<span class="badge" style="background:#23863622;color:#3fb950;border-color:#23863644;font-size:10px;">SUB</span>' : '';
        let rmBadge = item.is_rm ? '<span class="badge" style="background:#a371f722;color:#d2a8ff;border-color:#a371f744;font-size:10px;">RM</span>' : '';

        card.innerHTML = `
          <div class="card-top">
            <span class="${{idClass}}">
              <span>${{escapeHtml(idText)}}</span>
              ${{fileCountPill}}
            </span>
            <div class="badges">
              ${{subBadge}}
              ${{rmBadge}}
              ${{volBadgesHtml}}
              <span class="card-toggle-icon">&#9662;</span>
            </div>
          </div>
          <div class="card-body">
            ${{actressBadgesHtml}}
            <div class="card-title">${{escapeHtml(item.title || '(No Title Description)')}}</div>
            ${{filesHtml}}
          </div>
        `;

        // Tap on mobile / click on desktop to toggle lock expand
        card.onclick = function(e) {{
          // Avoid text selection cancelling
          if (window.getSelection().toString()) return;
          this.classList.toggle('is-expanded');
        }};

        listEl.appendChild(card);
      }});
    }}

    function changePage(delta) {{
      currentPage += delta;
      renderPage();
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function escapeHtml(str) {{
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }}

    // Startup
    initAuth();
  </script>
</body>
</html>'''

    out_file = os.path.join(os.path.dirname(__file__), 'index.html')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html_template)

    print(f"✓ Static site successfully generated: {out_file} ({os.path.getsize(out_file) // 1024} KB)")

    # 自动拷贝到目标 GitHub Pages 仓库
    target_repo_dir = r"d:\#E\Personal\kmcbest.github.io\codedb"
    if os.path.exists(os.path.dirname(target_repo_dir)):
        os.makedirs(target_repo_dir, exist_ok=True)
        target_html = os.path.join(target_repo_dir, "index.html")
        import shutil
        shutil.copyfile(out_file, target_html)
        print(f"✓ Copied to target repository: {target_html} ({os.path.getsize(target_html) // 1024} KB)")

if __name__ == '__main__':
    build_html()
