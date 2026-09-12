#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Showball 信息学 —— 站点生成器
生成：首页 + 8 个 GESP 等级页 + CSP 页 + 程序模板页 + 题解页
"""
import os, io, json, html, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")

SITE_NAME = "Showball 信息学"
SITE_SUB  = "教练型信息学学习工作台"

# ============ 公共样式 ============
def common_css(prefix=""):
    return prefix + """<style>
:root{
  --bg:#faf7f2; --bg-2:#f4efe7; --card:#fff; --card-2:#fdfbf8;
  --line:#ece5da; --line-2:#e0d6c8;
  --text:#1c1c28; --text-2:#5b5b6b; --text-3:#8b8b9a;
  --brand:#c0392b; --brand-2:#a93226; --brand-soft:#fdf0ee;
  --navy:#2b3a67;
  --shadow-sm:0 1px 2px rgba(28,28,40,.05);
  --shadow:0 2px 8px rgba(28,28,40,.06);
  --shadow-lg:0 8px 28px rgba(28,28,40,.10);
  --radius:14px; --radius-sm:10px; --maxw:1120px;
}
[data-theme="dark"]{
  --bg:#14141c; --bg-2:#1b1b26; --card:#1e1e2a; --card-2:#23232f;
  --line:#2e2e3d; --line-2:#3a3a4c;
  --text:#eceaf2; --text-2:#a8a6b8; --text-3:#7c7a8c;
  --brand:#e05a45; --brand-2:#f0705a; --brand-soft:#2e2020; --navy:#8ba3e8;
  --shadow-sm:0 1px 2px rgba(0,0,0,.25); --shadow:0 2px 8px rgba(0,0,0,.3);
  --shadow-lg:0 8px 28px rgba(0,0,0,.45);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);
  font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei","Segoe UI",Roboto,sans-serif;
  line-height:1.7;-webkit-font-smoothing:antialiased;
  min-height:100vh;display:flex;flex-direction:column;
  transition:background .25s,color .25s}
