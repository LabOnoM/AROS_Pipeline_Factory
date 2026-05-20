/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║                                                                              ║
 * ║   * 幻灯片内容配置文件                                                        ║
 * ║   修改演示内容请编辑此文件！                                                    ║
 * ║                                                                              ║
 * ║   版本: v1.4.1                                                               ║
 * ║   更新日期: 2026-01-29                                                       ║
 * ║   关联文档: 思路/文档/4页动态PPT设计.md (v1.3.1)                             ║
 * ║                                                                              ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 * 
 * 基本配置：
 * - badge: 顶部徽章 { icon, text }
 * - title: 标题 { text, gradient? }
 * - subtitle: 副标题（可选）
 * - clickHint: 底部提示文字（可选）
 * - defaultAnimation: 本页所有元素的默认动画（可选）
 * - elements: 内容元素数组，每个元素需要指定 step 和 type
 * 
 * 可用组件类型：
 * - comparison: 对比卡片
 * - terminal: 终端代码块
 * - quote: 引用块
 * - assumptions: 假设网格
 * - timeline: 时间线
 * - stats: 统计数字
 * - valueCards: 价值卡片
 * - competitionBox: 竞争分析框
 * - strategyBox: 战略框
 * - ending: 结束页
 * 
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║   * 动画配置                                                                 ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 * 
 * 优先级：element.animation > slide.defaultAnimation > 组件默认动画
 * 
 * 动画预设（preset）：
 * - fadeIn:     淡入
 * - slideUp:    从下方滑入（默认）
 * - slideDown:  从上方滑入
 * - slideLeft:  从右侧滑入
 * - slideRight: 从左侧滑入
 * - scaleIn:    缩放进入
 * - zoomIn:     放大进入
 * - flipIn:     翻转进入
 * 
 * 配置方式：
 * 
 * 1. Slide 级别（本页所有元素默认）:
 *    {
 *        defaultAnimation: { preset: 'slideUp', duration: 500 },
 *        elements: [...]
 *    }
 * 
 * 2. Element 级别（单个元素）:
 *    { step: 1, type: "quote", animation: { preset: "scaleIn", duration: 800, delay: 200 } }
 * 
 * 3. 简写形式:
 *    { step: 1, type: "quote", animation: "scaleIn" }
 * 
 * 可配置参数：
 * - preset:   动画预设名称
 * - duration: 动画时长（毫秒）
 * - delay:    动画延迟（毫秒）
 * - easing:   缓动函数（如 "ease-out", "cubic-bezier(0.4, 0, 0.2, 1)"）
 * - stagger:  列表项依次延迟间隔（毫秒，仅对 timeline/valueCards/stats 等列表组件有效）
 */

