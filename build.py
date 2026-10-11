"""Build the dependency-free Chinese reading guide. Run: python build.py"""
from pathlib import Path
import json
from html import escape as esc

ROOT = Path(__file__).resolve().parent
pages = json.loads((ROOT / 'content.json').read_text())
PDF = 'https://teorth.github.io/tao-web/slides/math-2-0-caltech-2026.pdf'
chapters = [
    ('01', '证明的供给变了', '01—06', '从证明稀缺到证明丰富'),
    ('02', '能力与评价的边界', '07—12', '看见突破，也看见没有报道的部分'),
    ('03', '把问题族变成地图', '13—15', '大规模实验数学的两个案例'),
    ('04', '理解为何不可绕过', '16—21', '灯塔、研究生态与目标失配'),
    ('05', 'Math 2.0 怎么做', '22—27', '把愿景变成具体研究工作'),
]
sources = {
    'blog': ('作者博客 · Math 2.0', 'https://terrytao.wordpress.com/2026/10/10/math-2-0/', '核对演讲日期、题目变更及总体主张。'),
    'lean': ('Lean 官方教材 · 公理与计算', 'https://lean-lang.org/theorem_proving_in_lean4/Axioms-and-Computation/', '说明形式化证明所依赖的基础系统与公理。'),
    'first': ('First Proof · 项目官网', 'https://1stproof.org/', '核对独立、透明的研究数学评估目标。'),
    'firstpaper': ('First Proof · 第二批论文', 'https://arxiv.org/abs/2606.18119', '提供测试方法、答案、审稿与运行记录入口。'),
    'etp': ('等式理论项目 · 官网', 'https://teorth.github.io/equational_theories/', '核对研究对象、等式数量和有向蕴含关系。'),
    'etppaper': ('等式理论项目 · 总结论文', 'https://arxiv.org/abs/2512.07087', '核对全部 22,028,942 条关系的完成与 Lean 验证。'),
    'igp': ('IGP24 · SAIR 官方挑战页', 'https://competition.sair.foundation/competitions/igp24/overview', '核对逆伽罗瓦挑战的项目范围。'),
    'igpblog': ('逆伽罗瓦挑战 · 作者介绍', 'https://terrytao.wordpress.com/2026/06/16/third-sair-competition-inverse-galois-challenge/', '核对 24 次情形及与 LMFDB 的合作背景。'),
    'mathlib': ('Mathlib · 数学内容概览', 'https://leanprover-community.github.io/mathlib-overview.html', '核对形式化数学库的性质和覆盖方向。'),
    'mathathon': ('Mathathon · 活动官网', 'https://mathathonchallenge.com/', '核对活动目标、两轮形式与 AI 工具规则。'),
    'ieantn': ('IEANTN · IPAM 项目说明', 'https://www.ipam.ucla.edu/news-research/special-projects/integrated-explicit-analytic-number-theory-network/', '核对显式估计、依赖传播和 AI 辅助形式化的目标。'),
    'ieantnrepo': ('IEANTN · 项目仓库', 'https://github.com/teorth/IEANTN', '核对依赖网络及论证依据的记录方式。'),
}

def external(url, label, cls=''):
    return f'<a class="{cls}" href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)} <span aria-hidden="true">↗</span></a>'