a{color:inherit;text-decoration:none}
::selection{background:var(--brand);color:#fff}
main{flex:1 0 auto;width:100%}

/* 顶栏 */
header{position:sticky;top:0;z-index:60;background:color-mix(in srgb,var(--bg) 92%,transparent);
  backdrop-filter:saturate(180%) blur(14px);border-bottom:1px solid var(--line)}
.bar{max-width:var(--maxw);margin:0 auto;padding:10px 20px;display:flex;align-items:center;gap:18px}
.brand{display:flex;align-items:center;gap:10px;flex:0 0 auto}
.logo{width:38px;height:38px;border-radius:10px;flex:0 0 auto;
  background:linear-gradient(135deg,var(--navy),#4a6bd6);display:grid;place-items:center;
  color:#fff;font-size:12px;font-weight:800;letter-spacing:.02em}
.brand-txt b{display:block;font-size:15.5px;font-weight:700;line-height:1.3}
.brand-txt small{display:block;font-size:11px;color:var(--text-3);line-height:1.3}
nav{display:flex;gap:2px;margin:0 auto;flex-wrap:wrap}
nav a{padding:7px 13px;border-radius:8px;font-size:14px;color:var(--text-2);transition:.16s;white-space:nowrap}
nav a:hover{color:var(--text);background:var(--bg-2)}
nav a.active{color:var(--text);background:var(--bg-2);font-weight:600}
.bar-right{display:flex;align-items:center;gap:10px;flex:0 0 auto}
.mini-search{display:flex;align-items:center;gap:7px;background:var(--bg-2);
  border:1px solid var(--line);border-radius:9px;padding:7px 12px;width:210px;
  color:var(--text-3);font-size:13px;cursor:text;transition:.18s}
.mini-search:hover{border-color:var(--line-2)}
.theme-btn{width:36px;height:36px;border-radius:50%;flex:0 0 auto;background:var(--bg-2);
  border:1px solid var(--line);color:var(--text-2);cursor:pointer;
  display:grid;place-items:center;transition:.18s;font-size:15px}
.theme-btn:hover{border-color:var(--brand);color:var(--brand)}

/* 页脚 */
footer{background:#1b1b26;color:#8b8b9a;padding:26px 20px;text-align:center;font-size:13px;margin-top:auto}
footer b{color:#c9c9d6;font-weight:600}
footer .flinks{margin-top:8px;display:flex;gap:18px;justify-content:center;flex-wrap:wrap}
footer a:hover{color:#fff}

/* 通用组件 */
.panel{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow-sm)}
.link-red{color:var(--brand);font-size:14px;font-weight:600;
  display:inline-flex;align-items:center;gap:4px;border-bottom:1px solid transparent;transition:.16s}
.link-red:hover{border-bottom-color:var(--brand)}
.btn{display:inline-flex;align-items:center;gap:7px;padding:11px 22px;border-radius:9px;
  font-size:14.5px;font-weight:600;cursor:pointer;border:1px solid transparent;transition:.18s}
.btn-primary{background:var(--brand);color:#fff;box-shadow:var(--shadow-sm)}
.btn-primary:hover{background:var(--brand-2);transform:translateY(-1px);box-shadow:var(--shadow)}
.btn-ghost{background:var(--card);color:var(--text);border-color:var(--line-2)}
.btn-ghost:hover{border-color:var(--brand);color:var(--brand)}
.pill{display:inline-flex;align-items:center;gap:7px;background:var(--brand-soft);
  border:1px solid color-mix(in srgb,var(--brand) 18%,transparent);color:var(--brand);
  border-radius:999px;padding:5px 14px;font-size:12.5px;font-weight:500;margin-bottom:20px}
.pill i{width:6px;height:6px;border-radius:50%;background:var(--brand);display:block;flex:0 0 auto}
.crumb{font-size:12.5px;color:var(--text-3);margin-bottom:10px}
.crumb a{color:var(--brand)}
.crumb a:hover{border-bottom:1px solid var(--brand)}

/* 响应式 */
@media (max-width:860px){
  .bar{flex-wrap:wrap;gap:12px}
  nav{order:3;width:100%;margin:0;overflow-x:auto;padding-bottom:4px}
  .bar-right{margin-left:auto}
  .mini-search{display:none}
}
#toTop{position:fixed;right:22px;bottom:22px;z-index:70;width:42px;height:42px;border-radius:50%;
  cursor:pointer;background:var(--card);color:var(--text-2);font-size:16px;
  border:1px solid var(--line-2);box-shadow:var(--shadow);
  display:grid;place-items:center;opacity:0;pointer-events:none;transition:.25s}
#toTop.on{opacity:1;pointer-events:auto}
#toTop:hover{color:var(--brand);border-color:var(--brand)}
</style>"""


def head(title, desc, prefix=""):
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#faf7f2">
<script>
(function(){{try{{if(localStorage.getItem("theme")==="dark")document.documentElement.setAttribute("data-theme","dark");}}catch(e){{}}}})();
</script>
{common_css(prefix)}
</head>
<body>"""


def header_html(nav_items, prefix="", active=""):
    links = []
    for label, href, key in nav_items:
        cls = ' class="active"' if key == active else ""
        links.append(f'<a href="{prefix}{href}"{cls}>{label}</a>')
    nav = "\n      ".join(links)
    return f"""
<header>
  <div class="bar">
    <a class="brand" href="{prefix}index.html">
      <div class="logo">OI</div>
      <div class="brand-txt">
        <b>{SITE_NAME}</b>
        <small>{SITE_SUB}</small>
      </div>
    </a>
    <nav>
      {nav}
    </nav>
    <div class="bar-right">
      <div class="mini-search">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
          <circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>
        </svg>
        <span>知识点 / 题目 / 教程</span>
      </div>
      <button class="theme-btn" id="themeBtn" title="切换主题">◐</button>
    </div>
  </div>
</header>
"""


NAV = [
    ("首页",        "index.html",       "home"),
    ("GESP 1–8 级", "gesp.html",        "gesp"),
    ("CSP-J/S",     "csp.html",         "csp"),
    ("程序模板",    "templates.html",   "tpl"),
    ("题解",        "solutions.html",   "sol"),
    ("OJ 与资源",   "resources.html",   "res"),
]


def footer_html(prefix=""):
    links = "".join(f'<a href="{prefix}{h}">{l}</a>' for l, h, _ in NAV)
    return f"""
<footer>
  <b>{SITE_NAME}</b>
  <div class="flinks">{links}</div>
  <p style="margin:10px 0 0;font-size:12px;opacity:.7">{SITE_NAME} · 内容持续补充中</p>
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


# ============ 知识点数据 ============
# 结构: {等级: [(编号, 标题, 描述, [标签...]), ...]}
LEVELS = {
1: ("编程入门知识字典", "GESP 一级要求学生了解计算机与开发环境，掌握 C++ 程序结构、输入输出、基本数据类型、基本运算，以及顺序、分支、循环三种结构。学完后应能读懂并编写单层程序，结合编译信息、样例和变量变化检查错误。", [
 ("计算机基础知识", "认识计算机的发展、组成、软硬件、操作系统与文件目录。", ["计算机组成","软硬件"]),
 ("集成开发环境", "完成编辑、编译、运行和调试，判断常见程序错误。", ["IDE","编译调试"]),
 ("程序基本结构", "理解头文件、命名空间、main 函数、语句、代码块和注释。", ["main函数","程序框架"]),
 ("输入输出语句", "使用 cin、cout、scanf、printf，并按题目要求控制输出格式。", ["cin-cout","scanf-printf"]),
 ("程序基本概念", "掌握标识符、关键字、常量、变量、赋值、表达式。", ["变量常量","标识符表达式"]),
 ("基本数据类型", "认识整型、浮点、字符和布尔类型的范围，理解与选择方法。", ["int-double","char-bool"]),
 ("基本运算", "掌握算术、关系、逻辑、赋值、自增自减及优先级规则。", ["运算符","优先级"]),
 ("顺序结构", "按顺序完成输入、计算和输出，并通过变量变化检查。", ["顺序执行","变量追踪"]),
 ("分支结构", "使用 if、if-else、else-if、switch 和三元运算处理不同情况。", ["if-else","switch-case"]),
 ("循环结构", "掌握三种循环与循环控制，解决累加、最值、位数、数列和枚举问题。", ["for-while","循环控制"]),
]),
2: ("编程基础与流程图", "GESP 二级在基本语法之上引入存储与网络常识、程序设计语言的分类与编译运行过程、流程图表示法，以及数据类型转换、多分支、循环嵌套和常用数学函数。重点是读懂流程图并把它与代码互相翻译。", [
 ("计算机存储与网络", "了解存储单位换算，认识网络协议与常见网络概念。", ["存储与单位","网络与协议"]),
 ("程序设计语言", "区分机器语言、汇编语言与高级语言，了解编译与运行过程。", ["语言分类","编译过程"]),
 ("流程图", "识别流程图符号，追踪流程走向，并在流程图与代码之间互相翻译。", ["符号辨认","流程追踪"]),
 ("数据类型转换", "掌握隐式转换与强制转换，注意整数除法与精度丢失。", ["隐式转换","强制转换"]),
 ("多分支判断", "处理分支嵌套与条件边界，避免遗漏情况。", ["分支嵌套","条件边界"]),
 ("循环嵌套", "用双重循环处理行列、图形与枚举问题，控制内层跳转。", ["行列问题","内层跳转"]),
 ("常用数学函数", "使用绝对值、平方根、最大最小值与随机数，注意取值范围。", ["绝对值平方根","最大最小值"]),
 ("程序调试", "根据编译信息与运行结果定位错误，学会输出中间变量。", ["编译信息","中间输出"]),
]),
3: ("数据编码与算法初步", "GESP 三级进入数据表示与算法描述：理解数据编码与进制转换、位运算，掌握算法的概念与描述方式，并开始系统使用数组、字符串和枚举，能估算简单程序的操作次数。", [
 ("数据编码", "确认每个数使用的二进制位数，判断能表示的整数范围。", ["二进制位数","整数范围"]),
 ("进制转换", "掌握任意进制与十进制之间的转换方法，并检查数字合法性。", ["按权展开","除基取余"]),
 ("位运算", "掌握与、或、异或、取反和移位，安全地进行位操作。", ["按位运算","移位"]),
 ("算法的概念与描述", "判断步骤是否明确且能结束，按接近代码的步骤推断输出。", ["步骤明确","结果推断"]),
 ("一维数组", "按位置编号访问元素，完成统计、查找和最值更新，并检查下标范围。", ["下标访问","范围检查"]),
 ("字符串处理", "按位置访问字符，查找与截取连续子串，完成连接与替换。", ["字符访问","子串截取"]),
 ("枚举算法", "确定枚举范围与判断条件，逐个检查并统计或更新最优解。", ["枚举范围","条件判断"]),
 ("模拟算法", "按题目规则保存状态并逐步推进，得到最终结果。", ["状态保存","规则推进"]),
]),
4: ("函数、指针与结构体", "GESP 四级引入函数与作用域、指针与引用、结构体与二维数组，并开始关注递推、排序算法和复杂度估算，同时了解文件操作与异常处理的基本写法。", [
 ("函数基础", "掌握函数声明与定义、调用与返回值，把重复任务拆分成函数。", ["声明定义","返回值"]),
 ("参数与作用域", "区分形参与实参，理解局部与全局变量、作用域与遮蔽。", ["形参实参","作用域"]),
 ("指针基础", "获取变量地址、解引用指针，并做空指针检查。", ["取地址","解引用"]),
 ("引用与参数传递", "区分值传递与引用传递，掌握数组作为参数的行为。", ["值传递","引用参数"]),
 ("结构体", "定义结构体类型与对象，访问成员，使用结构体数组。", ["成员访问","结构体数组"]),
 ("二维数组", "定义二维数组，完成行列遍历与矩阵基本操作。", ["行列遍历","矩阵操作"]),
 ("递推", "确定初始状态与递推关系，按顺序计算得到结果。", ["初始状态","递推关系"]),
 ("排序算法", "掌握冒泡、插入、选择排序的过程与稳定性。", ["冒泡排序","选择排序"]),
 ("复杂度估算", "估算操作次数，理解时间复杂度与空间复杂度的含义。", ["时间复杂度","空间复杂度"]),
 ("文件与异常", "完成文件重定向与文件流读写，处理输入校验与异常捕获。", ["文件流","异常处理"]),
]),
5: ("数论、链表与分治", "GESP 五级进入初等数论、高精度运算与线性数据结构，掌握链表与数组模拟链表、顺序查找与二分查找、二分答案、贪心与分治排序，并能根据数据范围判断复杂度是否可行。", [
 ("初等数论基础", "掌握整除与约数、素数与互质、同余与余数。", ["整除约数","同余"]),
 ("最大公约数", "用欧几里得算法求最大公约数，并推导最小公倍数与分数约分。", ["辗转相除","最小公倍数"]),
 ("素数筛法", "掌握埃氏筛与线性筛，实现素数表查询。", ["埃氏筛","线性筛"]),
 ("质因数分解", "写出标准分解式，求约数个数与约数和。", ["分解式","约数个数"]),
 ("高精度运算", "用数组存储大整数，处理进位借位以及与普通整数的乘除。", ["进位借位","大整数"]),
 ("链表", "掌握单向与双向链表的插入、删除与反转，会用数组模拟。", ["链表操作","数组模拟"]),
 ("顺序查找", "实现精确查找与左右边界查找，统计出现次数。", ["精确查找","左右边界"]),
 ("二分答案", "判断单调性，求最小可行值与最大可行值。", ["单调判定","边界取值"]),
 ("贪心算法", "完成贪心选择、排序后构造，并用交换论证说明正确性。", ["贪心选择","交换论证"]),
 ("分治与排序", "掌握分治三步，实现归并排序与快速排序。", ["分治三步","归并快排"]),
 ("递归", "明确递归出口，理解调用与返回过程，完成递归枚举。", ["递归出口","递归枚举"]),
 ("复杂度与数据范围", "根据数据范围判断算法是否可行，选择合适复杂度。", ["数据范围","复杂度判断"]),
]),
6: ("树结构与编码", "GESP 六级围绕树展开：树的构造与各种遍历、特殊二叉树、哈夫曼编码与格雷码，以及迷宫路径枚举与回溯，强调从层次结构走向系统化的问题求解。", [
 ("树的基础知识", "理解结点、边、根、子树、深度与度的概念。", ["结点关系","树的术语"]),
 ("树的构造与遍历", "根据输入构造树，掌握先序、中序、后序遍历。", ["构造树","三种遍历"]),
 ("层序遍历", "用队列按层访问结点，处理按层统计问题。", ["队列实现","按层访问"]),
 ("遍历序列还原", "根据两种遍历序列还原二叉树，并推断第三种序列。", ["序列还原","结构推断"]),
 ("特殊二叉树", "掌握二叉搜索树、完全二叉树与满二叉树的性质。", ["二叉搜索树","完全二叉树"]),
 ("哈夫曼编码", "构造哈夫曼树，计算带权路径长度并生成编码。", ["哈夫曼树","带权路径"]),
 ("格雷码", "理解格雷码的生成规则与相邻码字只差一位的性质。", ["生成规则","相邻码字"]),
 ("路径枚举与回溯", "在迷宫中枚举路径，处理状态标记与撤销。", ["状态标记","回溯撤销"]),
 ("深度优先搜索", "用递归实现 DFS，处理连通性与路径问题。", ["递归搜索","连通性"]),
 ("广度优先搜索", "用队列实现 BFS，求最短步数与层次信息。", ["队列搜索","最短步数"]),
]),
7: ("数学工具与图论入门", "GESP 七级进入数学库函数、复杂与二维动态规划、图的基本概念与存储、图的遍历，以及哈希表等关联容器的使用，为综合问题求解打基础。", [
 ("数学库常用函数", "处理角度与弧度换算，检查函数定义域，按题意处理浮点结果。", ["角度弧度","浮点处理"]),
 ("复杂动态规划", "增加状态维度，按阶段推进状态，按区间长度完成转移。", ["状态维度","阶段推进"]),
 ("二维动态规划", "处理网格最值、最长公共子序列与编辑距离。", ["网格最值","编辑距离"]),
 ("线性动态规划", "掌握最大连续和、最长上升子序列与背包空间优化。", ["最大连续和","空间优化"]),
 ("图的基本概念", "识别图的组成，计算顶点的度，判断路径、环与连通性。", ["顶点与边","连通性"]),
 ("图的存储", "掌握邻接矩阵、邻接表与链式前向星。", ["邻接矩阵","邻接表"]),
 ("图的遍历", "实现 DFS 与 BFS 遍历，处理非连通图。", ["DFS遍历","非连通图"]),
 ("网格搜索", "检查网格边界，使用方向数组扩展，标记并统计连通区域。", ["方向数组","连通区域"]),
 ("哈希表与集合", "统计元素出现次数，判断存在性，比较有序与无序关联容器。", ["键值统计","关联容器"]),
 ("综合应用", "把图论、动态规划与数据结构组合起来解决问题。", ["算法组合","建模"]),
]),
8: ("计数、图论与复杂度", "GESP 八级从准确建模走向复杂度可控的综合求解：计数原理与组合数、倍增与二进制拆分、数列与几何计算，以及最小生成树、最短路和常见优化手段。", [
 ("计数原理", "掌握加法原理与乘法原理，区分分类与分步。", ["加法原理","乘法原理"]),
 ("排列与组合", "计算排列数与阶乘，理解组合数的意义与性质。", ["排列数","组合数"]),
 ("杨辉三角", "处理边界条件，用递推与预处理求组合数。", ["边界条件","组合数递推"]),
 ("倍增", "用二进制拆分与倍增预处理实现快速查询。", ["二进制拆分","倍增查询"]),
 ("数列与代数", "对表达式化简，处理等差数列与等比数列。", ["数列求和","表达式化简"]),
 ("几何计算", "计算面积与周长、坐标距离，注意退化图形。", ["坐标距离","退化图形"]),
 ("图算法选择", "根据顶点、边、方向与权值选择合适的图算法。", ["图建模","算法选择"]),
 ("最小生成树", "理解生成树与最小生成树，实现 Prim 与 Kruskal。", ["Prim","Kruskal"]),
 ("单源最短路", "理解松弛操作，实现 Dijkstra 与负权处理。", ["松弛操作","Dijkstra"]),
 ("复杂度分析", "分析常见算法复杂度，按数据范围选择算法。", ["复杂度","范围判断"]),
 ("空间优化", "优化数组空间与图存储，使用滚动数组。", ["滚动数组","图存储"]),
 ("算法优化", "在暴力与剪枝、预处理与数学优化之间做出选择。", ["暴力剪枝","预处理"]),
]),
}

CSP = [
 ("01", "CSP-J 初赛", "计算机基础、C++ 语法、算法阅读与选择填空。",
  "先把握题目和选项的读法", "#5b8def"),
 ("02", "CSP-J 复赛", "模拟、枚举、排序、搜索、简单动态规划与代码规范。",
  "把思路写成完整程序", "#22b8a0"),
 ("03", "CSP-S 进阶", "图论、树结构、数论、复杂动态规划与复杂度控制。",
  "进入更综合的算法训练", "#a56bf0"),
]

TEMPLATES = [
 ("基础框架", "C++ 程序基本框架与快读快写，适合大数据量输入。", "基础"),
 ("数据结构", "并查集（路径压缩 + 按秩合并）、树状数组、线段树区间查询。", "数据结构"),
 ("图论", "邻接表存图、Dijkstra 堆优化、SPFA、拓扑排序。", "图论"),
 ("动态规划", "01 背包、完全背包、最长上升子序列与滚动数组优化。", "动态规划"),
 ("字符串", "KMP 匹配、字符串哈希、字典树。", "字符串"),
 ("数学", "快速幂、扩展欧几里得、素数筛与组合数预处理。", "数学"),
]

SOLUTIONS = [
 ("模拟", "按题意直接实现", "重点在边界处理与细节检查，先把题意翻译成清晰的步骤。"),
 ("搜索", "DFS / BFS", "状态如何设计、何时剪枝、如何去重，是搜索题的核心。"),
 ("贪心", "排序与选择", "构造贪心策略，并用交换论证或反例检验正确性。"),
 ("动态规划", "状态与转移", "确定状态含义、转移方程、初始化与遍历顺序。"),
 ("图论", "最短路与生成树", "识别是单源还是多源、有无负权，再选择合适算法。"),
 ("数论", "质数与同余", "筛法、快速幂、逆元与同余方程的处理方法。"),
]

RESOURCES = [
 ("OJ", "洛谷", "国内主流题库，题目与题解丰富", "https://www.luogu.com.cn/"),
 ("百科", "OI Wiki", "算法竞赛知识百科，查算法与证明", "https://oi-wiki.org/"),
 ("官方", "NOI 官网", "赛事通知、大纲与政策", "https://www.noi.cn/"),
 ("比赛", "Codeforces", "国际比赛与高质量题目", "https://codeforces.com/"),
]


# ============ 页面生成 ============
def extra_css():
    return """<style>
/* 首页 */
.hero{padding:68px 20px 40px;text-align:center}
.hero-inner{max-width:720px;margin:0 auto}
.hero h1{font-size:clamp(30px,5.2vw,46px);font-weight:800;letter-spacing:-.02em;margin:0 0 12px;line-height:1.2}
.hero .sub{color:var(--text-2);font-size:15.5px;margin:0 0 28px}
.big-search{display:flex;align-items:center;gap:10px;background:var(--card);
  border:1px solid var(--line-2);border-radius:12px;padding:13px 16px;box-shadow:var(--shadow);
  max-width:620px;margin:0 auto 22px;transition:.2s;cursor:text}
.big-search:focus-within{border-color:var(--brand);box-shadow:0 0 0 4px color-mix(in srgb,var(--brand) 12%,transparent)}
.big-search svg{color:var(--text-3);flex:0 0 auto}
.big-search b{font-size:14.5px;font-weight:600;flex:0 0 auto}
.big-search input{flex:1;border:0;outline:0;background:transparent;font-size:14.5px;
  color:var(--text);font-family:inherit;min-width:0}
.big-search input::placeholder{color:var(--text-3)}
.kbd{font-size:11.5px;color:var(--text-3);background:var(--bg-2);border:1px solid var(--line);
  border-radius:5px;padding:2px 7px;flex:0 0 auto;font-family:inherit}
.hero-actions{display:flex;gap:11px;justify-content:center;flex-wrap:wrap}
.hero-note{color:var(--text-3);font-size:13px;margin:16px 0 0}
#results{max-width:620px;margin:10px auto 0;background:var(--card);border:1px solid var(--line-2);
  border-radius:var(--radius-sm);box-shadow:var(--shadow-lg);overflow:hidden;display:none;text-align:left}
#results.on{display:block}
#results a{display:block;padding:11px 18px;font-size:14px;border-bottom:1px solid var(--line);transition:.14s}
#results a:last-child{border-bottom:0}
#results a:hover{background:var(--bg-2);padding-left:24px}
#results a span{color:var(--text-3);font-size:12.5px}
#results .empty{padding:16px 18px;color:var(--text-3);font-size:13.5px}

main.wrap{max-width:var(--maxw);margin:0 auto;padding:0 20px 60px}
main.wide{max-width:var(--maxw);margin:0 auto;padding:0 20px 60px}
.sec{margin-bottom:52px}
.sec>h2{font-size:22px;font-weight:700;letter-spacing:-.01em;margin:0 0 6px}
.sec>.sec-sub{color:var(--text-2);font-size:14px;margin:0 0 22px}
.sec-head{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:14px;flex-wrap:wrap}
.sec-head h3{font-size:15.5px;font-weight:700;margin:0}
.sec-head .hint{color:var(--text-3);font-size:12.5px}
.lastvisit{display:flex;align-items:center;gap:20px;padding:20px 24px;margin-bottom:52px;flex-wrap:wrap}
.lastvisit .lv-left b{display:block;font-size:15px;font-weight:700}
.lastvisit .lv-left span{font-size:12.5px;color:var(--text-3)}
.lastvisit .lv-mid{flex:1;color:var(--text-2);font-size:14px;min-width:200px}
.lastvisit .lv-right{display:flex;gap:18px;flex-wrap:wrap}

/* 等级卡（首页） */
.levels{display:grid;grid-template-columns:repeat(8,1fr);gap:10px}
.lv-card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius-sm);
  padding:14px 12px 15px;box-shadow:var(--shadow-sm);transition:.2s;position:relative;
  overflow:hidden;display:block}
.lv-card::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:var(--bar,var(--brand))}
.lv-card:hover{transform:translateY(-4px);border-color:var(--line-2);box-shadow:var(--shadow-lg)}
.lv-card .no{font-size:11.5px;font-weight:700;color:var(--text-3);letter-spacing:.08em}
.lv-card .lv{font-size:24px;font-weight:800;line-height:1.15;margin-top:2px}
.lv-card .lbl{font-size:12px;color:var(--text-2);margin-top:1px}
.lv-card .desc{font-size:11.5px;color:var(--text-3);margin:9px 0 0;line-height:1.55;
  border-top:1px solid var(--line);padding-top:8px}

/* 横栏列表 */
.rows{display:grid;gap:10px}
.row{display:flex;align-items:center;gap:14px;background:var(--card);border:1px solid var(--line);
  border-radius:var(--radius-sm);padding:14px 18px;box-shadow:var(--shadow-sm);transition:.2s}
.row:hover{border-color:var(--line-2);transform:translateX(3px)}
.row .tag{flex:0 0 auto;font-size:12px;font-weight:700;background:var(--brand-soft);
  color:var(--brand);border-radius:6px;padding:4px 10px}
.row .t{flex:0 0 auto;font-size:14.5px;font-weight:600}
.row .d{flex:1;font-size:13px;color:var(--text-3);min-width:0}
.row .go{flex:0 0 auto;color:var(--text-3);font-size:15px}

/* 等级页 */
.level-layout{display:grid;grid-template-columns:250px 1fr;gap:36px;align-items:start;
  max-width:var(--maxw);margin:0 auto;padding:34px 20px 60px}
.side{position:sticky;top:78px;background:var(--card);border:1px solid var(--line);
  border-radius:var(--radius);box-shadow:var(--shadow-sm);overflow:hidden}
.side-h{padding:15px 18px;border-bottom:1px solid var(--line);font-size:14.5px;font-weight:700}
.side-g{padding:13px 18px 8px;font-size:12px;font-weight:600;color:var(--text-3);letter-spacing:.04em}
.side-list{list-style:none;margin:0;padding:0 0 12px}
.side-list li a{display:flex;gap:9px;padding:7px 18px;font-size:13.2px;color:var(--text-2);
  transition:.14s;border-left:3px solid transparent}
.side-list li a:hover{background:var(--bg-2);color:var(--text);border-left-color:var(--brand)}
.side-list li a .n{color:var(--text-3);font-variant-numeric:tabular-nums;flex:0 0 auto;font-size:12px}

.lv-hero{padding:0 0 8px}
.lv-hero h1{font-size:clamp(32px,5vw,48px);font-weight:800;margin:8px 0 0;letter-spacing:-.02em}
.intro{display:grid;grid-template-columns:1fr 1.15fr;gap:32px;align-items:start;
  padding:28px 0 32px;border-bottom:1px solid var(--line);margin-bottom:32px}
.intro h2{font-size:26px;font-weight:700;line-height:1.35;margin:0}
.intro p{color:var(--text-2);font-size:14px;margin:0;line-height:1.85}

.progress{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:1px;
  background:var(--line);border:1px solid var(--line);border-radius:var(--radius);
  overflow:hidden;margin-bottom:40px}
.progress>div{background:var(--card);padding:18px 20px}
.progress .p-title{font-size:14.5px;font-weight:700;margin-bottom:4px}
.progress .p-desc{font-size:12.5px;color:var(--text-3);line-height:1.6}
.progress .p-num{font-size:21px;font-weight:800;color:var(--brand);font-variant-numeric:tabular-nums}
.progress .p-lbl{font-size:12px;color:var(--text-3);margin-top:2px}

.kp-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.kp{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:17px 18px;box-shadow:var(--shadow-sm);transition:.2s;display:flex;flex-direction:column}
.kp:hover{border-color:var(--line-2);transform:translateY(-3px);box-shadow:var(--shadow-lg)}
.kp-top{display:flex;align-items:center;gap:8px;margin-bottom:9px}
.kp-top .no{font-size:11.5px;font-weight:700;color:var(--text-3);letter-spacing:.06em}
.kp-top .badge{font-size:10.5px;font-weight:700;background:var(--brand-soft);color:var(--brand);
  border-radius:4px;padding:2px 7px}
.kp-top .state{margin-left:auto;font-size:11px;color:var(--text-3);
  background:var(--bg-2);border-radius:4px;padding:2px 7px}
.kp h4{margin:0 0 7px;font-size:16px;font-weight:700}
.kp p{margin:0 0 12px;font-size:12.8px;color:var(--text-2);line-height:1.7;flex:1}
.kp .tags{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px}
.kp .tags span{font-size:10.5px;color:var(--text-3);background:var(--bg-2);
  border-radius:4px;padding:2px 8px}

/* CSP 阶段卡 */
.stage-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.stage{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:20px 20px 18px;box-shadow:var(--shadow-sm);position:relative;overflow:hidden;transition:.2s}
.stage::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:var(--bar,var(--brand))}
.stage:hover{transform:translateY(-4px);box-shadow:var(--shadow-lg)}
.stage .no{font-size:13px;font-weight:800;color:var(--brand);letter-spacing:.08em}
.stage .tip{font-size:12px;color:var(--text-3);margin:8px 0 14px}
.stage h3{font-size:19px;font-weight:700;margin:0 0 8px}
.stage p{font-size:13px;color:var(--text-2);margin:0 0 16px;line-height:1.7}
.stage .foot{border-top:1px solid var(--line);padding-top:12px}

