/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║                                                                              ║
 * ║   📝 红杉对话 LangChain 创始人：Long-Horizon Agents 元年                        ║
 * ║   2026 年 AI 告别对话框，步入 Long-Horizon Agents 元年                          ║
 * ║                                                                              ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 * 
 * 来源：Sequoia Capital × Harrison Chase (LangChain)
 * 
 * 核心观点：
 * - AI 从 "Talkers" 转向 "Doers"
 * - Long Horizon Agents 具备自主规划、长时运行能力
 * - Harness + 模型协同推动 Agent 能力飞跃
 * - Memory 和 Trace 将成为关键基建
 */

const SLIDES = [
    {
        badge: { icon: "*", text: "SEQUOIA x LANGCHAIN 2026" },
        title: { text: "Long-Horizon Agents", gradient: true },
        subtitle: "AI 告别对话框，步入 Doers 元年",
        clickHint: "点击开启探索",
        elements: [
            {
                step: 1,
                type: "comparison",
                style: "width: 90%; margin-bottom: 2vmin;",
                left: {
                    icon: "o",
                    title: "Talkers 时代",
                    items: [
                        "对话框交互为主",
                        "单轮任务处理",
                        "被动响应用户指令",
                        "短期记忆、即时遗忘"
                    ]
                },
                right: {
                    icon: "O",
                    title: "Doers 时代",
                    items: [
                        "自主规划与执行",
                        "长程任务持续运行",
                        "主动发现与解决问题",
                        "长期记忆、经验积累"
                    ]
                }
            },
            {
                step: 2,
                type: "terminal",
                style: "max-width: 650px; box-shadow: var(--shadow-lg); margin-bottom: 2vmin;",
                content: [
                    { type: "prompt", text: "AGENT_2026 > " },
                    { type: "text", text: "mode = " },
                    { type: "highlight", text: "LONG_HORIZON" },
                    { type: "text", text: " | capabilities = " },
                    { type: "highlight", text: "AUTONOMOUS" },
                    { type: "cursor" }
                ]
            },
            {
                step: 3,
                type: "quote",
                style: "border-left: 4px solid var(--accent-coral);",
                text: "2026年是 AI 从 Talkers 变成 Doers 的元年。",
                textStyle: "font-size: clamp(1.2rem, 2.8vmin, 1.8rem); font-weight: 600;",
                author: { icon: "*", text: "Harrison Chase, LangChain" }
            }
        ]
    },
    {
        badge: { icon: "+", text: "CORE CONCEPT" },
        title: { text: "Long Horizon Agents" },
        subtitle: "自主规划、长时执行的智能体",
        clickHint: "点击了解核心能力",
        elements: [
            {
                step: 1,
                type: "valueCards",
                style: "margin-bottom: 3vmin;",
                items: [
                    { activeStep: 1, icon: "+", title: "自主规划", desc: "独立分解复杂任务 - 制定执行策略 - 动态调整方案" },
                    { activeStep: 2, icon: "-", title: "长时运行", desc: "持续数小时工作 - 异步任务管理 - 断点续接能力" },
                    { activeStep: 3, icon: "*", title: "专家级执行", desc: "编码、SRE、金融 - 复杂工作流处理 - 人机协作场景" }
                ]
            },
            {
                step: 4,
                type: "assumptions",
                style: "gap: 2vmin; margin-bottom: 2vmin;",
                revealStep: 5,
                items: [
                    { old: "X Agent 只能做简单任务", new: "-> 已突破至专家级复杂任务" },
                    { old: "X 必须实时人工监督", new: "-> 自主运行 + 关键点人工介入" },
                    { old: "X 仅限编码领域", new: "-> 快速扩展至各类任务流" }
                ]
            },
            {
                step: 6,
                type: "quote",
                style: "background: var(--bg-tertiary);",
                text: "文件系统权限已成 Agent 标配，Coding Agent 可能是通用 Agent 的终极形态",
                gradient: true,
                author: { icon: "*", text: "Core Insight" }
            }
        ]
    },
    {
        badge: { icon: "#", text: "ARCHITECTURE" },
        title: { text: "Harness：Agent 的软件外壳" },
        subtitle: "有主见的架构设计是性能突破的关键",
        clickHint: "点击解析架构演进",
        elements: [
            {
                step: 1,
                type: "comparison",
                style: "width: 90%; margin-bottom: 2vmin;",
                left: {
                    icon: "[ ]",
                    title: "Framework (无主见)",
                    items: [
                        "通用抽象层",
                        "灵活但松散",
                        "Scaffolding 脚手架",
                        "需要大量定制"
                    ]
                },
                right: {
                    icon: "[x]",
                    title: "Harness (有主见)",
                    items: [
                        "集成 Planning 能力",
                        "内置文件系统操作",
                        "工具管理一体化",
                        "开箱即用高性能"
                    ]
                }
            },
            {
                step: 2,
                type: "timeline",
                style: "margin-bottom: 2vmin;",
                items: [
                    { activeStep: 2, badge: "Layer 1", icon: "o", title: "强力推理模型", desc: "基础智能能力", case: "Claude / GPT-4 / Gemini" },
                    { activeStep: 3, badge: "Layer 2", icon: "=", title: "Harness 外壳", desc: "执行与协调层", case: "LangGraph / 自研框架" },
                    { activeStep: 4, badge: "Layer 3", icon: "O", iconFilled: true, title: "工具 & 环境", desc: "Code Sandbox + CLI", case: "Terminal-Bench 2.0" }
                ]
            },
            {
                step: 5,
                type: "stats",
                items: [
                    { icon: "+", value: "LangGraph", label: "Agent 认知架构核心" },
                    { icon: "*", value: "Bench 2.0", label: "区分模型与 Harness 贡献" },
                    { icon: "#", value: "Coding Co.", label: "Harness 设计领先者" }
                ]
            }
        ]
    },
    {
        badge: { icon: ">", text: "NEW PARADIGM" },
        title: { text: "Agent 构建 ≠ 传统软件" },
        subtitle: "行为依赖模型，需要全新的测试与调试方法",
        clickHint: "点击理解构建差异",
        elements: [
            {
                step: 1,
                type: "assumptions",
                style: "gap: 2vmin; margin-bottom: 3vmin;",
                revealStep: 2,
                items: [
                    { old: "传统：代码完全控制逻辑", new: "Agent：逻辑部分依赖模型输出" },
                    { old: "传统：本地测试即可验证", new: "Agent：需线上测试 + Tracing 监控" },
                    { old: "传统：行为完全可预测", new: "Agent：行为具有概率性、不确定性" },
                    { old: "传统：Debug 靠断点调试", new: "Agent：依赖 Trace 数据复盘分析" }
                ]
            },
            {
                step: 3,
                type: "comparison",
                style: "width: 90%; margin-bottom: 2vmin;",
                left: {
                    icon: "[T]",
                    title: "Tracing 追踪",
                    items: [
                        "Agent 调试的核心数据",
                        "记录完整执行链路",
                        "支持协作与复盘",
                        "在线实时监控"
                    ]
                },
                right: {
                    icon: "[E]",
                    title: "Eval 评估",
                    items: [
                        "人类标注 + LLM 评判",
                        "行为质量评估",
                        "Harness 持续优化",
                        "自我改进闭环"
                    ]
                }
            },
            {
                step: 4,
                type: "quote",
                style: "border-left: 4px solid var(--accent-coral);",
                text: "构建 Agent 的核心难点：Context 压缩、Sub-agent 协调、Prompt 设计",
                author: { icon: "*", text: "Key Challenges" }
            }
        ]
    },
    {
        badge: { icon: "@", text: "MEMORY & UX" },
        title: { text: "Memory：Agent 的核心壁垒" },
        subtitle: "长期记忆与 Hybrid 交互模式",
        clickHint: "点击探索未来交互",
        elements: [
            {
                step: 1,
                type: "valueCards",
                style: "margin-bottom: 3vmin;",
                items: [
                    { activeStep: 1, icon: "+", title: "长期记忆", desc: "交互学习积累 - 经验持久化 - 形成竞争壁垒" },
                    { activeStep: 2, icon: "-", title: "异步执行", desc: "后台长时运行 - 任务队列管理 - 无需持续关注" },
                    { activeStep: 3, icon: "*", title: "同步协作", desc: "关键决策介入 - 实时反馈调整 - 人机高效配合" }
                ]
            },
            {
                step: 4,
                type: "competitionBox",
                style: "margin-top: 2vmin;",
                title: "Hybrid Mode：异步与同步的无缝结合",
                items: [
                    "异步：复杂任务后台自主执行",
                    "同步：关键节点实时人机协作",
                    "记忆：跨会话经验持续积累"
                ],
                conclusion: "Memory > 单次能力"
            },
            {
                step: 5,
                type: "quote",
                style: "background: var(--bg-tertiary);",
                text: "Memory 将成为 Agent 持续提升的基础，是最重要的发展方向",
                gradient: true,
                author: { icon: "*", text: "Future Direction" }
            }
        ]
    },
    {
        badge: { icon: "*", text: "CONCLUSION" },
        title: { text: "2026：Agent 新纪元" },
        subtitle: "自主化、协作化、高效智能",
        clickHint: "点击查看未来图景",
        elements: [
            {
                step: 1,
                type: "timeline",
                style: "margin-bottom: 2vmin;",
                items: [
                    { activeStep: 1, badge: "Now", icon: "O", iconFilled: true, title: "Long Horizon Agents", desc: "自主规划长时执行", case: "Doers时代开启" },
                    { activeStep: 2, badge: "Next", icon: "=", title: "Harness + 模型协同", desc: "能力飞跃式提升", case: "Coding Agent 引领" },
                    { activeStep: 3, badge: "Future", icon: "o", title: "Memory 基建成熟", desc: "持续学习与进化", case: "通用 Agent 雏形" }
                ]
            },
            {
                step: 4,
                type: "strategyBox",
                style: "margin-top: 2vmin; border: 1px solid var(--border-strong);",
                title: "Agent 时代的核心基建",
                items: [
                    { type: "right", text: "Trace：调试与协作的关键数据" },
                    { type: "right", text: "Eval：行为评估与自我改进" },
                    { type: "right", text: "Memory：长期记忆与竞争壁垒" }
                ],
                final: { arrow: "->", text: "Coding Agent 可能是通用智能的基石" }
            },
            {
                step: 5,
                type: "ending",
                style: "margin-top: 3vmin;",
                icon: "*",
                message: "从对话框到自主执行，AI 应用的新篇章",
                thanks: "THANKS FOR WATCHING"
            }
        ]
    }
];
