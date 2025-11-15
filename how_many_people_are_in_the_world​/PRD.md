# 「全球人口数量」工具 PRD

## 1. 项目背景
- 站点主导航覆盖单位换算与百科问答，此问题搜索量高且具时效性。
- 现有文件夹为空，未提供可访问内容，影响导航完整性、SEO 与分享功能。

## 2. 产品目标与指标
- T+1 发布可访问的单页工具，含全球人口实时估算、增速描述与常见问答。
- 页面首屏 LCP < 2.5s（桌面），CLS < 0.1。
- 通过导航生成脚本新增 1 条 `how_many_people_are_in_the_world` 数据，分享组件启用率 100%。

## 3. 核心用户场景
1. **学生/创作者**：快速引用最新人口数据和增长速度。
2. **普通用户**：获得一个清晰的“当前人口+可视化”答案，并可复制或分享。
3. **媒体/运营**：需要简单的地区对比与来源链接以便嵌入报道。

## 4. 功能需求
1. 顶部数卡：显示“全球人口即时估算”，数字每秒刷新（基于年增长率换算）。
2. 信息模块：
   - 当年人口、去年人口、年增长率、每日新增人口估算。
   - 三段式解读：影响因素、联合国预测、数据更新时间（UTC）。
3. 数据可视化：简单的微型柱状图或条形图展示 2015-2030 的预测数据（静态 JSON）。
4. FAQ：至少 3 条（例如“人口如何计算”“人口最多的国家”）。
5. CTA：分享按钮（调用 `share-utils.js`）与“复制数据”功能。
6. SEO：Title、Meta、Schema（WebApplication + FAQPage），支持 OG/Twitter 卡片。
7. 无障碍：语义化标签、数字朗读、对比度 ≥ 4.5:1。

## 5. 数据与算法
- 数据源：联合国《World Population Prospects 2024》+ Worldometer 实时估算。
- 计算逻辑：
  - 设基准人口 `P0`（2024-07-01），年增长率 `r`。
  - 实时人口 `P(t) = P0 * (1 + r)^(t/365)`，`t` 为距基准日的天数。
  - 每秒增量 = `P(t) * r / (365*24*3600)`，用于数字滚动。
- 数据文件：在该文件夹新增 `population-data.json` 存储 `P0`、`r`、预测数组。

## 6. 界面与交互
1. 视觉延续 iOS 高级灰风格，主色 `--ios-blue`，大号数字卡片置中。
2. 数卡下方提供“刷新到当前时间”按钮，点击重置计时器。
3. FAQ 折叠组件，移动端展示为手风琴，默认展开第一条。
4. 图表可使用纯 CSS/Canvas 迷你条形图，保障无依赖。

## 7. 技术实现
- 复用全站模板：`<main class="calculator-card">`。
- 引入 `share-utils.js`、`share-section`；文案：`"I just checked today's world population!"`。
- JavaScript 结构：
  - `fetch('population-data.json')` → 初始化状态。
  - `updatePopulation()` 每秒更新 DOM，使用 `requestAnimationFrame` 平滑过渡。
  - `renderForecastChart(data)` 生成小图（SVG/CSS）。
- 需在 `navigation_generator.py` 扫描后自动写入导航与 sitemap。

## 8. 里程碑
- D0：补齐 `population-data.json` 与 PRD（当前文档）。
- D1：完成 `index.html` 初版 + 桌/移动端样式。
- D2：整合分享组件与 FAQ Schema，完成手工测试（含 `test-sharing.html`）。
- D3：运行 `python3 navigation_generator.py`、`python3 sitemap_generator.py`，提交发布。

## 9. 风险与依赖
- **数据可信度**：需明确引用并在页脚加来源链接。
- **实时刷新性能**：数字过快可能导致移动端掉帧，需节流至 250ms 更新。
- **命名与路径**：目录包含零宽字符，脚本操作时必须从 `navigation_generator.py` 输出的 `folder_name` 复制，避免重复目录。