/* 代码块 */
.code{background:#1b1b26;border-radius:var(--radius-sm);padding:16px 18px;overflow-x:auto;
  font-family:"SF Mono",Monaco,Menlo,Consolas,monospace;font-size:12.5px;line-height:1.75;
  color:#c9d1d9;border:1px solid #2e2e3d}
.code .k{color:#ff7b72}.code .t{color:#79c0ff}.code .f{color:#d2a8ff}.code .c{color:#8b949e}

.two{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.tool-card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:18px;box-shadow:var(--shadow-sm);display:flex;flex-direction:column;margin-bottom:12px}
.tool-card h4{margin:0 0 6px;font-size:16px;font-weight:700}
.tool-card p{margin:0 0 12px;font-size:13px;color:var(--text-3);flex:1}

@media (max-width:1040px){
  .levels{grid-template-columns:repeat(4,1fr)}
  .kp-grid{grid-template-columns:repeat(2,1fr)}
  .stage-grid{grid-template-columns:1fr}
  .level-layout{grid-template-columns:1fr}
  .side{position:static}
}
@media (max-width:620px){
  .levels{grid-template-columns:repeat(2,1fr)}
  .kp-grid{grid-template-columns:1fr}
  .intro{grid-template-columns:1fr;gap:16px}
  .progress{grid-template-columns:1fr 1fr}
  .two{grid-template-columns:1fr}
  .big-search b{display:none}
}
</style>"""


def page_shell(title, desc, body, active, prefix="", css_extra=True):
    return (head(title, desc, prefix)
            + header_html(NAV, prefix, active)
            + (extra_css() if css_extra else "")
            + "\n" + body + "\n"
            + footer_html(prefix))


def write_page(relpath, content):
    path = os.path.join(SITE, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    io.open(path, "w", encoding="utf-8").write(content)
    return path


# ---------- 首页 ----------
def build_home():
    lv_cards = ""
    colors = ["#5b8def","#7c6bf0","#a56bf0","#d86bc8","#ef6b9c","#ef7b6b","#ef9d6b","#d9a441"]
    for i in range(1, 9):
        d = LEVELS[i][2][0][1][:22]
        lv_cards += f"""
        <a class="lv-card" href="gesp/level{i}.html" style="--bar:{colors[i-1]}">
          <div class="no">{i:02d}</div>
          <div class="lv" style="color:{colors[i-1]}">{i}级</div>
          <div class="lbl">GESP {i} 级</div>
          <div class="desc">{html.escape(d)}</div>
        </a>"""

    csp_rows = ""
    for no, name, desc, sub, bar in CSP:
        csp_rows += f"""
        <a class="row" href="csp.html">
          <span class="tag">{name.split()[0].replace('CSP-','')}</span>
          <span class="t">{name}</span>
          <span class="d">{html.escape(desc)}</span>
          <span class="go">→</span>
        </a>"""

    res_rows = ""
    for tag, name, desc, url in RESOURCES:
        res_rows += f"""
        <a class="row" href="{url}" target="_blank" rel="noopener">
          <span class="tag">{tag}</span>
          <span class="t">{name}</span>
          <span class="d">{html.escape(desc)}</span>
          <span class="go">↗</span>
        </a>"""

    tpl_rows = ""
    for name, desc, tag in TEMPLATES[:4]:
        tpl_rows += f"""
        <a class="tool-card" href="templates.html">
          <h4>{name}</h4>
          <p>{html.escape(desc)}</p>
          <span class="link-red">打开模板 →</span>
        </a>"""

    body = f"""
<main>
  <section class="hero">
    <div class="hero-inner">
      <div class="pill"><i></i>{SITE_NAME} · C++ 学习词典</div>
      <h1>今天想解决什么？</h1>
      <p class="sub">继续当前学习，或者先把一道题卡住的地方解决掉。</p>
      <div class="big-search" id="bigSearchWrap">
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
          <circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
        <b>搜索全站</b>
        <input id="search" type="search" placeholder="搜索知识点、题目、模板……" autocomplete="off">
        <span class="kbd">ctrl K</span>
      </div>
      <div class="hero-actions">
        <a class="btn btn-primary" href="gesp.html">开始学习 →</a>
        <a class="btn btn-ghost" href="#stuck">解决做题卡点</a>
      </div>
      <p class="hero-note">从 GESP 学习路线选择当前级别</p>
    </div>
  </section>

  <div id="results"></div>

  <div class="wrap">
    <div class="panel lastvisit">
      <div class="lv-left"><b>上次访问</b><span>只记录在这台设备上。</span></div>
      <div class="lv-mid" id="lastVisitText">还没有最近访问。先选择一条路线，之后可以从这里返回。</div>
      <div class="lv-right">
        <a class="link-red" href="gesp.html">从 GESP 开始 →</a>
        <a class="link-red" href="csp.html">查看 CSP 路线</a>
      </div>
    </div>

    <section class="sec" id="levels">
      <h2>选择学习路线</h2>
      <p class="sec-sub">GESP 按当前等级学习；CSP 按考试阶段准备。</p>
      <div class="sec-head"><h3>GESP 一级至八级</h3><span class="hint">按等级查询，不设访问门槛</span></div>
      <div class="levels">{lv_cards}</div>
    </section>

    <section class="sec" id="csp">
      <div class="sec-head"><h3>CSP-J/S</h3><a class="link-red" href="csp.html">查看 CSP 学习路线 →</a></div>
      <div class="rows">{csp_rows}</div>
    </section>

    <section class="sec" id="stuck">
      <h2>这道题卡在哪里？</h2>
      <p class="sec-sub">先判断卡点，再进入对应内容。</p>
      <div class="two">
        <div class="rows">
          <a class="row" href="solutions.html">
            <span class="tag">01</span><span class="t">看不懂题意</span>
            <span class="d">先看清样例，把题意转化成条件、目标和边界</span><span class="go">→</span></a>
          <a class="row" href="solutions.html">
            <span class="tag">02</span><span class="t">不知道思路</span>
            <span class="d">对照题型清单确认已经见过的模式</span><span class="go">→</span></a>
          <a class="row" href="templates.html">
            <span class="tag">03</span><span class="t">不会写代码</span>
            <span class="d">从可以修改的程序模板开始</span><span class="go">→</span></a>
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
      <div class="two">
        <div>{tpl_rows}</div>
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

    <section class="sec" id="resources">
      <h2>OJ 与学习资源</h2>
      <p class="sec-sub">返回题库练习，或查看权威资料。</p>
      <div class="rows">{res_rows}</div>
    </section>
  </div>
</main>

<script>
(function(){{
  "use strict";
  var INDEX = [
    {{t:"GESP 分级总览", d:"八级学习路线", h:"gesp.html"}},
    {{t:"CSP-J/S", d:"初赛、复赛与进阶", h:"csp.html"}},
    {{t:"程序模板", d:"可修改的 C++ 代码框架", h:"templates.html"}},
    {{t:"题解", d:"读题、思路与代码映射", h:"solutions.html"}},
    {{t:"OJ 与资源", d:"题库与学习资料", h:"resources.html"}}
  ];
  var LV = ["计算机基础","集成开发环境","程序基本结构","输入输出","基本数据类型","基本运算","顺序结构","分支结构","循环结构","存储与网络","流程图","类型转换","数组","字符串","枚举","模拟","函数","指针","结构体","二维数组","排序","递推","数论","素数筛","高精度","链表","二分","贪心","分治","递归","树","遍历","哈夫曼","格雷码","回溯","搜索","动态规划","图论","最短路","最小生成树","哈希表","计数原理","排列组合","倍增","复杂度"];
  for (var i = 1; i <= 8; i++) {{
    INDEX.push({{t:"GESP " + i + " 级", d:"第 " + i + " 级知识点", h:"gesp/level" + i + ".html"}});
  }}
  LV.forEach(function(k){{ INDEX.push({{t:k, d:"知识点查询", h:"gesp.html"}}); }});

  var input = document.getElementById("search"), box = document.getElementById("results");
  function render(kw){{
    var q = kw.trim().toLowerCase();
    if(!q){{ box.className=""; box.innerHTML=""; return; }}
    var hit = INDEX.filter(function(it){{ return (it.t+" "+it.d).toLowerCase().indexOf(q)!==-1; }}).slice(0,8);
    box.innerHTML = hit.length ? hit.map(function(it){{
      return '<a href="'+it.h+'"><b>'+it.t+'</b> <span>'+it.d+'</span></a>';
    }}).join("") : '<div class="empty">没有找到「'+kw.replace(/[<>&]/g,"")+'」，换个关键词试试</div>';
    box.className = "on";
  }}
  input.addEventListener("input", function(){{ render(this.value); }});
  input.addEventListener("keydown", function(e){{
    if(e.key==="Enter"){{ var f=box.querySelector("a"); if(f)f.click(); }}
    if(e.key==="Escape"){{ box.className=""; input.blur(); }}
  }});
  document.addEventListener("click", function(e){{
    if(!e.target.closest("#bigSearchWrap") && !e.target.closest("#results")) box.className="";
  }});
  document.addEventListener("keydown", function(e){{
    if((e.ctrlKey||e.metaKey) && e.key.toLowerCase()==="k"){{
      e.preventDefault(); window.scrollTo({{top:0,behavior:"smooth"}});
      setTimeout(function(){{input.focus();}},200);
    }}
  }});

  var lv; try{{ lv = localStorage.getItem("lastLevel"); }}catch(e){{}}
  if(lv) document.getElementById("lastVisitText").innerHTML = "上次学到 <b>GESP " + lv + " 级</b>，可以从这里继续。";
}})();
</script>
"""
    return page_shell(f"{SITE_NAME} | GESP · CSP-J/S",
                      "面向 GESP、CSP-J/S 学生的学习工作台，按等级整理学习路线、程序模板、题解与 OJ 资源。",
                      body, "home")


# ---------- 等级页 ----------
def build_level(n):
    kps = LEVELS[n][2]
    kicker = LEVELS[n][0]
    intro_text = LEVELS[n][1]
    colors = ["#5b8def","#7c6bf0","#a56bf0","#d86bc8","#ef6b9c","#ef7b6b","#ef9d6b","#d9a441"]
    bar = colors[n-1]

    side_items = ""
    for i, (t, d, tags) in enumerate(kps, 1):
        side_items += f'<li><a href="#kp{i}"><span class="n">{i:02d}</span><span>{html.escape(t)}</span></a></li>'

    kp_html = ""
    for i, (t, d, tags) in enumerate(kps, 1):
        tag_html = "".join(f"<span>{html.escape(x)}</span>" for x in tags)
        kp_html += f"""
      <div class="kp" id="kp{i}">
        <div class="kp-top">
          <span class="no">{i:02d}</span>
          <span class="badge">官方核心</span>
          <span class="state">未复习</span>
        </div>
        <h4>{html.escape(t)}</h4>
        <p>{html.escape(d)}</p>
        <div class="tags">{tag_html}</div>
        <a class="link-red" href="#kp{i}">查看知识点 →</a>
      </div>"""

    total = len(kps)
    other = "".join(
        f'<a class="row" href="level{i}.html"><span class="tag">{i}级</span>'
        f'<span class="t">GESP {i} 级</span>'
        f'<span class="d">{html.escape(LEVELS[i][0])}</span><span class="go">→</span></a>'
        for i in range(1, 9) if i != n)

    body = f"""
<main class="wide">
<div class="level-layout">
  <aside class="side">
    <div class="side-h">GESP {n} 级总览</div>
    <div class="side-g">{n} 级知识点</div>
    <ul class="side-list">{side_items}</ul>
  </aside>

  <div>
    <div class="lv-hero">
      <div class="crumb"><a href="../index.html">{SITE_NAME}</a> · GESP 分级 · {html.escape(kicker)}</div>
      <h1>GESP {n} 级</h1>
    </div>

    <div class="intro">
      <h2>遇到问题，<br>直接查对应知识点</h2>
      <p>{html.escape(intro_text)}</p>
    </div>

    <div class="progress">
      <div>
        <div class="p-title">本机复习记录</div>
        <div class="p-desc">只记录当前设备上的复习与自测情况，不代表考试成绩。</div>
      </div>
      <div><div class="p-num" id="p1">0/{total}</div><div class="p-lbl">已复习知识点</div></div>
      <div><div class="p-num" id="p2">0/{total}</div><div class="p-lbl">已完成自测</div></div>
      <div><div class="p-num">暂无记录</div><div class="p-lbl">自测正确率</div></div>
    </div>

    <div class="sec-head">
      <h3>{n} 级知识点</h3>
      <span class="hint">共 {total} 个知识点，按官方大纲顺序排列</span>
    </div>
    <div class="kp-grid">{kp_html}</div>

    <section class="sec" style="margin-top:44px">
      <h2>其他等级</h2>
      <p class="sec-sub">切换到其它 GESP 等级继续学习。</p>
      <div class="rows">{other}</div>
    </section>
  </div>
</div>
</main>

<script>
(function(){{
  try{{
    localStorage.setItem("lastLevel", "{n}");
    var seen = JSON.parse(localStorage.getItem("reviewed")||"{{}}");
    var c = (seen["{n}"]||[]).length;
    document.getElementById("p1").textContent = c + "/{total}";
  }}catch(e){{}}
  document.querySelectorAll(".kp").forEach(function(el){{
    el.addEventListener("click", function(){{
      el.querySelector(".state").textContent = "已复习";
      el.querySelector(".state").style.color = "#c0392b";
    }});
  }});
}})();
</script>
"""
    return page_shell(f"GESP {n} 级 | {SITE_NAME}",
                      f"GESP {n} 级知识点整理：{intro_text}",
                      body, "gesp", prefix="../")


# ---------- GESP 总览 ----------
def build_gesp_index():
    colors = ["#5b8def","#7c6bf0","#a56bf0","#d86bc8","#ef6b9c","#ef7b6b","#ef9d6b","#d9a441"]
    cards = ""
    for i in range(1, 9):
        kps = LEVELS[i][2]
        cards += f"""
      <a class="lv-card" href="gesp/level{i}.html" style="--bar:{colors[i-1]}">
        <div class="no">{i:02d}</div>
        <div class="lv" style="color:{colors[i-1]}">{i}级</div>
        <div class="lbl">GESP {i} 级 · {len(kps)} 个知识点</div>
        <div class="desc">{html.escape(LEVELS[i][0])}</div>
      </a>"""

    body = f"""
<main class="wrap" style="padding-top:52px">
  <div class="crumb"><a href="index.html">{SITE_NAME}</a> · GESP 分级</div>
  <section class="sec">
    <h2>GESP 一级至八级</h2>
    <p class="sec-sub">按等级查询知识点，不设访问门槛，可以直接进入任意一级。</p>
    <div class="levels">{cards}</div>
  </section>

  <section class="sec">
    <h2>各级知识点数量</h2>
    <p class="sec-sub">每级覆盖的知识点范围。</p>
    <div class="rows">
      {"".join(f'<a class="row" href="gesp/level{i}.html"><span class="tag">{i}级</span><span class="t">GESP {i} 级</span><span class="d">{html.escape(LEVELS[i][0])} · 共 {len(LEVELS[i][1])} 个知识点</span><span class="go">→</span></a>' for i in range(1,9))}
    </div>
  </section>
</main>
"""
    return page_shell(f"GESP 分级 | {SITE_NAME}", "GESP 一级至八级知识点总览。", body, "gesp")


# ---------- CSP ----------
def build_csp():
    stages = ""
    for no, name, desc, tip, bar in CSP:
        stages += f"""
      <div class="stage" style="--bar:{bar}">
        <div class="no">{no}</div>
        <div class="tip">{html.escape(tip)}</div>
        <h3>{html.escape(name)}</h3>
        <p>{html.escape(desc)}</p>
        <div class="foot"><span class="link-red">查看阶段 →</span></div>
      </div>"""

    rows = ""
    for no, name, desc, tip, bar in CSP:
        rows += f"""
      <a class="row" href="#">
        <span class="tag">{name.split()[0].replace('CSP-','')}</span>
        <span class="t">{html.escape(name)}</span>
        <span class="d">{html.escape(desc)}</span><span class="go">→</span></a>"""

    body = f"""
<main class="wrap" style="padding-top:52px">
  <div class="crumb"><a href="index.html">{SITE_NAME}</a> · CSP-J/S · 按考试阶段查询</div>
  <section class="sec">
    <h1 style="font-size:clamp(30px,5vw,44px);font-weight:800;margin:0 0 14px;letter-spacing:-.02em">
      选择你正在准备的 CSP 阶段</h1>
    <p class="sec-sub" style="max-width:640px">
      初赛、复赛和进阶训练关注的内容不同。先选择你眼下正在准备的阶段，再直接进入对应说明。</p>
    <a class="btn btn-primary" href="#stages">查看三个备考阶段 →</a>
  </section>

  <section class="sec" id="stages">
    <h2>三个备考阶段</h2>
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
    return page_shell(f"CSP-J/S | {SITE_NAME}", "CSP-J 初赛、CSP-J 复赛与 CSP-S 进阶的学习范围。", body, "csp")


# ---------- 程序模板 ----------
def build_templates():
    cards = ""
    for name, desc, tag in TEMPLATES:
        cards += f"""
      <div class="tool-card">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
          <span class="tag" style="font-size:11px;font-weight:700;background:var(--brand-soft);
            color:var(--brand);border-radius:5px;padding:3px 9px">{html.escape(tag)}</span>
        </div>
        <h4>{html.escape(name)}</h4>
        <p>{html.escape(desc)}</p>
        <span class="link-red">打开模板 →</span>
      </div>"""

    body = f"""
<main class="wrap" style="padding-top:52px">
  <div class="crumb"><a href="index.html">{SITE_NAME}</a> · 程序模板 · C++ 代码框架</div>
  <section class="sec">
    <h1 style="font-size:clamp(30px,5vw,44px);font-weight:800;margin:0 0 14px;letter-spacing:-.02em">
      找到可以直接修改的代码框架</h1>
    <p class="sec-sub" style="max-width:640px">
      已经有思路、只是不确定怎么写时，从下面的模板开始，替换关键部分即可。</p>
  </section>

  <section class="sec">
    <h2>常用模板</h2>
    <p class="sec-sub">按类别整理，覆盖竞赛中高频出现的写法。</p>
    <div class="two">{cards}</div>
  </section>

  <section class="sec">
    <h2>基础框架</h2>
    <p class="sec-sub">每个程序都从这里开始。</p>
    <div class="code"><span class="c">// 基础框架 + 快读快写</span>
<span class="k">#include</span> <span class="t">&lt;bits/stdc++.h&gt;</span>
<span class="k">using namespace</span> std;

<span class="k">inline int</span> <span class="f">read</span>() {{
    <span class="k">int</span> x = <span class="t">0</span>, f = <span class="t">1</span>; <span class="k">char</span> c = <span class="f">getchar</span>();
    <span class="k">while</span> (c &lt; <span class="t">'0'</span> || c &gt; <span class="t">'9'</span>) {{ <span class="k">if</span> (c == <span class="t">'-'</span>) f = -<span class="t">1</span>; c = <span class="f">getchar</span>(); }}
    <span class="k">while</span> (c &gt;= <span class="t">'0'</span> &amp;&amp; c &lt;= <span class="t">'9'</span>) {{ x = x * <span class="t">10</span> + c - <span class="t">'0'</span>; c = <span class="f">getchar</span>(); }}
    <span class="k">return</span> x * f;
}}

<span class="k">int</span> <span class="f">main</span>() {{
    <span class="c">// 在这里写主逻辑</span>
    <span class="k">return</span> <span class="t">0</span>;
}}</div>
  </section>

  <section class="sec">
    <h2>并查集</h2>
    <p class="sec-sub">路径压缩 + 按秩合并，接近常数时间。</p>
    <div class="code"><span class="k">int</span> fa[<span class="t">100005</span>], rk[<span class="t">100005</span>];

<span class="k">int</span> <span class="f">find</span>(<span class="k">int</span> x) {{
    <span class="k">while</span> (fa[x] != x) {{ fa[x] = fa[fa[x]]; x = fa[x]; }}
    <span class="k">return</span> x;
}}

<span class="k">void</span> <span class="f">unite</span>(<span class="k">int</span> a, <span class="k">int</span> b) {{
    a = <span class="f">find</span>(a); b = <span class="f">find</span>(b);
    <span class="k">if</span> (a == b) <span class="k">return</span>;
    <span class="k">if</span> (rk[a] &lt; rk[b]) swap(a, b);
    fa[b] = a;
    <span class="k">if</span> (rk[a] == rk[b]) rk[a]++;
}}</div>
  </section>

  <section class="sec">
    <h2>Dijkstra 最短路（堆优化）</h2>
    <p class="sec-sub">适用于非负权图，复杂度 O((n+m) log n)。</p>
    <div class="code"><span class="k">struct</span> Edge {{ <span class="k">int</span> to, w; }};
vector&lt;Edge&gt; g[<span class="t">100005</span>];
<span class="k">int</span> dis[<span class="t">100005</span>];
<span class="k">const int</span> INF = <span class="t">0x3f3f3f3f</span>;

<span class="k">void</span> <span class="f">dijkstra</span>(<span class="k">int</span> s) {{
    memset(dis, <span class="t">0x3f</span>, <span class="k">sizeof</span>(dis));
    priority_queue&lt;pair&lt;<span class="k">int</span>,<span class="k">int</span>&gt;, vector&lt;pair&lt;<span class="k">int</span>,<span class="k">int</span>&gt;&gt;, greater&lt;&gt;&gt; pq;
    dis[s] = <span class="t">0</span>; pq.push({{<span class="t">0</span>, s}});
    <span class="k">while</span> (!pq.empty()) {{
        <span class="k">auto</span> [d, u] = pq.top(); pq.pop();
        <span class="k">if</span> (d &gt; dis[u]) <span class="k">continue</span>;
        <span class="k">for</span> (<span class="k">auto</span> &amp;e : g[u]) {{
            <span class="k">if</span> (dis[e.to] &gt; d + e.w) {{
                dis[e.to] = d + e.w;
                pq.push({{dis[e.to], e.to}});
            }}
        }}
    }}
}}</div>
  </section>

  <section class="sec">
    <h2>01 背包</h2>
    <p class="sec-sub">注意体积从大到小枚举，避免重复选取。</p>
    <div class="code"><span class="k">int</span> dp[<span class="t">100005</span>];

<span class="k">for</span> (<span class="k">int</span> i = <span class="t">1</span>; i &lt;= n; i++)
    <span class="k">for</span> (<span class="k">int</span> j = V; j &gt;= w[i]; j--)
        dp[j] = max(dp[j], dp[j - w[i]] + v[i]);</div>
  </section>
</main>
"""
    return page_shell(f"程序模板 | {SITE_NAME}", "竞赛常用 C++ 代码模板与框架。", body, "tpl")


# ---------- 题解 ----------
def build_solutions():
    cards = ""
    for name, sub, desc in SOLUTIONS:
        cards += f"""
      <div class="tool-card">
        <h4>{html.escape(name)} · {html.escape(sub)}</h4>
        <p>{html.escape(desc)}</p>
        <span class="link-red">查看题解 →</span>
      </div>"""

    body = f"""
<main class="wrap" style="padding-top:52px">
  <div class="crumb"><a href="index.html">{SITE_NAME}</a> · 题解 · 读题、思路与代码映射</div>
  <section class="sec">
    <h1 style="font-size:clamp(30px,5vw,44px);font-weight:800;margin:0 0 14px;letter-spacing:-.02em">
      学习读题、思路与代码的映射</h1>
    <p class="sec-sub" style="max-width:640px">
      按题型整理，重点是「怎么想到的」，而不只是「代码怎么写」。</p>
  </section>

  <section class="sec">
    <h2>按题型查看</h2>
    <p class="sec-sub">先确认题型，再对照该题型的常见突破点。</p>
    <div class="two">{cards}</div>
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

  <section class="sec">
    <h2>常见卡点</h2>
    <p class="sec-sub">对照检查自己的程序。</p>
    <div class="two">
      <div class="tool-card"><h4>程序出错</h4>
        <p>编译错误看第一行报错信息；运行错误先检查数组越界与除以零。</p></div>
      <div class="tool-card"><h4>运行超时</h4>
        <p>先算复杂度是否超过范围，再考虑优化或换算法。</p></div>
      <div class="tool-card"><h4>答案错误</h4>
        <p>用小样例和边界数据对拍，逐个排除逻辑分支。</p></div>
      <div class="tool-card"><h4>格式错误</h4>
        <p>检查空格、换行与末尾多余字符，注意浮点精度。</p></div>
    </div>
  </section>
</main>
"""
    return page_shell(f"题解 | {SITE_NAME}", "信息学竞赛题解与解题思路整理。", body, "sol")


# ---------- OJ 与资源 ----------
def build_resources():
    rows = ""
    for tag, name, desc, url in RESOURCES:
        rows += f"""
      <a class="row" href="{url}" target="_blank" rel="noopener">
        <span class="tag">{tag}</span><span class="t">{name}</span>
        <span class="d">{html.escape(desc)}</span><span class="go">↗</span></a>"""

    body = f"""
<main class="wrap" style="padding-top:52px">
  <div class="crumb"><a href="index.html">{SITE_NAME}</a> · OJ 与资源</div>
  <section class="sec">
    <h2>OJ 与学习资源</h2>
    <p class="sec-sub">进入题库练习，或查阅权威资料。</p>
    <div class="rows">{rows}</div>
  </section>

  <section class="sec">
    <h2>怎么用这些资源</h2>
    <p class="sec-sub">按当前阶段选择，不要一次全都打开。</p>
    <div class="rows">
      <div class="row"><span class="tag">刷题</span><span class="t">按专题刷</span>
        <span class="d">学完一个知识点后，立刻找 3–5 道同类题目巩固</span></div>
      <div class="row"><span class="tag">查漏</span><span class="t">看题解前先自己想</span>
        <span class="d">卡住 20 分钟以上再看题解，效率更高</span></div>
      <div class="row"><span class="tag">复习</span><span class="t">记录错题</span>
        <span class="d">把错因写下来，比反复刷同类型题更有效</span></div>
    </div>
  </section>
</main>
"""
    return page_shell(f"OJ 与资源 | {SITE_NAME}", "常用在线评测平台与学习资料。", body, "res")


# ============ 主流程 ============
def main():
    if os.path.exists(SITE):
        shutil.rmtree(SITE)
    os.makedirs(SITE)

    written = []
    written.append(write_page("index.html", build_home()))
    written.append(write_page("gesp.html", build_gesp_index()))
    written.append(write_page("csp.html", build_csp()))
    written.append(write_page("templates.html", build_templates()))
    written.append(write_page("solutions.html", build_solutions()))
    written.append(write_page("resources.html", build_resources()))
    for n in range(1, 9):
        written.append(write_page(f"gesp/level{n}.html", build_level(n)))

    # .nojekyll
    io.open(os.path.join(SITE, ".nojekyll"), "w").write("")
    total_kp = sum(len(LEVELS[n][1]) for n in range(1, 9))
    print(f"✅ 生成 {len(written)} 个页面")
    print(f"✅ 知识点总数: {total_kp}")
    for w in written:
        print("   ", os.path.relpath(w, ROOT))


if __name__ == "__main__":
    main()