nav = ''.join(f'<a href="#p-{p["n"]:02}" class="page-link" data-page="{p["n"]}"><span>{p["n"]:02}</span>{esc(p["title"].split("：")[0])}</a>' for p in pages)
chapter_nav = ''.join(f'<a class="chapter-link" href="#chapter-{i}"><span>{c[0]}</span><strong>{c[1]}</strong><small>{c[2]}</small></a>' for i,c in enumerate(chapters))
sections = []
for p in pages:
    i=p['n']; c=p['chapter']
    if i == [1,7,13,16,22][c]:
        sections.append(f'<header class="chapter-heading" id="chapter-{c}"><span class="eyebrow">CHAPTER {chapters[c][0]} / {chapters[c][2]}</span><h2>{chapters[c][1]}</h2><p>{chapters[c][3]}</p></header>')
    links=''.join(external(sources[r][1],sources[r][0]) for r in p['refs'])
    sections.append(f'''<article class="slide-article" id="p-{i:02}" data-chapter="{c}" data-page="{i}" aria-labelledby="title-{i}">
      <div class="slide-aside"><div class="slide-meta"><span>SLIDE {i:02} / 27</span><a href="{PDF}#page={i}" target="_blank" rel="noopener noreferrer">PDF 第 {i} 页 ↗</a></div>
      <button class="image-button" data-slide="{i}" aria-label="放大第 {i} 页原始幻灯片"><img src="slide-{i:02}.webp" alt="Math 2.0 原稿第 {i} 页：{esc(p['english'])}" width="1089" height="817" loading="lazy" decoding="async"><span>＋ 放大原图</span></button>
      <p class="original-title">{esc(p['english'])}</p></div>
      <div class="slide-copy"><h3 id="title-{i}">{esc(p['title'])}</h3><p class="takeaway">{esc(p['take'])}</p>
      <div class="original"><span class="copy-label">原页要点 · 中文转述</span><p>{esc(p['original'])}</p></div>
      <div class="explain"><span class="copy-label">逐页解读</span>{''.join('<p>'+esc(t)+'</p>' for t in p['explain'])}</div>
      <aside class="reading-note"><span class="note-dot" aria-hidden="true"></span><p>{esc(p['note'])}</p></aside>
      {f'<div class="inline-sources"><span>补充依据</span>{links}</div>' if links else ''}
      </div></article>''')