const SLIDES = [
    {
        badge: { icon: "*", text: "HELIXLIFE 2026" },
        title: { text: "范式转移" },
        subtitle: "从石油价值演变历史带来的启示",
        author: "by JS",
        clickHint: "2026.1.30",
        defaultAnimation: { preset: "slideUp", duration: 500, easing: "ease-out" },
        elements: [
            // 步骤1：石油历史 - 图片 + 时间线
            {
                step: 1,
                type: "image",
                hideStep: 2,
                style: "margin-top: 10vmin; margin-bottom: 1.5vmin;",
                layout: "grid",
                columns: 3,
                images: [
                    { src: "../../work_dir/resources/images/kerosene_lamp_era/9_z-image_00121_.png", title: "煤油灯时代" },
                    { src: "../../work_dir/resources/images/electric_light_revolution/9_z-image_00122_.png", title: "电灯革命" },
                    { src: "../../work_dir/resources/images/rise_of_automobiles/9_z-image_00123_.png", title: "汽车崛起" }
                ]
            },
            {
                step: 1,
                type: "timeline",
                hideStep: 3,
                style: "margin-bottom: 1vmin;",
                items: [
                    { activeStep: 1, badge: "1", icon: "○", title: "1853 煤油提炼", desc: "照明燃料时代", case: "替代了鲸油" },
                    { activeStep: 1, badge: "2", icon: "◐", title: "1879 电灯发明", desc: "煤油需求骤降", case: "再次变垃圾" },
                    { activeStep: 1, badge: "3", icon: "●", title: "1886 汽车普及", desc: "汽油需求激增", case: "新需求涌现" }
                ]
            },
            // 步骤2：对比总结 - 对比卡片
            {
                step: 2,
                type: "comparison",
                hideStep: 3,
                style: "width: 85%; margin-bottom: 1vmin;",
                left: {
                    icon: "+",
                    title: "原有问题与方案",
                    items: [
                        "照明问题 → 鲸油方案（被煤油替代）",
                        "照明问题 → 煤油方案（被电灯淘汰）",
                        "运输问题 → 马车方案（被汽车淘汰）"
                    ]
                },
                right: {
                    icon: "*",
                    title: "新方案的优势",
                    items: [
                        "煤油方案 → 更便宜、更易获取（相比鲸油）",
                        "电灯方案 → 更安全、更明亮、无需燃料（相比煤油）",
                        "汽车方案 → 更快、更远、更可靠（相比马车）",
                        "核心启示：解决原有问题的方案失去价值"
                    ]
                }
            },
            // 步骤3：核心洞察
            {
                step: 3,
                type: "quote",
                style: "border-left: 4px solid var(--accent-coral); margin-bottom: 1vmin;",
                text: "不是原来路径的缓慢升级，而是快速彻底的替代",
                author: { icon: "——", text: "石油的故事告诉我们" }
            },
            // 步骤4：范式转移定义 - 终端
            {
                step: 4,
                type: "terminal",
                style: "max-width: 650px; box-shadow: var(--shadow-lg);",
                content: [
                    { type: "prompt", text: "PARADIGM_SHIFT > " },
                    { type: "text", text: "范式转移 = " },
                    { type: "highlight", text: "旧假设被打破" },
                    { type: "text", text: " + " },
                    { type: "highlight", text: "问题被重定义" },
                    { type: "text", text: " + " },
                    { type: "highlight", text: "新需求涌现" },
                    { type: "text", text: " + " },
                    { type: "highlight", text: "旧方案失效" },
                    { type: "cursor" },
                    { type: "text", text: "\n\n关键要素：基本假设变化" }
                ]
            },
            // 步骤5：过渡到AI时代
            {
                step: 5,
                type: "quote",
                style: "background: var(--bg-tertiary); border-left: 4px solid var(--accent-blue);",
                text: "2026，AI正在打破哪些基本假设？",
                gradient: true,
                author: { icon: "→", text: "" }
            }
        ]
    },
    {
        badge: { icon: "*", text: "BREAKING LIMITS" },
        title: { text: "AI：打破\"自动化\"边界" },
        clickHint: "唯一的限制是想象力",
        elements: [
            {
                step: 1,
                type: "assumptions",
                style: "gap: 2.5vmin; margin-bottom: 3vmin;",
                revealStep: 2,
                items: [
                    { old: "X 科研制图无法自动化", new: "-> 生成式AI实现科研制图自动化（Nano Banana Pro）" },
                    { old: "X 代码编写无法自动化", new: "-> 生成式AI实现代码自动生成（GitHub Copilot、Claude Code、Cursor）" },
                    { old: "X 配音服务无法自动化", new: "-> 生成式AI实现配音自动化（AI语音合成、语音克隆，从50-200元/分钟降至4元/10分钟）" },
                    { old: "X 内容生产无法自动化", new: "-> 生成式AI实现内容自动生成（小红书图文笔记，从2-3小时/篇缩短至2分钟/10篇）" }
                ]
            },
            {
                step: 3,
                type: "quote",
                style: "background: var(--bg-tertiary);",
                text: "当假设被打破，边界即成为新的起跑线",
                gradient: true,
                author: { icon: "*", text: "The New Reality" }
            }
        ]
    },
    {
        badge: { icon: "+", text: "SKILLS ERA" },
        title: { text: "2026：Skills" },
        subtitle: "AI产品范式转移",
        clickHint: "价值的变迁",
        elements: [
            // Step 1: Skills介绍 - 对比展示
            {
                step: 1,
                type: "comparison",
                hideStep: 2,
                style: "width: 90%; margin-bottom: 1.5vmin;",
                left: {
                    icon: "○",
                    title: "以前的AI",
                    items: [
                        "要写提示词",
                        "要选知识库",
                        "要搭工作流"
                    ]
                },
                right: {
                    icon: "●",
                    title: "Agent + Skills",
                    items: [
                        "自动找提示词",
                        "自动选知识库",
                        "自动搭工作流"
                    ]
                }
            },
            {
                step: 1,
                type: "quote",
                hideStep: 2,
                style: "background: var(--bg-tertiary); max-width: 70%;",
                text: "Skills：Anthropic 2025年10月推出，已成行业标准",
                author: { icon: "→", text: "人人都有个JAVIS成为可能" }
            },
            // Step 2: 演进主线 - 趋势展示
            {
                step: 2,
                type: "stats",
                hideStep: 3,
                style: "margin-bottom: 2vmin;",
                title: "2023～2025 AI产品演进主线",
                items: [
                    { icon: "↑", value: "大模型能力", label: "Model Capability" },
                    { icon: "↓", value: "使用成本", label: "Usage Cost" },
                    { icon: "→", value: "套壳应用", label: "Wrapper Apps" }
                ]
            },
            {
                step: 2,
                type: "quote",
                hideStep: 3,
                style: "background: var(--bg-tertiary);",
                text: "每个阶段都是一次范式转移——把前一阶段的核心工作自动化",
                author: { icon: "→", text: "四个阶段演进" }
            },
            // Step 3-6: 四阶段时间线
            {
                step: 3,
                type: "timeline",
                hideStep: 7,
                style: "margin-bottom: 2vmin;",
                items: [
                    { 
                        activeStep: 3, 
                        badge: "2023", 
                        icon: "1", 
                        title: "大模型即产品", 
                        desc: "实现：newidea应用", 
                        case: "打破「可用的AI需要训练」→ 怎么写提示词" 
                    },
                    { 
                        activeStep: 4, 
                        badge: "2024", 
                        icon: "2", 
                        title: "RAG即产品", 
                        desc: "实现：deepseek+pubmed", 
                        case: "打破「需要写提示词」→ 怎么搭建知识库" 
                    },
                    { 
                        activeStep: 5, 
                        badge: "2025", 
                        icon: "3", 
                        title: "工作流即产品", 
                        desc: "实现：monica、pollo、newidea工作台", 
                        case: "打破「需要选知识库」→ 怎么搭建工作流" 
                    },
                    { 
                        activeStep: 6, 
                        badge: "2026", 
                        badgeCurrent: true, 
                        icon: "★", 
                        iconFilled: true, 
                        title: "Coding Agent即产品", 
                        desc: "实现：opencode、clawdbot、一体机", 
                        case: "打破「需要手动搭建工作流」→ 怎么搭建skills" 
                    }
                ]
            },
            // Step 7: 科研技能
            {
                step: 7,
                type: "valueCards",
                hideStep: 9,
                style: "margin-bottom: 2vmin;",
                items: [
                    { activeStep: 7, icon: "1", title: "选题调研", desc: "文献检索 · 热点追踪 · 可行性分析" },
                    { activeStep: 7, icon: "2", title: "研究设计", desc: "实验方案 · 统计规划 · 对照设置" },
                    { activeStep: 7, icon: "3", title: "数据分析", desc: "统计建模 · 可视化 · 结果解读" },
                    { activeStep: 7, icon: "4", title: "学术写作", desc: "论文撰写 · 图表制作 · 投稿润色" }
                ]
            },
            // Step 8: 核心结论
            {
                step: 8,
                type: "quote",
                hideStep: 9,
                style: "background: var(--bg-tertiary);",
                text: "AI产品的竞争，演进到\"谁给Agent配的skills更好\"(大家都是套壳)",
                gradient: true,
                author: { icon: "*", text: "解螺旋的战略：把科研技能做成世界一流的skills" }
            },
            // Step 9: 过渡
            {
                step: 9,
                type: "quote",
                style: "background: var(--bg-secondary); border-left: 4px solid var(--accent-coral);",
                text: "当所有事情都能自动化的时候，什么是不能被自动化的？",
                gradient: true,
                author: { icon: "→", text: "于是问题就来了..." }
            }
        ]
    },
    {
        badge: { icon: "*", text: "HUMAN VALUE" },
        title: { text: "不变" },
        subtitle: "当所有事情都能自动化",
        clickHint: "什么是不能被自动化的？",
        elements: [
            // Step 1: 人类核心价值答案
            {
                step: 1,
                type: "quote",
                hideStep: 2,
                style: "background: var(--bg-secondary); border-left: 4px solid var(--accent-coral);",
                text: "不可自动化的核心人类特质，是为事物赋予独特意义的能力",
                author: { icon: "*", text: "The Answer" }
            },
            // Step 2: 三种人类角色
            {
                step: 2,
                type: "valueCards",
                hideStep: 4,
                style: "margin-bottom: 2vmin;",
                items: [
                    { activeStep: 2, icon: "1", title: "意义发现者", desc: "定义为什么 · 编织叙事 · 建立深层链接" },
                    { activeStep: 2, icon: "2", title: "责任承担者", desc: "伦理裁决 · 风险把控 · 最终决策背书" },
                    { activeStep: 2, icon: "3", title: "体验承载者", desc: "情感共振 · 审美直觉 · 创造独特记忆" }
                ]
            },
            // Step 3: 新新范式（未来竞争方向）
            {
                step: 3,
                type: "competitionBox",
                hideStep: 4,
                style: "margin-top: 1vmin;",
                title: "当所有人都有全自动工厂后，竞争将变成：",
                items: [
                    "谁拥有最具魅力的品牌故事",
                    "谁设计出独一无二且情感共鸣的产品",
                    "谁能围绕产品构建充满意义的社区",
                    "谁能解决工厂本身解决不了的问题"
                ],
                conclusion: "意义 (Meaning) > 效率 (Efficiency)"
            },
            // Step 4: 回到石油的问题
            {
                step: 4,
                type: "comparison",
                hideStep: 5,
                style: "width: 85%; margin-bottom: 1.5vmin;",
                left: {
                    icon: "◇",
                    title: "石油的价值形态",
                    items: [
                        "煤油 → 汽油 → ...",
                        "（快速变化中）"
                    ]
                },
                right: {
                    icon: "◆",
                    title: "AI的价值形态",
                    items: [
                        "提示词 → 知识库 → Skills → ...",
                        "（快速变化中）"
                    ]
                }
            },
            {
                step: 4,
                type: "quote",
                hideStep: 5,
                style: "background: var(--bg-tertiary); border-left: 4px solid var(--accent-coral);",
                text: "追逐\"当前有价值的形态\"是徒劳的——今天的煤油就是明天的垃圾",
                author: { icon: "——", text: "范式快速变化阶段" }
            },
            // Step 5: 解螺旋战略核心
            {
                step: 5,
                type: "strategyBox",
                hideStep: 6,
                title: "解螺旋的战略选择",
                items: [
                    { type: "wrong", text: "追逐某个具体形态（提示词/知识库/Skills...）" },
                    { type: "right", text: "抓住范式转移后涌现的新需求" }
                ],
                final: {
                    arrow: "→",
                    text: "我们教人用AI做科研"
                }
            },
            // Step 6: 竞争关键三要素
            {
                step: 6,
                type: "stats",
                hideStep: 8,
                style: "margin-bottom: 2vmin;",
                title: "竞争关键是什么？",
                items: [
                    { icon: "→", value: "快", label: "以酸谈直播周为单位" },
                    { icon: "◎", value: "准", label: "数据飞轮驱动" },
                    { icon: "↓", value: "多", label: "覆盖目标用户的各种需求" }
                ]
            },
            // Step 7: 核心结论
            {
                step: 7,
                type: "quote",
                hideStep: 8,
                style: "background: var(--bg-tertiary); font-size: 1.2em;",
                gradient: true,
                text: "劳博：\n\n\"通量解决概率问题\"",
                author: { icon: "*", text: "解螺旋核心战略" }
            },
            // Step 8: 结束页
            {
                step: 8,
                type: "ending",
                style: "margin-top: 3vmin;",
                icon: "*",
                message: "从范式转移到不变的价值\n快速跟上变化，抓住新需求",
                thanks: "THANKS FOR WATCHING"
            }
        ]
    }
];
