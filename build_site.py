#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Showball 信息学 —— 站点生成器 v2
生成：首页 + GESP总览 + 8 等级页 + CSP + 程序模板 + 题解 + OJ资源
"""
import os, io, html, shutil
from site_data import (SITE_NAME, SITE_SUB, LEVELS, CSP, TEMPLATE_CATS,
                       COMMON_TEMPLATES, SOLUTION_STEPS, RESOURCE_GROUPS,
                       KP_DETAILS)

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(ROOT, "site")

BAR_COLORS = ["#5b8def","#7c6bf0","#a56bf0","#d86bc8","#ef6b9c","#ef7b6b","#ef9d6b","#d9a441"]
CN_NUM = ["一","二","三","四","五","六","七","八"]

NAV = [
    ("首页",        "index.html",     "home"),
    ("GESP 1–8 级", "gesp.html",      "gesp"),
    ("CSP-J/S",     "csp.html",       "csp"),
    ("程序模板",    "templates.html", "tpl"),
    ("题解",        "solutions.html", "sol"),
    ("OJ 与资源",   "resources.html", "res"),
]

E = html.escape


# ============================== 样式 ==============================
CSS = """<style>
:root{
  --bg:#f8fafc;--bg-2:#f1f5f9;--card:#fff;--card-2:#f8fafc;
  --line:#e2e8f0;--line-2:#cbd5e1;
  --text:#1e293b;--text-2:#64748b;--text-3:#94a3b8;
  --brand:#6366f1;--brand-2:#4f46e5;--brand-soft:#eef2ff;--navy:#6366f1;
  --accent:#c0392b;--accent-2:#a93226;--accent-soft:#fdf0ee;--accent-text:#c0392b;
  --shadow-sm:0 1px 2px rgba(15,23,42,.05);
  --shadow:0 2px 8px rgba(15,23,42,.06);
  --shadow-lg:0 8px 28px rgba(15,23,42,.10);
  --radius:14px;--radius-sm:10px;--maxw:1120px;
}
[data-theme="dark"]{
  --bg:#0f172a;--bg-2:#1e293b;--card:#1e293b;--card-2:#263548;
  --line:#334155;--line-2:#475569;
  --text:#f1f5f9;--text-2:#94a3b8;--text-3:#64748b;
  --brand:#818cf8;--brand-2:#a5b4fc;--brand-soft:rgba(129,140,248,.14);--navy:#818cf8;
  --accent:#e05a45;--accent-2:#f0705a;--accent-soft:#2e2020;--accent-text:#ffb38f;
  --shadow-sm:0 1px 2px rgba(0,0,0,.25);
  --shadow:0 2px 8px rgba(0,0,0,.3);
  --shadow-lg:0 8px 28px rgba(0,0,0,.45);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);
  font-family:system-ui,-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei","Segoe UI",Roboto,sans-serif;
  line-height:1.7;-webkit-font-smoothing:antialiased;
  min-height:100vh;display:flex;flex-direction:column;transition:background .25s,color .25s}
