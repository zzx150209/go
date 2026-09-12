# rickroll-site

打开即跳转到 B 站 Rickroll 视频的极简跳转页，用于绑定自己的域名。

## 文件

- `index.html` — 唯一的页面，落地即 `location.replace` 跳转
- `.nojekyll` — 让 GitHub Pages 跳过 Jekyll 处理

## 本地预览

```bash
cd rickroll-site
python3 -m http.server 8080
# 浏览器打开 http://localhost:8080
```

## 部署到 GitHub Pages

```bash
cd rickroll-site
git init
git add .
git commit -m "rickroll redirect"
git branch -M main
git remote add origin https://github.com/<你的用户名>/<仓库名>.git
git push -u origin main
```

然后到仓库 **Settings → Pages**，Source 选 `Deploy from a branch`，Branch 选 `main` / `root`，保存。
等 1–2 分钟，访问 `https://<你的用户名>.github.io/<仓库名>/` 验证跳转。

## 绑定自己的域名

1. 仓库 **Settings → Pages → Custom domain** 填入你的域名，保存（会在仓库根目录生成 `CNAME` 文件）
2. 到域名商 DNS 后台添加记录：
   - 根域名（如 `example.com`）：4 条 A 记录 → `185.199.108.153`、`185.199.109.153`、`185.199.110.153`、`185.199.111.153`
   - `www`：1 条 CNAME → `<你的用户名>.github.io`
3. 回到 Pages 页面，等 DNS 检查通过后勾选 **Enforce HTTPS**

## 注意事项

- 微信 / QQ 内置浏览器可能拦截自动跳转，页面留了「点击继续」兜底
- 短域名 + 立即跳转到外部站，部分浏览器或插件可能给出安全提示，属正常现象