source_rows=''.join(f'<li id="ref-{key}">{external(v[1],v[0])}<p>{v[2]}</p></li>' for key,v in sources.items())
html='''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="逐页解读陶哲轩在 Caltech 的 Math 2.0 演讲：27 页原图对照，理解证明丰富、AI 能力边界、人机协作与数学研究的未来。">
<meta name="theme-color" content="#f4f2eb"><title>Math 2.0｜陶哲轩 Caltech 演讲 · 27 页中文解读</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23243733'/%3E%3Ctext x='32' y='46' text-anchor='middle' fill='%23e5eeae' font-size='44' font-family='serif'%3E∑%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="style.css"></head>
<body><a class="skip-link" href="#reading">跳到逐页解读</a><div id="read-progress" aria-hidden="true"></div>
<aside class="rail" aria-label="阅读目录"><a class="wordmark" href="#top">M<span>2.0</span><small>READING NOTES</small></a><div class="rail-caption">陶哲轩 / CALTECH / 2026</div><nav class="chapter-nav">{{CHAPTER_NAV}}</nav><details class="all-pages"><summary>全部 27 页目录 <span>＋</span></summary><nav>{{NAV}}</nav></details><div class="rail-bottom"><a href="#sources">来源与编辑说明 ↗</a><p>以理解为中心的<br>数学研究未来。</p></div></aside>
<main id="top"><header class="hero"><div class="hero-top"><span class="eyebrow">A PAGE-BY-PAGE READING</span><a href="{{PDF}}" target="_blank" rel="noopener noreferrer">阅读原始 PDF ↗</a></div><div class="hero-grid"><div><div class="hero-kicker">Terence Tao · Math 2.0</div><h1>证明增多之后，<br>理解变得<span>更重要。</span></h1><p class="hero-deck">陶哲轩 Caltech 演讲的逐页中文解读。<br>从 AI 的解题突破，走向能够持续产生理解、<br class="desktop-br">方法与新问题的数学研究。</p><a class="primary" href="#reading">开始逐页阅读 <span>↓</span></a></div><div class="hero-visual" aria-hidden="true"><svg viewBox="0 0 360 360"><defs><pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#c7cdc0"/></pattern></defs><rect width="360" height="360" fill="url(#grid)"/><circle cx="180" cy="180" r="136" fill="none" stroke="#b9c1b0"/><ellipse cx="180" cy="180" rx="145" ry="58" fill="none" stroke="#869386" transform="rotate(-35 180 180)"/><ellipse cx="180" cy="180" rx="145" ry="58" fill="none" stroke="#869386" transform="rotate(35 180 180)"/><circle cx="180" cy="180" r="72" fill="#253c34"/><text x="180" y="178" text-anchor="middle" fill="#f7f5ee" font-size="24">人的理解</text><text x="180" y="202" text-anchor="middle" fill="#c9d7b2" font-size="9" letter-spacing="2">UNDERSTANDING</text><circle cx="64" cy="98" r="9" fill="#cc6849"/><circle cx="296" cy="98" r="9" fill="#cc6849"/><circle cx="180" cy="316" r="9" fill="#cc6849"/><text x="34" y="72" fill="#4b5f53" font-size="14">问题</text><text x="286" y="72" fill="#4b5f53" font-size="14">证明</text><text x="180" y="348" text-anchor="middle" fill="#4b5f53" font-size="14">新方法 · 新联系</text></svg></div></div><div class="hero-facts"><span><strong>27</strong> 页完整覆盖</span><span><strong>05</strong> 个阅读章节</span><span>原稿 <b>2026.10</b></span><span>逐页对照 · 图解 · 来源核对</span></div></header>
<section class="orientation" aria-label="阅读说明"><p><strong>先抓住这条主线</strong>数学适合 AI → 证明供给增长 → 只按解题评价可能失配 → 用 AI 强化人的理解。</p><p class="muted">“原页要点”是中文转述；“逐页解读”和旁注是编者说明。所有 27 页均保留对应原图，图像可以点开放大。本文不是演讲逐字稿或作者审定译文。</p></section>
<section class="ecosystem" aria-labelledby="ecosystem-title"><div class="diagram-intro"><span class="eyebrow">THE CENTRAL IDEA · PAGES 18 / 19 / 21</span><h2 id="ecosystem-title">AI 应该加入哪条路径？</h2><p>切换三种模式，看“人的理解”在研究中处于什么位置。</p></div><div class="mode-buttons" aria-label="研究生态模式"><button data-mode="traditional" aria-pressed="false">01 传统研究循环</button><button data-mode="bypass" aria-pressed="false">02 只优化答案</button><button data-mode="augment" aria-pressed="true">03 强化理解</button></div>
<div class="diagram-scroll"><svg id="eco-svg" data-mode="augment" viewBox="0 0 760 400" role="img" aria-labelledby="eco-title eco-desc"><title id="eco-title">Math 2.0 研究生态示意图</title><desc id="eco-desc">纯数学问题与答案通过人的理解形成循环。理解支持符合真实目标的应用。模式切换显示 AI 绕过理解或增强理解的不同路径。</desc><defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="context-stroke"/></marker></defs>
<g class="base-edges"><path d="M182 330H580"/><path d="M182 136H580"/><path d="M182 129Q330 36 580 43" class="risk-edge"/></g>
<g class="understanding-edges"><path d="M168 309Q210 218 295 219"/><path d="M300 241Q225 267 171 317"/><path d="M465 220Q540 236 600 309"/><path d="M605 309Q568 259 462 239"/><path d="M417 199Q468 135 580 138"/></g>
<g class="ai-direct"><path d="M408 360Q495 357 580 336"/><path d="M401 57Q465 20 580 38"/><text x="379" y="371">AI</text><text x="363" y="63">AI</text></g>
<g class="nodes"><rect x="25" y="110" width="160" height="54"/><text x="105" y="143">应用问题</text><rect x="575" y="15" width="165" height="54" class="bad-node"/><text x="657" y="48" class="bad-text">偏离真实目标</text><rect x="575" y="110" width="165" height="54"/><text x="657" y="143">符合真实目标</text><rect x="25" y="304" width="160" height="54"/><text x="105" y="337">纯数学问题</text><rect x="575" y="304" width="165" height="54"/><text x="657" y="337">可验证的答案</text></g>
<g class="human"><rect x="286" y="192" width="190" height="72"/><text x="381" y="222">人的理解</text><text x="381" y="245" class="node-sub">洞见 · 方法 · 判断</text></g><g class="ai-plus"><text x="218" y="254">+ AI</text><text x="504" y="275">+ AI</text><text x="490" y="182">+ AI</text><text x="235" y="299">+ AI</text></g><text class="svg-caption" x="657" y="186">需要结合目标与情境判断</text><text class="svg-caption" x="657" y="383">检查形式化的逻辑关系</text></svg></div>
<div class="diagram-caption" aria-live="polite"><span id="mode-tag">MATH 2.0</span><p id="mode-explanation">AI 帮助提出问题、解释证明、建立联系，并支持应用中的判断。答案继续回流为可分享、可复用的理解。</p></div><p class="diagram-note">依据原稿第 18、19、21 页重绘的概念图。线条表示关系，不表示测量值；“强化理解”是一项设计目标，不是自动获得安全性的保证。</p></section>
<section id="reading" class="reading"><div class="reading-header"><div><span class="eyebrow">THE ANNOTATED SLIDES</span><h2>逐页读懂 Math 2.0</h2></div><span id="result-count" aria-live="polite">27 / 27 页</span></div><div class="reading-tools"><label class="search-box"><span aria-hidden="true">⌕</span><input id="search" type="search" placeholder="搜索概念、项目或页码" aria-label="搜索逐页解读"></label><label class="chapter-select"><span class="sr-only">按章节筛选</span><select id="chapter-filter"><option value="all">全部章节</option>{{OPTIONS}}</select></label><button id="reset-filter" hidden>清除筛选 ×</button></div><div id="empty-state" hidden><strong>没有找到匹配页面</strong><p>试试“理解”“Lean”或页码，或清除筛选。</p></div><div id="articles">{{SECTIONS}}</div></section>
<section class="closing"><span class="eyebrow">THREE DISTINCTIONS TO KEEP</span><h2>读完后，保留三个区分</h2><div class="distinctions"><div><span>01</span><h3>证明正确 ≠ 现实模型正确</h3><p>逻辑核验回答给定前提下能否推出结论。模型是否符合现实，需要另外的证据与判断。</p></div><div><span>02</span><h3>结果丰富 ≠ 理解自动增长</h3><p>证明需要被解释、比较和组织，才能更充分地转化为人的知识与下一轮研究能力。</p></div><div><span>03</span><h3>改进解题 ≠ 只评价解题</h3><p>扩大求解能力有价值。Math 2.0 也重视方法、关系网络、公共知识库与更好的问题。</p></div></div></section>
<section id="sources" class="sources"><span class="eyebrow">SOURCES & EDITORIAL NOTES</span><h2>回到一手材料</h2><div class="source-primary"><span>主要依据</span><a href="{{PDF}}" target="_blank" rel="noopener noreferrer">Terence Tao · Math 2.0 · 27 页原始幻灯片 ↗</a><p>按 2026 年 10 月 11 日读取的 PDF 逐页编写。作者博客将演讲时间注明为 2026 年 10 月 9 日晚，地点为 Caltech。原始幻灯片图像版权归原作者及相应权利人所有，本页用于评论与对照阅读。</p></div><ol>{{SOURCES}}</ol><p class="editorial-note">编辑说明：本页采用简体中文，按简化技术写作的清晰表达原则整理。作者判断、原文转述与编者解释分别标明。补充资料用于核对项目背景；没有实际运行 AI 数学评测，也没有审计各项目全部证明。原稿中的未来计划保留其演讲时的语境。</p></section>
<footer><span>MATH 2.0 / READING NOTES</span><a href="#top">回到顶部 ↑</a></footer></main>
<nav class="mobile-nav" aria-label="移动阅读导航"><a href="#reading">逐页阅读</a><label><span class="sr-only">跳转页码</span><select id="page-jump"><option value="">跳转到…</option>{{PAGE_OPTIONS}}</select></label><a href="#sources">来源 ↗</a></nav>
<dialog id="slide-dialog" aria-labelledby="dialog-title"><div class="dialog-toolbar"><strong id="dialog-title">原始幻灯片</strong><button id="close-dialog" aria-label="关闭原图">关闭 ×</button></div><img id="dialog-image" alt="" width="1089" height="817"><div class="dialog-footer"><button id="previous-slide">← 上一页</button><a id="dialog-pdf" target="_blank" rel="noopener noreferrer">打开 PDF 原页 ↗</a><button id="next-slide">下一页 →</button></div></dialog>
<script src="app.js"></script></body></html>'''
for key,value in {
 'PDF':PDF,'NAV':nav,'CHAPTER_NAV':chapter_nav,'SECTIONS':''.join(sections),'SOURCES':source_rows,
 'OPTIONS':''.join(f'<option value="{i}">{c[0]} · {c[1]}</option>' for i,c in enumerate(chapters)),
 'PAGE_OPTIONS':''.join(f'<option value="{p["n"]}">{p["n"]:02} · {esc(p["title"])}</option>' for p in pages)
}.items():
    html=html.replace('{{'+key+'}}',value)
(ROOT/'index.html').write_text(html)
print(f'Built {len(pages)} pages, {len(html.encode())} bytes HTML')