a{color:inherit;text-decoration:none}
::selection{background:var(--brand);color:#fff}
main{flex:1 0 auto;width:100%}

/* ---------- 顶栏 ---------- */
header{position:sticky;top:0;z-index:60;background:var(--card);
  backdrop-filter:saturate(180%) blur(14px);border-bottom:1px solid var(--line)}
.bar{max-width:var(--maxw);margin:0 auto;padding:10px 20px;display:flex;align-items:center;gap:18px}
.brand{display:flex;align-items:center;gap:10px;flex:0 0 auto}
.logo{width:auto;height:auto;border-radius:0;flex:0 0 auto;
  background:none;display:grid;place-items:center;
  color:var(--brand);font-size:22px;font-weight:850;letter-spacing:-.025em;line-height:1}
.brand-txt b{display:block;font-size:15.5px;font-weight:700;line-height:1.3}
.brand-txt small{display:block;font-size:11px;color:var(--text-3);line-height:1.3}
nav{display:flex;gap:2px;margin:0 auto;flex-wrap:wrap}
nav a{padding:7px 13px;border-radius:8px;font-size:14px;color:var(--text-2);transition:.16s;white-space:nowrap}
nav a:hover{color:var(--text);background:var(--bg-2)}
nav a.active{color:var(--brand);background:var(--brand-soft);font-weight:600}
.bar-right{display:flex;align-items:center;gap:10px;flex:0 0 auto}
.mini-search{display:flex;align-items:center;gap:7px;background:var(--bg-2);
  border:1px solid var(--line);border-radius:9px;padding:7px 12px;width:210px;
  color:var(--text-3);font-size:13px;cursor:text;transition:.18s}
.mini-search:hover{border-color:var(--line-2)}
.theme-btn{width:36px;height:36px;border-radius:50%;flex:0 0 auto;background:var(--bg-2);
  border:1px solid var(--line);color:var(--text-2);cursor:pointer;
  display:grid;place-items:center;transition:.18s;font-size:15px}
.theme-btn:hover{border-color:var(--brand);color:var(--brand)}

/* ---------- 页脚 ---------- */
footer{background:#0f172a;color:#94a3b8;padding:38px 20px 26px;font-size:13px;margin-top:auto}
.fwrap{max-width:var(--maxw);margin:0 auto;display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:32px}
.fbrand b{display:block;color:#f1f5f9;font-size:15px;font-weight:700;margin-bottom:6px}
.fbrand p{margin:0;font-size:12.5px;line-height:1.7;opacity:.75}
.fcol h5{margin:0 0 10px;font-size:13px;color:#cbd5e1;font-weight:600}
.fcol a{display:block;padding:3px 0;font-size:12.5px;opacity:.8;transition:.15s}
.fcol a:hover{color:#fff;opacity:1}
.fbottom{max-width:var(--maxw);margin:26px auto 0;padding-top:18px;
  border-top:1px solid #1e293b;font-size:11.5px;opacity:.6;line-height:1.7}

/* ---------- 通用 ---------- */
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 20px 64px}
.panel{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow-sm)}
.link-red{color:var(--brand);font-size:14px;font-weight:600;
  display:inline-flex;align-items:center;gap:4px;border-bottom:1px solid transparent;transition:.16s}
.link-red:hover{border-bottom-color:var(--brand)}
.btn{display:inline-flex;align-items:center;gap:7px;padding:11px 22px;border-radius:9px;
  font-size:14.5px;font-weight:600;cursor:pointer;border:1px solid transparent;transition:.18s}
.btn-primary{background:var(--accent);color:#fff;box-shadow:var(--shadow-sm)}
.btn-primary:hover{background:var(--accent-2);transform:translateY(-1px);box-shadow:var(--shadow)}
.btn-ghost{background:var(--card);color:var(--text);border-color:var(--line-2)}
.btn-ghost:hover{border-color:var(--brand);color:var(--brand)}
.btn-blue{background:var(--navy);color:#fff}
.btn-blue:hover{background:#3a4d85;transform:translateY(-1px)}
.pill{display:inline-flex;align-items:center;gap:7px;background:var(--accent-soft);
  border:1px solid color-mix(in srgb,var(--accent) 15%,transparent);color:var(--accent-text);
  border-radius:999px;padding:5px 14px;font-size:12.5px;font-weight:500;margin-bottom:18px}
.pill i{width:6px;height:6px;border-radius:50%;background:var(--accent);display:block;flex:0 0 auto}
.pill-plain{display:inline-block;background:var(--brand-soft);color:var(--brand);
  border-radius:6px;padding:4px 11px;font-size:12px;font-weight:600;margin-bottom:14px}
.crumb{font-size:12.5px;color:var(--text-3);margin-bottom:12px}
.crumb a{color:var(--brand)}
.crumb a:hover{border-bottom:1px solid var(--brand)}
h1.page{font-size:clamp(30px,5vw,46px);font-weight:800;letter-spacing:-.02em;
  line-height:1.24;margin:0 0 14px}
.lead{color:var(--text-2);font-size:15px;max-width:660px;margin:0 0 22px;line-height:1.8}
.sec{margin-bottom:54px}
.sec>h2{font-size:23px;font-weight:700;letter-spacing:-.01em;margin:0 0 6px}
.sec>.sec-sub{color:var(--text-2);font-size:14px;margin:0 0 20px}
.sec-head{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:14px;flex-wrap:wrap}
.sec-head h3{font-size:16px;font-weight:700;margin:0}
.sec-head .hint{color:var(--text-3);font-size:12.5px}
hr.rule{border:0;border-top:1px solid var(--line);margin:0 0 30px}

/* 顶部两栏 */
.split-top{display:grid;grid-template-columns:1.15fr 1fr;gap:40px;align-items:start;margin-bottom:34px}
.note-box{background:var(--bg-2);border-radius:var(--radius-sm);padding:16px 18px;
  font-size:13px;color:var(--text-2);line-height:1.75}
.note-box b{color:var(--text);display:block;margin-bottom:4px;font-weight:600}

/* 等级小卡（GESP总览） */
.lv-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.lv-card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:18px 18px 16px;box-shadow:var(--shadow-sm);transition:.2s;position:relative;
  overflow:hidden;display:block}
.lv-card::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:var(--bar,var(--brand))}
.lv-card:hover{transform:translateY(-4px);border-color:var(--line-2);box-shadow:var(--shadow-lg)}
.lv-card .no{font-size:13px;font-weight:800;color:var(--text-3);letter-spacing:.06em;font-variant-numeric:tabular-nums}
.lv-card .nm{font-size:21px;font-weight:800;margin:4px 0 8px}
.lv-card .ds{font-size:12.5px;color:var(--text-2);line-height:1.65;margin:0 0 14px;min-height:42px}
.lv-card .ft{border-top:1px solid var(--line);padding-top:10px;
  font-size:11.5px;color:var(--text-3);display:flex;align-items:center;gap:5px}
.lv-card .ft b{color:var(--brand);font-weight:700}

/* 首页专用：一行 8 个窄卡 */
.lv-mini{display:grid;grid-template-columns:repeat(8,1fr);gap:10px}
.lv-mini a{background:var(--card);border:1px solid var(--line);border-radius:var(--radius-sm);
  padding:14px 12px 13px;box-shadow:var(--shadow-sm);transition:.2s;position:relative;
  overflow:hidden;display:block}
.lv-mini a::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:var(--bar,var(--brand))}
.lv-mini a:hover{transform:translateY(-4px);border-color:var(--line-2);box-shadow:var(--shadow-lg)}
.lv-mini .no{font-size:13px;font-weight:700;color:var(--brand);letter-spacing:.04em}
.lv-mini .lv{font-size:18px;font-weight:800;line-height:1.2;margin:3px 0 2px;color:var(--text)}
.lv-mini .lbl{display:none}
.lv-mini .desc{font-size:11px;color:var(--text-3);margin:8px 0 0;line-height:1.55;
  border-top:1px solid var(--line);padding-top:7px;min-height:52px}

/* 知识大纲四列 */
.outline{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.outline-col{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:16px 18px;box-shadow:var(--shadow-sm)}
.outline-col h4{margin:0 0 10px;font-size:14.5px;font-weight:700;
  padding-bottom:9px;border-bottom:1px solid var(--line)}
.outline-col h4 em{font-style:normal;color:var(--text-3);font-weight:500;font-size:12.5px}
.outline-col ul{list-style:none;margin:0;padding:0}
.outline-col li{font-size:12.5px;color:var(--text-2);padding:3px 0;line-height:1.6;
  display:flex;gap:7px}
.outline-col li::before{content:"";width:4px;height:4px;border-radius:50%;
  background:var(--line-2);flex:0 0 auto;margin-top:9px}

/* 横栏 */
.rows{display:grid;gap:10px}
.row{display:flex;align-items:center;gap:14px;background:var(--card);border:1px solid var(--line);
  border-radius:var(--radius-sm);padding:14px 18px;box-shadow:var(--shadow-sm);transition:.2s}
.row:hover{border-color:var(--line-2);transform:translateX(3px)}
.row .tag{flex:0 0 auto;font-size:12px;font-weight:700;background:var(--brand-soft);
  color:var(--brand);border-radius:6px;padding:4px 10px}
.row .t{flex:0 0 auto;font-size:14.5px;font-weight:600}
.row .d{flex:1;font-size:13px;color:var(--text-3);min-width:0}
.row .go{flex:0 0 auto;color:var(--text-3);font-size:15px}

/* 步骤条（题解/卡点） */
.step{display:flex;align-items:center;gap:18px;background:var(--card);border:1px solid var(--line);
  border-radius:var(--radius-sm);padding:16px 20px;box-shadow:var(--shadow-sm);transition:.2s}
.step:hover{border-color:var(--line-2);transform:translateX(4px)}
.step .no{flex:0 0 auto;font-size:19px;font-weight:800;color:var(--brand);
  font-variant-numeric:tabular-nums;width:34px}
.step .tx{flex:1;min-width:0}
.step .tx b{display:block;font-size:15.5px;font-weight:700;margin-bottom:2px}
.step .tx span{font-size:13px;color:var(--text-3)}
.step .go{flex:0 0 auto;font-size:13px;color:var(--brand);font-weight:600;
  display:flex;align-items:center;gap:5px}

/* 空状态卡 */
.empty-wrap{display:flex;justify-content:center}
.empty-card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  box-shadow:var(--shadow-sm);padding:30px 34px;display:flex;gap:30px;align-items:center;
  width:100%;max-width:760px}
.empty-card .num{font-size:52px;font-weight:800;color:var(--brand);line-height:1;
  font-variant-numeric:tabular-nums}
.empty-card .num small{display:block;font-size:12px;font-weight:500;color:var(--text-3);margin-top:6px}
.empty-card .bd h3{margin:0 0 8px;font-size:21px;font-weight:700}
.empty-card .bd p{margin:0;font-size:13.5px;color:var(--text-2);line-height:1.8}

/* 模板分类卡 */
.cat-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}
.cat{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:16px 16px 14px;box-shadow:var(--shadow-sm);transition:.2s;display:block;position:relative}
.cat.featured{border-color:color-mix(in srgb,var(--brand) 35%,var(--line))}
.cat:hover{transform:translateY(-4px);box-shadow:var(--shadow-lg);border-color:var(--line-2)}
.cat .ico{width:32px;height:32px;border-radius:9px;background:var(--bg-2);
  display:grid;place-items:center;font-size:15px;margin-bottom:11px;color:var(--brand)}
.cat h4{margin:0 0 3px;font-size:15px;font-weight:700}
.cat .cnt{font-size:11.5px;color:var(--brand);font-weight:600;margin-bottom:8px}
.cat p{margin:0 0 11px;font-size:12px;color:var(--text-3);line-height:1.65;min-height:38px}
.cat .kw{display:flex;flex-direction:column;gap:4px}
.cat .kw span{font-size:11px;color:var(--text-3);background:var(--bg-2);
  border-radius:4px;padding:3px 8px;display:inline-block;width:fit-content}

/* 通用模板条目 */
.tpl-row{display:grid;grid-template-columns:1fr 1.25fr;gap:20px;align-items:start;
  padding:22px 0;border-bottom:1px solid var(--line)}
.tpl-row:last-child{border-bottom:0}
.tpl-row .lt .tag{display:inline-block;font-size:11px;font-weight:700;background:var(--brand-soft);
  color:var(--brand);border-radius:5px;padding:3px 9px;margin-bottom:10px}
.tpl-row .lt h4{margin:0 0 6px;font-size:18px;font-weight:700}
.tpl-row .lt p{margin:0 0 12px;font-size:13px;color:var(--text-2);line-height:1.75}
.tpl-row .lt .kw{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:14px}
.tpl-row .lt .kw span{font-size:11px;color:var(--text-3);background:var(--bg-2);
  border-radius:4px;padding:3px 9px}
.code{background:#0f172a;border-radius:var(--radius-sm);padding:16px 18px;overflow-x:auto;
  font-family:"SF Mono",Monaco,Menlo,Consolas,monospace;font-size:12.5px;line-height:1.8;
  color:#c9d1d9;border:1px solid var(--line);white-space:pre}
.code .k{color:#ff7b72}.code .t{color:#79c0ff}.code .f{color:#d2a8ff}.code .c{color:#8b949e}

/* 资源条目 */
.res-item{display:flex;align-items:center;gap:15px;background:var(--card);
  border:1px solid var(--line);border-radius:var(--radius-sm);padding:14px 18px;
  box-shadow:var(--shadow-sm);transition:.2s;margin-bottom:9px}
.res-item:hover{border-color:var(--line-2);transform:translateX(3px)}
.res-item .ic{width:34px;height:34px;border-radius:9px;flex:0 0 auto;display:grid;
  place-items:center;font-size:14px;font-weight:700;color:#fff}
.res-item .tx{flex:1;min-width:0}
.res-item .tx b{font-size:14.5px;font-weight:600;margin-right:8px}
.res-item .tx em{font-style:normal;font-size:11px;font-weight:600;color:var(--brand);
  background:var(--brand-soft);border-radius:4px;padding:2px 7px}
.res-item .tx p{margin:3px 0 0;font-size:12.5px;color:var(--text-3);line-height:1.6}
.res-item .go{color:var(--text-3);flex:0 0 auto}

/* 等级页 */
.layout{display:grid;grid-template-columns:250px 1fr;gap:38px;align-items:start}
.side{position:sticky;top:78px;align-self:start}
.side-box{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  box-shadow:var(--shadow-sm);overflow:hidden}
.side-h{padding:14px 18px;border-bottom:1px solid var(--line);font-size:14px;font-weight:700;
  display:flex;align-items:center;justify-content:space-between}
.side-h span{color:var(--text-3);font-size:11px}
.side-g{padding:12px 18px 6px;font-size:11.5px;font-weight:600;color:var(--text-3);letter-spacing:.04em}
.side-list{list-style:none;margin:0;padding:0 0 12px}
.side-list li a{display:flex;gap:9px;padding:6px 18px;font-size:13px;color:var(--text-2);
  transition:.14s;border-left:3px solid transparent;line-height:1.6}
.side-list li a:hover{background:var(--bg-2);color:var(--text);border-left-color:var(--brand)}
.side-list li a .n{color:var(--text-3);font-variant-numeric:tabular-nums;flex:0 0 auto;font-size:11.5px}

.intro{display:grid;grid-template-columns:1fr 1.2fr;gap:34px;align-items:start;
  padding:26px 0 30px;border-bottom:1px solid var(--line);margin-bottom:30px}
.intro h2{font-size:27px;font-weight:700;line-height:1.4;margin:0;letter-spacing:-.01em}
.intro p{color:var(--text-2);font-size:14px;margin:0;line-height:1.9}

.progress{display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr;gap:1px;
  background:var(--line);border:1px solid var(--line);border-radius:var(--radius);
  overflow:hidden;margin-bottom:38px}
.progress>div{background:var(--card);padding:17px 20px}
.progress .p-title{font-size:14px;font-weight:700;margin-bottom:4px}
.progress .p-desc{font-size:12px;color:var(--text-3);line-height:1.6}
.progress .p-num{font-size:22px;font-weight:800;color:var(--brand);font-variant-numeric:tabular-nums}
.progress .p-lbl{font-size:11.5px;color:var(--text-3);margin-top:2px}

.kp-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.kp{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:16px 18px;box-shadow:var(--shadow-sm);transition:.2s;display:flex;flex-direction:column}
.kp:hover{border-color:var(--line-2);transform:translateY(-3px);box-shadow:var(--shadow-lg)}
.kp-top{display:flex;align-items:center;gap:8px;margin-bottom:8px}
.kp-top .no{font-size:11.5px;font-weight:700;color:var(--text-3);letter-spacing:.06em}
.kp-top .badge{font-size:10.5px;font-weight:700;background:var(--brand-soft);
  color:var(--brand);border-radius:4px;padding:2px 7px}
.kp-top .state{margin-left:auto;font-size:10.5px;color:var(--text-3);
  background:var(--bg-2);border-radius:4px;padding:2px 7px}
.kp h4{margin:0 0 7px;font-size:15.5px;font-weight:700}
.kp p{margin:0 0 11px;font-size:12.5px;color:var(--text-2);line-height:1.7;flex:1}
.kp .tags{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:11px}
.kp .tags span{font-size:10.5px;color:var(--text-3);background:var(--bg-2);
  border-radius:4px;padding:2px 8px}

/* 知识点详细内容（可展开） */
.kp-detail{max-height:0;overflow:hidden;transition:max-height .3s ease}
.kp-detail.open{max-height:1200px}
.kp-detail-body{padding-top:4px;border-top:1px solid var(--line);margin-top:4px}
.kp-section{margin:14px 0 0}
.kp-section>b{display:block;font-size:13px;font-weight:700;margin-bottom:7px;color:var(--brand)}
.kp-pts,.kp-tips{margin:0;padding-left:18px;font-size:12.5px;color:var(--text-2);line-height:1.75}
.kp-pts li,.kp-tips li{margin-bottom:4px}
.kp-tips li{color:var(--accent-text)}
.kp-code{background:#0f172a;border:1px solid var(--line);border-radius:var(--radius-sm);
  padding:12px 14px;margin:12px 0 0;overflow-x:auto}
.kp-code pre{margin:0;font-family:"SF Mono",Monaco,Menlo,Consolas,monospace;
  font-size:12px;line-height:1.7;color:#c9d1d9;white-space:pre}
.kp-toggle{width:100%;margin-top:12px;padding:8px;border:1px solid var(--line-2);
  border-radius:8px;background:var(--bg-2);color:var(--brand);font-size:13px;
  font-weight:600;cursor:pointer;transition:.15s;font-family:inherit}
.kp-toggle:hover{border-color:var(--brand);color:var(--brand-2)}

/* 阶段卡 */
.stage-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.stage{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:20px;box-shadow:var(--shadow-sm);position:relative;overflow:hidden;transition:.2s}
.stage::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:var(--bar,var(--brand))}
.stage:hover{transform:translateY(-4px);box-shadow:var(--shadow-lg)}
.stage .no{font-size:13px;font-weight:800;color:var(--brand);letter-spacing:.08em}
.stage .tip{font-size:12px;color:var(--text-3);margin:8px 0 13px}
.stage h3{font-size:19px;font-weight:700;margin:0 0 8px}
.stage p{font-size:13px;color:var(--text-2);margin:0 0 14px;line-height:1.75}
.stage .kw{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:15px}
.stage .kw span{font-size:11px;color:var(--text-3);background:var(--bg-2);
  border-radius:4px;padding:3px 9px}
.stage .foot{border-top:1px solid var(--line);padding-top:12px}

/* 搜索 */
#results{max-width:620px;margin:10px auto 0;background:var(--card);border:1px solid var(--line-2);
  border-radius:var(--radius-sm);box-shadow:var(--shadow-lg);overflow:hidden;display:none;text-align:left}
#results.on{display:block}
#results a{display:block;padding:11px 18px;font-size:14px;border-bottom:1px solid var(--line);transition:.14s}
#results a:last-child{border-bottom:0}
#results a:hover{background:var(--bg-2);padding-left:24px}
#results a span{color:var(--text-3);font-size:12.5px}
#results .empty{padding:16px 18px;color:var(--text-3);font-size:13.5px}

/* 响应式 */
@media (max-width:1060px){
  .lv-grid{grid-template-columns:repeat(2,1fr)}
  .outline{grid-template-columns:repeat(2,1fr)}
  .cat-grid{grid-template-columns:repeat(3,1fr)}
  .fwrap{grid-template-columns:1fr 1fr}
}
@media (max-width:900px){
  .layout{grid-template-columns:1fr}
  .side{position:static}
  .kp-grid{grid-template-columns:repeat(2,1fr)}
  .stage-grid{grid-template-columns:1fr}
  .split-top{grid-template-columns:1fr;gap:20px}
  .intro{grid-template-columns:1fr;gap:14px}
  .tpl-row{grid-template-columns:1fr}
}
@media (max-width:860px){
  .bar{flex-wrap:wrap;gap:12px}
  nav{order:3;width:100%;margin:0;overflow-x:auto;padding-bottom:4px}
  .bar-right{margin-left:auto}
  .mini-search{display:none}
}
@media (max-width:640px){
  .lv-grid{grid-template-columns:1fr}
  .outline{grid-template-columns:1fr}
  .cat-grid{grid-template-columns:1fr 1fr}
  .kp-grid{grid-template-columns:1fr}
  .progress{grid-template-columns:1fr 1fr}
  .fwrap{grid-template-columns:1fr}
  .empty-card{flex-direction:column;text-align:center;gap:18px}
}
#toTop{position:fixed;right:22px;bottom:22px;z-index:70;width:42px;height:42px;border-radius:50%;
  cursor:pointer;background:var(--card);color:var(--text-2);font-size:16px;
  border:1px solid var(--line-2);box-shadow:var(--shadow);
  display:grid;place-items:center;opacity:0;pointer-events:none;transition:.25s}
#toTop.on{opacity:1;pointer-events:auto}
#toTop:hover{color:var(--brand);border-color:var(--brand)}
</style>"""


# ============================== 骨架 ==============================
def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#f8fafc">
<script>(function(){{try{{if(localStorage.getItem("theme")==="dark")document.documentElement.setAttribute("data-theme","dark");}}catch(e){{}}}})();</script>
{CSS}
</head>
<body>"""


def make_header(prefix="", active=""):
    links = []
    for label, href, key in NAV:
        cls = ' class="active"' if key == active else ""
        links.append(f'<a href="{prefix}{href}"{cls}>{label}</a>')
    return f"""
<header>
  <div class="bar">
    <a class="brand" href="{prefix}index.html">
      <div class="logo">OI</div>
      <div class="brand-txt"><b>{SITE_NAME}</b><small>{SITE_SUB}</small></div>
    </a>
    <nav>
      {"".join(links)}
    </nav>
    <div class="bar-right">
      <div class="mini-search">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
          <circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
        <span>知识点 / 题目 / 教程</span>
      </div>
      <button class="theme-btn" id="themeBtn" title="切换主题">◐</button>
    </div>
  </div>
</header>"""


def make_footer(prefix=""):
    fcols = [("学习路线", [("首页","index.html"),("GESP 1–8 级","gesp.html"),("CSP-J/S","csp.html")]),
             ("工具",     [("程序模板","templates.html"),("题解","solutions.html")]),
             ("资源",     [("OJ 与资源","resources.html"),("洛谷","https://www.luogu.com.cn/")])]
    cols = ""
    for title, items in fcols:
        lis = "".join(f'<a href="{prefix}{h}">{l}</a>' for l, h in items)
        cols += f'<div class="fcol"><h5>{title}</h5>{lis}</div>'
    return f"""
<footer>
  <div class="fwrap">
    <div class="fbrand">
      <b>{SITE_NAME}</b>
      <p>帮助学生按等级学习信息学、查找知识、解决做题卡点并回到 OJ 独立完成。</p>
    </div>
    {cols}
  </div>
  <div class="fbottom">
    本站为个人学习资料整理，知识点依据 GESP / CSP-J/S 官方大纲组织，内容自行撰写。<br>
    部分外链指向第三方网站，其内容与规则以主办方发布为准。
  </div>
</footer>

<button id="toTop" title="回到顶部">↑</button>
<script>
(function(){{
  var t=document.getElementById("themeBtn");
  if(t)t.addEventListener("click",function(){{
    var r=document.documentElement,d=r.getAttribute("data-theme")==="dark";
    if(d)r.removeAttribute("data-theme");else r.setAttribute("data-theme","dark");
    try{{localStorage.setItem("theme",d?"light":"dark");}}catch(e){{}}
  }});
  var b=document.getElementById("toTop");
  window.addEventListener("scroll",function(){{b.className=window.scrollY>500?"on":""}},{{passive:true}});
  b.addEventListener("click",function(){{window.scrollTo({{top:0,behavior:"smooth"}})}});
}})();
</script>
</body>
</html>"""


def page(title, desc, body, active, prefix=""):
    return head(title, desc) + make_header(prefix, active) + "\n" + body + "\n" + make_footer(prefix)


def write(rel, content):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, "w", encoding="utf-8").write(content)


# ============================== 页面 ==============================
def build_home():
    lv_cards = ""
    for i in range(1, 9):
        n = len(LEVELS[i][3])
        lv_cards += f"""
        <a href="gesp/level{i}.html" style="--bar:{BAR_COLORS[i-1]}">
          <div class="no">{i:02d}</div>
          <div class="lv">{CN_NUM[i-1]}级</div>
          <div class="lbl">{n} 个知识点</div>
          <div class="desc">{E(LEVELS[i][2][:30])}</div>
        </a>"""

    body = f"""
<main>
  <section style="padding:64px 20px 36px;text-align:center;
    background:radial-gradient(ellipse 80% 60% at 50% -10%,rgba(99,102,241,.06) 0%,transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 50%,rgba(6,182,212,.04) 0%,transparent 50%)">
    <div style="max-width:720px;margin:0 auto">
      <div class="pill"><i></i>{SITE_NAME} · C++ 学习词典</div>
      <h1 class="page" style="text-align:center">今天想解决什么？</h1>
      <p class="lead" style="margin:0 auto 26px;text-align:center">继续当前学习，或者先把一道题卡住的地方解决掉。</p>
      <div style="display:flex;align-items:center;gap:10px;background:var(--card);
        border:1px solid var(--line-2);border-radius:12px;padding:13px 16px;box-shadow:var(--shadow);
        max-width:620px;margin:0 auto 20px">
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"
          style="color:var(--text-3);flex:0 0 auto"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
        <b style="font-size:14.5px;flex:0 0 auto">搜索全站</b>
        <input id="search" type="search" placeholder="搜索知识点、题目、模板……" autocomplete="off"
          style="flex:1;border:0;outline:0;background:transparent;font-size:14.5px;color:var(--text);
          font-family:inherit;min-width:0">
        <span style="font-size:11.5px;color:var(--text-3);background:var(--bg-2);border:1px solid var(--line);
          border-radius:5px;padding:2px 7px;flex:0 0 auto">ctrl K</span>
      </div>
      <div style="display:flex;gap:11px;justify-content:center;flex-wrap:wrap">
        <a class="btn btn-primary" href="gesp.html">开始学习 →</a>
        <a class="btn btn-ghost" href="#stuck">解决做题卡点</a>
      </div>
      <p style="color:var(--text-3);font-size:13px;margin:15px 0 0">从 GESP 学习路线选择当前级别</p>
    </div>
  </section>

  <div id="results"></div>

  <div class="wrap">
    <div class="panel" style="display:flex;align-items:center;gap:20px;padding:20px 24px;
      margin-bottom:52px;flex-wrap:wrap">
      <div><b style="display:block;font-size:15px;font-weight:700">上次访问</b>
        <span style="font-size:12.5px;color:var(--text-3)">只记录在这台设备上。</span></div>
      <div id="lastVisitText" style="flex:1;color:var(--text-2);font-size:14px;min-width:200px">
        还没有最近访问。先选择一条路线，之后可以从这里返回。</div>
      <div style="display:flex;gap:18px;flex-wrap:wrap">
        <a class="link-red" href="gesp.html">从 GESP 开始 →</a>
        <a class="link-red" href="csp.html">查看 CSP 路线</a>
      </div>
    </div>

    <section class="sec">
      <h2>选择学习路线</h2>
      <p class="sec-sub">GESP 按当前等级学习；CSP 按考试阶段准备。</p>
      <div class="sec-head"><h3>GESP 一级至八级</h3>
        <span class="hint">按等级查询，不设访问门槛</span></div>
      <div class="lv-mini">{lv_cards}</div>
    </section>

    <section class="sec">
      <div class="sec-head"><h3>CSP-J/S</h3>
        <a class="link-red" href="csp.html">查看 CSP 学习路线 →</a></div>
      <div class="rows">
        {"".join(f'''<a class="row" href="csp.html"><span class="tag">{c[1].split()[0].replace("CSP-","")}</span>
        <span class="t">{E(c[1])}</span><span class="d">{E(c[2])}</span><span class="go">→</span></a>''' for c in CSP)}
      </div>
    </section>

    <section class="sec" id="stuck">
      <h2>这道题卡在哪里？</h2>
      <p class="sec-sub">先判断卡点，再进入对应内容。</p>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
        <div class="rows">
          {"".join(f'''<a class="step" href="{h}"><span class="no">{n}</span>
          <span class="tx"><b>{E(t)}</b><span>{E(d)}</span></span>
          <span class="go">{E(g)} →</span></a>''' for n,t,d,g,h in SOLUTION_STEPS)}
        </div>
        <div>
          <div class="code"><span class="c">// 二分答案：先确定单调性，再缩小范围</span>
<span class="k">int</span> <span class="f">check</span>(<span class="k">int</span> x) {{ <span class="k">return</span> x &gt;= target; }}

<span class="k">int</span> l = <span class="t">0</span>, r = n, ans = -<span class="t">1</span>;
<span class="k">while</span> (l &lt;= r) {{
    <span class="k">int</span> mid = l + (r - l) / <span class="t">2</span>;
    <span class="k">if</span> (<span class="f">check</span>(mid)) {{ ans = mid; r = mid - <span class="t">1</span>; }}
    <span class="k">else</span> l = mid + <span class="t">1</span>;
}}</div>
        </div>
      </div>
    </section>

    <section class="sec">
      <h2>常用工具</h2>
      <p class="sec-sub">知道自己需要什么时，直接进入对应工具。</p>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
        <div>
          <a class="step" href="templates.html"><span class="no">01</span>
            <span class="tx"><b>程序模板</b><span>已经有思路、需要可直接复制的框架时使用</span></span>
            <span class="go">打开程序模板 →</span></a>
          <div style="height:10px"></div>
          <a class="step" href="solutions.html"><span class="no">02</span>
            <span class="tx"><b>题解库</b><span>从选题读题、突破口到写代码过程使用</span></span>
            <span class="go">打开题解 →</span></a>
        </div>
        <div>
          <div class="code"><span class="c">// 快读快写（大数据量必备）</span>
<span class="k">inline int</span> <span class="f">read</span>() {{
    <span class="k">int</span> x = <span class="t">0</span>, f = <span class="t">1</span>; <span class="k">char</span> c = <span class="f">getchar</span>();
    <span class="k">while</span> (c &lt; <span class="t">'0'</span> || c &gt; <span class="t">'9'</span>) {{
        <span class="k">if</span> (c == <span class="t">'-'</span>) f = -<span class="t">1</span>; c = <span class="f">getchar</span>();
    }}
    <span class="k">while</span> (c &gt;= <span class="t">'0'</span> &amp;&amp; c &lt;= <span class="t">'9'</span>) {{
        x = x * <span class="t">10</span> + c - <span class="t">'0'</span>; c = <span class="f">getchar</span>();
    }}
    <span class="k">return</span> x * f;
}}</div>
        </div>
      </div>
    </section>

    <section class="sec">
      <h2>OJ 与学习资源</h2>
      <p class="sec-sub">返回题库练习，或查看权威资料。</p>
      <div class="rows">
        <a class="row" href="https://www.luogu.com.cn/" target="_blank" rel="noopener">
          <span class="tag">OJ</span><span class="t">洛谷</span>
          <span class="d">国内主流题库，题目与题解丰富</span><span class="go">↗</span></a>
        <a class="row" href="https://oi-wiki.org/" target="_blank" rel="noopener">
          <span class="tag">百科</span><span class="t">OI Wiki</span>
          <span class="d">算法竞赛知识百科，查算法与证明</span><span class="go">↗</span></a>
        <a class="row" href="https://www.noi.cn/" target="_blank" rel="noopener">
          <span class="tag">官方</span><span class="t">NOI 官网</span>
          <span class="d">赛事通知、大纲与政策</span><span class="go">↗</span></a>
        <a class="row" href="https://codeforces.com/" target="_blank" rel="noopener">
          <span class="tag">比赛</span><span class="t">Codeforces</span>
          <span class="d">国际比赛与高质量题目</span><span class="go">↗</span></a>
      </div>
    </section>
  </div>
</main>

<script>
(function(){{
  "use strict";
  var INDEX=[
    {{t:"GESP 分级总览",d:"八级学习路线",h:"gesp.html"}},
    {{t:"CSP-J/S",d:"初赛、复赛与进阶",h:"csp.html"}},
    {{t:"程序模板",d:"可修改的 C++ 代码框架",h:"templates.html"}},
    {{t:"题解",d:"读题、思路与代码映射",h:"solutions.html"}},
    {{t:"OJ 与资源",d:"题库与学习资料",h:"resources.html"}}
  ];
  var KWS=["计算机基础","集成开发环境","程序基本结构","输入输出","基本数据类型","基本运算","顺序结构","分支结构","循环结构","存储与网络","流程图","类型转换","进制转换","位运算","数组","字符串","枚举","模拟","函数","指针","引用","结构体","二维数组","排序","递推","复杂度","数论","素数筛","高精度","链表","二分","贪心","分治","递归","树","遍历","哈夫曼","格雷码","回溯","深度优先","广度优先","动态规划","背包","图论","最短路","最小生成树","哈希表","计数原理","排列组合","倍增"];
  for(var i=1;i<=8;i++) INDEX.push({{t:"GESP "+i+" 级",d:"第 "+i+" 级知识点",h:"gesp/level"+i+".html"}});
  KWS.forEach(function(k){{ INDEX.push({{t:k,d:"知识点查询",h:"gesp.html"}}); }});

  var input=document.getElementById("search"),box=document.getElementById("results");
  function render(kw){{
    var q=kw.trim().toLowerCase();
    if(!q){{box.className="";box.innerHTML="";return;}}
    var hit=INDEX.filter(function(it){{return (it.t+" "+it.d).toLowerCase().indexOf(q)!==-1;}}).slice(0,8);
    box.innerHTML=hit.length?hit.map(function(it){{
      return '<a href="'+it.h+'"><b>'+it.t+'</b> <span>'+it.d+'</span></a>';
    }}).join(""):'<div class="empty">没有找到「'+kw.replace(/[<>&]/g,"")+'」，换个关键词试试</div>';
    box.className="on";
  }}
  input.addEventListener("input",function(){{render(this.value);}});
  input.addEventListener("keydown",function(e){{
    if(e.key==="Enter"){{var f=box.querySelector("a");if(f)f.click();}}
    if(e.key==="Escape"){{box.className="";input.blur();}}
  }});
  document.addEventListener("click",function(e){{
    if(!e.target.closest("#results")&&!e.target.closest("input"))box.className="";
  }});
  document.addEventListener("keydown",function(e){{
    if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==="k"){{
      e.preventDefault();window.scrollTo({{top:0,behavior:"smooth"}});
      setTimeout(function(){{input.focus();}},200);
    }}
  }});
  try{{var lv=localStorage.getItem("lastLevel");
    if(lv)document.getElementById("lastVisitText").innerHTML="上次学到 <b>GESP "+lv+" 级</b>，可以从这里继续。";
  }}catch(e){{}}
}})();
</script>
"""
    return page(f"{SITE_NAME} | GESP · CSP-J/S",
                "面向 GESP、CSP-J/S 学生的学习工作台，按等级整理学习路线、程序模板、题解与 OJ 资源。",
                body, "home")


def build_gesp():
    cards = ""
    for i in range(1, 9):
        n = len(LEVELS[i][3])
        cards += f"""
      <a class="lv-card" href="gesp/level{i}.html" style="--bar:{BAR_COLORS[i-1]}">
        <div class="no">{i:02d}</div>
        <div class="nm">{CN_NUM[i-1]}级</div>
        <div class="ds">{E(LEVELS[i][2])}</div>
        <div class="ft"><b>{n}</b> 个知识点 · 可直接进入</div>
      </a>"""

    cols = ""
    for i in range(1, 9):
        kps = LEVELS[i][3]
        lis = "".join(f"<li>{E(k[0])}</li>" for k in kps)
        cols += f"""
      <div class="outline-col">
        <h4>{CN_NUM[i-1]}级 · {len(kps)} 个知识点</h4>
        <ul>{lis}</ul>
      </div>"""

    total = sum(len(LEVELS[i][3]) for i in range(1, 9))

    body = f"""
<main class="wrap" style="padding-top:48px">
  <div class="crumb"><a href="index.html">{SITE_NAME}</a> · GESP · 编程入门知识字典</div>

  <div class="split-top">
    <div>
      <h1 class="page">选择你正在学习的<br>GESP 级别</h1>
      <p class="lead" style="margin-bottom:0">从一级到八级，直接进入对应知识目录。每个知识点都可以单独查看，不设置解锁门槛。</p>
    </div>
    <div class="note-box">
      <b>不知道从哪一级开始？</b>
      先查看一级大纲，随便用全部章节熟悉通用的基础，再确定当前等级。
      <div style="margin-top:10px"><a class="link-red" href="gesp/level1.html">从一级开始 →</a></div>
    </div>
  </div>
  <hr class="rule">

  <section class="sec">
    <div class="sec-head"><h2 style="margin:0">一级至八级</h2>
      <span class="hint">按当学习阶段自由查看</span></div>
    <div class="lv-grid">{cards}</div>
  </section>

  <section class="sec">
    <div class="sec-head"><h3 style="font-size:23px">GESP 知识大纲</h3>
      <span class="hint">{total} 个真实知识点 · 全部可直接访问</span></div>
    <div class="outline">{cols}</div>
  </section>
</main>
"""
    return page(f"GESP 分级 | {SITE_NAME}", "GESP 一级至八级知识点总览与大纲。", body, "gesp")


def build_level(n):
    kicker = LEVELS[n][0]
    intro_text = LEVELS[n][1]
    kps = LEVELS[n][3]
    bar = BAR_COLORS[n-1]
    total = len(kps)

    side = "".join(
        f'<li><a href="#kp{i}"><span class="n">{i:02d}</span><span>{E(k[0])}</span></a></li>'
        for i, k in enumerate(kps, 1))

    grid = ""
    for i, (t, d, tags) in enumerate(kps, 1):
        tg = "".join(f"<span>{E(x)}</span>" for x in tags)
        det = KP_DETAILS.get(t, {"points": [], "code": None, "tips": []})
        pts = "".join(f"<li>{E(p)}</li>" for p in det["points"])
        tips = "".join(f"<li>{E(tp)}</li>" for tp in det["tips"])
        code_block = ""
        if det.get("code"):
            code_block = (f'<div class="kp-code"><pre>{E(det["code"])}</pre></div>')
        grid += f"""
      <div class="kp" id="kp{i}">
        <div class="kp-top"><span class="no">{i:02d}</span>
          <span class="badge">官方核心</span><span class="state">未复习</span></div>
        <h4>{E(t)}</h4>
        <p>{E(d)}</p>
        <div class="tags">{tg}</div>
        <div class="kp-detail">
          <div class="kp-detail-body">
            <div class="kp-section"><b>核心要点</b><ul class="kp-pts">{pts}</ul></div>
            {code_block}
            <div class="kp-section"><b>注意事项</b><ul class="kp-tips">{tips}</ul></div>
          </div>
        </div>
        <button class="kp-toggle" type="button">查看详细内容 ↓</button>
      </div>"""

    others = ""
    for i in range(1, 9):
        if i == n: continue
        others += f"""
        <a class="row" href="level{i}.html" style="--bar:{BAR_COLORS[i-1]}">
          <span class="tag">{CN_NUM[i-1]}级</span>
          <span class="t">GESP {i} 级</span>
          <span class="d">{E(LEVELS[i][2])}</span>
          <span class="go">→</span></a>"""

    body = f"""
<main class="wrap" style="padding-top:40px">
<div class="layout">
  <aside class="side">
    <div class="side-box">
      <div class="side-h">{CN_NUM[n-1]}级总览 <span>{total}</span></div>
      <div class="side-g">{n} 级知识点</div>
      <ul class="side-list">{side}</ul>
    </div>
  </aside>

  <div>
    <div class="crumb"><a href="../index.html">{SITE_NAME}</a> · GESP {n} 级 · {E(kicker)}</div>
    <h1 class="page">GESP {n} 级</h1>

    <div class="intro">
      <h2>遇到问题，<br>直接查对应知识点</h2>
      <p>{E(intro_text)}</p>
    </div>

    <div class="progress">
      <div><div class="p-title">本机复习记录</div>
        <div class="p-desc">只记录当前设备上的复习与自测情况，不代表考试成绩。</div></div>
      <div><div class="p-num" id="p1">0/{total}</div><div class="p-lbl">已复习知识点</div></div>
      <div><div class="p-num" id="p2">0/{total}</div><div class="p-lbl">已完成自测</div></div>
      <div><div class="p-num">暂无记录</div><div class="p-lbl">自测正确率</div></div>
    </div>

    <div class="sec-head"><h3>{n} 级知识点</h3>
      <span class="hint">共 {total} 个知识点，按官方大纲顺序排列</span></div>
    <div class="kp-grid">{grid}</div>

    <section class="sec" style="margin-top:46px">
      <h2>其他等级</h2>
      <p class="sec-sub">切换到其它 GESP 等级继续学习。</p>
      <div class="rows">{others}</div>
    </section>
  </div>
</div>
</main>

<script>
(function(){{
  var n="{n}", total={total};
  try{{
    localStorage.setItem("lastLevel", n);
    var seen=JSON.parse(localStorage.getItem("reviewed")||"{{}}");
    var c=(seen[n]||[]).length;
    document.getElementById("p1").textContent=c+"/"+total;
  }}catch(e){{}}
  var kps=[].slice.call(document.querySelectorAll(".kp"));
  kps.forEach(function(el){{
    el.addEventListener("click",function(e){{
      if(e.target.closest(".kp-toggle")||e.target.closest(".kp-detail"))return;
      var st=el.querySelector(".state");
      st.textContent="已复习"; st.style.color="var(--brand)";
      try{{
        var seen=JSON.parse(localStorage.getItem("reviewed")||"{{}}");
        var arr=seen[n]||[];
        if(arr.indexOf(el.id)===-1) arr.push(el.id);
        seen[n]=arr; localStorage.setItem("reviewed",JSON.stringify(seen));
        document.getElementById("p1").textContent=arr.length+"/"+total;
      }}catch(e){{}}
    }});
  }});
  document.querySelectorAll(".kp-toggle").forEach(function(btn){{
    btn.addEventListener("click",function(){{
      var detail=this.previousElementSibling;
      var open=detail.classList.toggle("open");
      this.textContent=open?"收起内容 ↑":"查看详细内容 ↓";
    }});
  }});
}})();
</script>
"""
    return page(f"GESP {n} 级 | {SITE_NAME}",
                f"GESP {n} 级知识点整理：{intro_text}", body, "gesp", prefix="../")


def build_csp():
    stages = ""
    for no, name, desc, tip, color, kws in CSP:
        kw = "".join(f"<span>{E(x)}</span>" for x in kws)
        stages += f"""
      <div class="stage" style="--bar:{color}">
        <div class="no">{no}</div>
        <div class="tip">{E(tip)}</div>
        <h3>{E(name)}</h3>
        <p>{E(desc)}</p>
        <div class="kw">{kw}</div>
        <div class="foot"><span class="link-red">查看阶段 →</span></div>
      </div>"""

    rows = ""
    for no, name, desc, tip, color, kws in CSP:
        rows += f"""
      <a class="row" href="#stages"><span class="tag">{name.split()[0].replace('CSP-','')}</span>
        <span class="t">{E(name)}</span><span class="d">{E(desc)}</span>
        <span class="go">→</span></a>"""

    body = f"""
<main class="wrap" style="padding-top:48px">
  <div class="crumb"><a href="index.html">{SITE_NAME}</a> · CSP-J/S · 按考试阶段查询</div>

  <div class="split-top">
    <div>
      <h1 class="page">选择你正在准<br>备的 CSP 阶段</h1>
      <p class="lead" style="margin-bottom:0">初赛、复赛和进阶训练关注的内容不同。先选择你眼下正在准备的阶段，再直接进入对应说明。</p>
      <div style="margin-top:20px"><a class="btn btn-primary" href="#stages">查看三个备考阶段 →</a></div>
    </div>
    <div class="note-box">
      <b>适合现在？</b>
      适合已经开始准备 CSP-J/S、想按考试阶段查看学习范围的学生。
    </div>
  </div>
  <hr class="rule">

  <section class="sec" id="stages">
    <div class="sec-head"><h3 style="font-size:23px">三个备考阶段</h3>
      <span class="hint">按目标直接进入</span></div>
    <p class="sec-sub">阶段不是门槛，选择你眼下正在准备的考试，直接查看对应范围。</p>
    <div class="stage-grid">{stages}</div>
  </section>

  <section class="sec">
    <h2>三个阶段怎么选</h2>
    <p class="sec-sub">只比较现在最需要的信息，不替你判断学习状态。</p>
    <div class="rows">{rows}</div>
  </section>
</main>
"""
    return page(f"CSP-J/S | {SITE_NAME}", "CSP-J 初赛、CSP-J 复赛与 CSP-S 进阶的学习范围。", body, "csp")


def build_templates():
    total = sum(c[2] for c in TEMPLATE_CATS)
    cats = ""
    for ico, name, cnt, desc, kws, feat in TEMPLATE_CATS:
        kw = "".join(f"<span>{E(k)}</span>" for k in kws)
        cls = "cat featured" if feat else "cat"
        cats += f"""
      <a class="{cls}" href="#common">
        <div class="ico">{ico}</div>
        <h4>{E(name)}</h4>
        <div class="cnt">{cnt} 个模板</div>
        <p>{E(desc)}</p>
        <div class="kw">{kw}</div>
      </a>"""

    commons = ""
    for name, desc, kws, code in COMMON_TEMPLATES:
        kw = "".join(f"<span>{E(k)}</span>" for k in kws)
        commons += f"""
      <div class="tpl-row">
        <div class="lt">
          <span class="tag">编辑站点</span>
          <h4>{E(name)}</h4>
          <p>{E(desc)}</p>
          <div class="kw">{kw}</div>
          <a class="link-red" href="#common">查看并修改模板 →</a>
        </div>
        <div class="code">{E(code)}</div>
      </div>"""

    body = f"""
<main class="wrap" style="padding-top:48px">
  <div class="crumb"><a href="index.html">{SITE_NAME}</a> · 程序模板 · C++ 代码框架</div>

  <span class="pill-plain">适合现在 · 已有解题思路</span>
  <h1 class="page">查找可以直接<br>修改的程序模板</h1>
  <p class="lead">知道要用什么算法时，先搜索具体模板；还不确定名称时，再按分类进入。</p>

  <div style="display:flex;gap:10px;max-width:620px;margin-bottom:8px">
    <input type="search" placeholder="输入题型、算法名称或描述，例如「累加求和」「二分查找」"
      style="flex:1;padding:13px 16px;font-size:14.5px;background:var(--card);color:var(--text);
      border:1px solid var(--line-2);border-radius:11px;outline:none;font-family:inherit">
    <button class="btn btn-primary" style="padding:13px 26px">搜索</button>
  </div>
  <p style="font-size:12.5px;color:var(--text-3);margin:0 0 40px">搜索结果会直接进入可以查看和修改的模板页面。</p>

  <section class="sec" id="cats">
    <div class="sec-head"><h2 style="margin:0">从分类浏览</h2>
      <span class="hint">{total} 个真实模板</span></div>
    <p class="sec-sub">不确定模板名称时，从最接近的分类进入。</p>
    <div class="cat-grid">{cats}</div>
  </section>

  <section class="sec" id="common">
    <h2>常用模板</h2>
    <p class="sec-sub">编辑精选的常用框架，可以直接进入页面查看修改位置和完整说明。</p>
    {commons}
  </section>
</main>
"""
    return page(f"程序模板 | {SITE_NAME}", "竞赛常用 C++ 代码模板与框架，按分类浏览。", body, "tpl")


def build_solutions():
    steps = ""
    for no, title, desc, go, href in SOLUTION_STEPS:
        steps += f"""
      <a class="step" href="{href}"><span class="no">{no}</span>
        <span class="tx"><b>{E(title)}</b><span>{E(desc)}</span></span>
        <span class="go">{E(go)} →</span></a>"""

    body = f"""
<main class="wrap" style="padding-top:48px">
  <div class="crumb"><a href="index.html">{SITE_NAME}</a> · 题解 · 从卡点开始</div>

  <div class="split-top">
    <div>
      <h1 class="page">先判断你卡<br>在哪一步</h1>
    </div>
    <div class="note-box" style="background:transparent;padding:0">
      做题卡住时，先别急着找一份完整答案。判断自己是没看懂知识、不会把思路写成代码，还是需要继续练习，再进入对应入口。
      <div style="margin-top:12px">
        <span style="font-size:12.5px;color:var(--text-3)">这里不会把空目录包装成题库；当前题解收录情况实时反映本站已发布的真实内容。</span>
      </div>
      <div style="margin-top:12px"><a class="link-red" href="#steps">从卡点选择下一步</a></div>
    </div>
  </div>
  <hr class="rule">

  <section class="sec" id="steps">
    <div class="sec-head"><h3 style="font-size:23px">下一步不是同一个答案</h3>
      <span class="hint">按现在的卡点选择</span></div>
    <div class="rows">{steps}</div>
  </section>

  <section class="sec">
    <div class="empty-wrap">
    <div class="empty-card">
      <div class="num">00<small>篇已发布题解</small></div>
      <div class="bd">
        <h3>目前还没有发布具体题解</h3>
        <p>GESP 一级至四级往年真题解析会在知识目录构建完成后另建阶段。现在可以先按上面的卡点去查知识、找模板或继续练习。</p>
      </div>
    </div>
    </div>
  </section>

  <section class="sec">
    <h2>读题四步</h2>
    <p class="sec-sub">遇到读不懂的题，按这个顺序过一遍。</p>
    <div class="rows">
      <div class="row"><span class="tag">01</span><span class="t">找输入输出</span>
        <span class="d">先明确要读什么、要输出什么格式</span></div>
      <div class="row"><span class="tag">02</span><span class="t">看数据范围</span>
        <span class="d">数据范围决定算法复杂度上限，这一步最容易被跳过</span></div>
      <div class="row"><span class="tag">03</span><span class="t">手算样例</span>
        <span class="d">用小样例手动推一遍，确认自己理解了规则</span></div>
      <div class="row"><span class="tag">04</span><span class="t">找边界情况</span>
        <span class="d">最小值、最大值、空数据、重复元素往往是失分点</span></div>
    </div>
  </section>
</main>
"""
    return page(f"题解 | {SITE_NAME}", "信息学竞赛题解与解题思路整理。", body, "sol")


def build_resources():
    groups = ""
    for gtitle, gdesc, _, items in RESOURCE_GROUPS:
        lis = ""
        for initial, name, badge, desc, color in items:
            lis += f"""
        <a class="res-item" href="#" >
          <div class="ic" style="background:{color}">{E(initial)}</div>
          <div class="tx"><b>{E(name)}</b><em>{E(badge)}</em><p>{E(desc)}</p></div>
          <div class="go">↗</div>
        </a>"""
        groups += f"""
      <section class="sec">
        <h2>{E(gtitle)}</h2>
        <p class="sec-sub">{E(gdesc)}</p>
        {lis}
      </section>"""

    body = f"""
<main class="wrap" style="padding-top:48px">
  <div class="crumb"><a href="index.html">{SITE_NAME}</a> · OJ 与资源</div>

  <div class="split-top">
    <div>
      <h1 class="page">先说你 现在要做什么</h1>
      <p class="lead">资源按四种常见任务整理。每组只有一个首选入口，其他网站放在后面，避免在长串链接里反复比较。</p>
      <div style="margin-top:20px"><a class="btn btn-blue" href="#today">准备刷题 →</a></div>
    </div>
    <div class="note-box">
      <b>适合现在？</b>
      适合准备刷题、查考试通知、学算法，或配置 C++ 编程环境。
    </div>
  </div>
  <hr class="rule">

  {groups}
</main>
"""
    return page(f"OJ 与资源 | {SITE_NAME}", "常用在线评测平台与学习资料。", body, "res")


# ============================== 主流程 ==============================
def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    files = [
        ("index.html",     build_home()),
        ("gesp.html",      build_gesp()),
        ("csp.html",       build_csp()),
        ("templates.html", build_templates()),
        ("solutions.html", build_solutions()),
        ("resources.html", build_resources()),
    ]
    for n in range(1, 9):
        files.append((f"gesp/level{n}.html", build_level(n)))

    for rel, content in files:
        write(rel, content)

    io.open(os.path.join(OUT, ".nojekyll"), "w").write("")

    total_kp = sum(len(LEVELS[i][3]) for i in range(1, 9))
    print(f"✅ 生成 {len(files)} 个页面")
    print(f"✅ 知识点总数: {total_kp}")
    for i in range(1, 9):
        print(f"     GESP {i} 级: {len(LEVELS[i][3])} 个")
    print(f"✅ 模板分类: {len(TEMPLATE_CATS)} 类 / 共 {sum(c[2] for c in TEMPLATE_CATS)} 个模板")


if __name__ == "__main__":
    main()
