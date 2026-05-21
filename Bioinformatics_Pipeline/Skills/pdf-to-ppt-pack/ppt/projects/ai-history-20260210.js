const SLIDES = [
    {
        badge: { icon: "*", text: "AI HISTORY" },
        title: { text: "AI的发展历史", gradient: true },
        subtitle: "从符号主义到生成式与智能体",
        clickHint: "时间轴概览",
        elements: [
            {
                step: 1,
                type: "timeline",
                style: "margin-bottom: 2vmin;",
                items: [
                    { activeStep: 1, badge: "1956", icon: "o", title: "起点", desc: "达特茅斯会议提出AI", case: "符号主义" },
                    { activeStep: 1, badge: "1970s", icon: "=", title: "规则推理", desc: "知识表示与逻辑推理", case: "符号系统" },
                    { activeStep: 1, badge: "1980s", icon: "o", title: "专家系统", desc: "商业化落地与成本上升", case: "第一次寒冬" },
                    { activeStep: 1, badge: "2012", icon: "O", iconFilled: true, title: "深度学习突破", desc: "ImageNet带动性能跃升", case: "数据+算力" },
                    { activeStep: 1, badge: "2023", icon: "O", iconFilled: true, title: "生成式大模型", desc: "多模态与对话式模型普及", case: "应用爆发" }
                ]
            }
        ]
    },
    {
        badge: { icon: "+", text: "SYMBOLIC AI" },
        title: { text: "1950s-1970s 符号主义时代" },
        subtitle: "规则驱动的早期方法",
        clickHint: "从规则到瓶颈",
        elements: [
            {
                step: 1,
                type: "comparison",
                style: "width: 90%; margin-bottom: 2vmin;",
                left: {
                    icon: "o",
                    title: "优势",
                    items: [
                        "可解释规则",
                        "可控推理链条",
                        "适合结构化任务"
                    ]
                },
                right: {
                    icon: "O",
                    title: "局限",
                    items: [
                        "知识获取昂贵",
                        "对噪声敏感",
                        "扩展性弱"
                    ]
                }
            },
            {
                step: 2,
                type: "quote",
                style: "border-left: 4px solid var(--accent-coral);",
                text: "规则系统让AI可解释, 但难以处理现实的不确定性",
                author: { icon: "*", text: "阶段总结" }
            }
        ]
    },
    {
        badge: { icon: "#", text: "EXPERT SYSTEMS" },
        title: { text: "1980s-1990s 专家系统与寒冬" },
        subtitle: "商业化高峰后遇到瓶颈",
        clickHint: "结构性挑战",
        elements: [
            {
                step: 1,
                type: "stats",
                style: "margin-bottom: 2vmin;",
                title: "阶段特征",
                items: [
                    { icon: "+", value: "专家系统", label: "在特定领域成功落地" },
                    { icon: "-", value: "高成本", label: "知识工程与维护负担" },
                    { icon: "*", value: "两次寒冬", label: "资金与预期急剧下降" }
                ]
            },
            {
                step: 2,
                type: "assumptions",
                style: "gap: 2vmin;",
                revealStep: 3,
                items: [
                    { old: "X 规则可覆盖复杂世界", new: "-> 现实充满噪声与不确定性" },
                    { old: "X 手工编码可规模化", new: "-> 知识获取成本过高" },
                    { old: "X 硬件足够支撑性能", new: "-> 算力成为限制因素" }
                ]
            }
        ]
    },
    {
        badge: { icon: "@", text: "DATA + COMPUTE" },
        title: { text: "1997-2011 统计学习复兴" },
        subtitle: "数据与算力驱动新突破",
        clickHint: "关键里程碑",
        elements: [
            {
                step: 1,
                type: "timeline",
                style: "margin-bottom: 1.5vmin;",
                items: [
                    { activeStep: 1, badge: "1997", icon: "o", title: "深蓝击败人类", desc: "IBM Deep Blue", case: "算力证明" },
                    { activeStep: 1, badge: "2006", icon: "=", title: "深度学习复兴", desc: "分层表示与无监督预训练", case: "Hinton" },
                    { activeStep: 1, badge: "2009", icon: "o", title: "GPU并行", desc: "大规模训练成为可能", case: "算力拐点" },
                    { activeStep: 1, badge: "2011", icon: "O", iconFilled: true, title: "Watson夺冠", desc: "问答系统验证商业潜力", case: "数据驱动" }
                ]
            },
            {
                step: 2,
                type: "quote",
                style: "background: var(--bg-tertiary);",
                text: "数据规模与算力开始决定AI上限",
                gradient: true,
                author: { icon: "*", text: "趋势判断" }
            }
        ]
    },
    {
        badge: { icon: "*", text: "DEEP LEARNING" },
        title: { text: "2012-2017 深度学习爆发" },
        subtitle: "端到端学习成为主流",
        clickHint: "三大驱动",
        elements: [
            {
                step: 1,
                type: "valueCards",
                style: "margin-bottom: 2vmin;",
                items: [
                    { activeStep: 1, icon: "+", title: "大数据", desc: "ImageNet等数据集提供监督信号" },
                    { activeStep: 2, icon: "=", title: "GPU加速", desc: "并行计算让训练周期大幅缩短" },
                    { activeStep: 3, icon: "O", title: "端到端", desc: "特征学习替代手工设计" }
                ]
            },
            {
                step: 4,
                type: "quote",
                style: "border-left: 4px solid var(--accent-blue);",
                text: "模型结构与训练策略成为性能关键",
                author: { icon: "*", text: "阶段总结" }
            }
        ]
    },
    {
        badge: { icon: "+", text: "TRANSFORMER" },
        title: { text: "2018-2022 预训练与大模型" },
        subtitle: "从任务特定到基础模型",
        clickHint: "范式转移",
        elements: [
            {
                step: 1,
                type: "comparison",
                style: "width: 90%; margin-bottom: 1.5vmin;",
                left: {
                    icon: "o",
                    title: "任务特定模型",
                    items: [
                        "每任务单独训练",
                        "标注成本高",
                        "迁移能力弱"
                    ]
                },
                right: {
                    icon: "O",
                    title: "预训练+微调",
                    items: [
                        "统一语料预训练",
                        "少样本适配",
                        "知识迁移更强"
                    ]
                }
            },
            {
                step: 2,
                type: "timeline",
                style: "margin-bottom: 1vmin;",
                items: [
                    { activeStep: 2, badge: "2018", icon: "o", title: "Transformer/BERT", desc: "自注意力成为核心架构", case: "NLP突破" },
                    { activeStep: 3, badge: "2020", icon: "=", title: "GPT-3", desc: "大规模预训练展现涌现能力", case: "规模效应" },
                    { activeStep: 4, badge: "2022", icon: "O", iconFilled: true, title: "对话式大模型", desc: "人类反馈与对齐技术成熟", case: "应用加速" }
                ]
            },
            {
                step: 5,
                type: "quote",
                style: "background: var(--bg-tertiary);",
                text: "大模型把通用能力带到更多任务场景",
                gradient: true,
                author: { icon: "*", text: "阶段总结" }
            }
        ]
    },
    {
        badge: { icon: ">", text: "GENAI ERA" },
        title: { text: "2023-2026 生成式与智能体" },
        subtitle: "多模态, 工具调用, 协作",
        clickHint: "当前阶段",
        elements: [
            {
                step: 1,
                type: "valueCards",
                style: "margin-bottom: 2vmin;",
                items: [
                    { activeStep: 1, icon: "+", title: "多模态", desc: "文本, 图像, 音频统一表征" },
                    { activeStep: 2, icon: "=", title: "工具调用", desc: "搜索, 代码, 操作系统成为外部手" },
                    { activeStep: 3, icon: "O", title: "智能体协作", desc: "任务分解与多代理协同" }
                ]
            },
            {
                step: 4,
                type: "competitionBox",
                style: "margin-top: 1vmin;",
                title: "关键挑战",
                items: [
                    "对齐与安全",
                    "数据和版权治理",
                    "成本与能效优化",
                    "评测与可靠性"
                ],
                conclusion: "能力提升与治理并行"
            }
        ]
    },
    {
        badge: { icon: "#", text: "SUMMARY" },
        title: { text: "历史脉络与未来焦点" },
        subtitle: "从模型能力到系统能力",
        clickHint: "收束",
        elements: [
            {
                step: 1,
                type: "strategyBox",
                title: "未来十年关注点",
                items: [
                    { type: "wrong", text: "只追逐单一基准分数" },
                    { type: "wrong", text: "忽视数据与工程治理" },
                    { type: "right", text: "模型+系统+治理协同" }
                ],
                final: { arrow: "->", text: "AI竞争从模型战转向系统战" }
            },
            {
                step: 2,
                type: "ending",
                style: "margin-top: 2vmin;",
                icon: "*",
                message: "AI发展是一条长期演化曲线",
                thanks: "THANKS FOR WATCHING"
            }
        ]
    }
];
