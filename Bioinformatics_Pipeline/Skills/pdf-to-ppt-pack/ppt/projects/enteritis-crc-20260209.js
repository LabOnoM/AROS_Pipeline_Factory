const SLIDES = [
  {
    badge: { icon: "*", text: "MEDICAL BRIEF" },
    title: { text: "肠炎与结直肠癌" },
    subtitle: "从慢性炎症到肿瘤发生的风险链路与干预要点",
    clickHint: "2026.02.09",
    elements: [
      {
        step: 1,
        type: "quote",
        style: "border-left: 4px solid var(--accent-green);",
        text: "慢性炎症不是背景噪声，而是肿瘤演化的信号。",
        author: { icon: "-", text: "临床核心观点" }
      }
    ]
  },
  {
    badge: { icon: "■", text: "RISK & BURDEN" },
    title: { text: "风险与负担" },
    elements: [
      {
        step: 1,
        type: "stats",
        title: "慢性炎症驱动的关键特征",
        items: [
          { icon: "●", value: "长期炎症", label: "持续损伤与修复" },
          { icon: "■", value: "风险升高", label: "高危人群需随访" },
          { icon: "▲", value: "可预防", label: "早筛可显著降低负担" }
        ]
      }
    ]
  },
  {
    badge: { icon: "▲", text: "PATHWAY" },
    title: { text: "炎症到癌变的关键路径" },
    elements: [
      {
        step: 1,
        type: "timeline",
        style: "margin-bottom: 2vmin;",
        items: [
          { activeStep: 1, badge: "1", icon: "●", title: "炎症激活", desc: "免疫因子持续释放", case: "屏障稳态被打破" },
          { activeStep: 2, badge: "2", icon: "●", title: "上皮损伤", desc: "反复修复与异常增殖", case: "细胞周期失衡" },
          { activeStep: 3, badge: "3", icon: "●", title: "不典型增生", desc: "组织结构和基因异常累积", case: "癌前病变形成" },
          { activeStep: 4, badge: "4", icon: "●", title: "癌变进程", desc: "侵袭与转移风险增加", case: "临床结直肠癌" }
        ]
      },
      {
        step: 2,
        type: "quote",
        style: "background: var(--bg-tertiary);",
        text: "控制炎症强度与持续时间，是阻断演化路径的关键。",
        gradient: true,
        author: { icon: "*", text: "干预逻辑" }
      }
    ]
  },
  {
    badge: { icon: "◆", text: "MICRO-ENV" },
    title: { text: "健康屏障 vs 炎症微环境" },
    elements: [
      {
        step: 1,
        type: "comparison",
        style: "width: 90%; margin-bottom: 2vmin;",
        left: {
          icon: "○",
          title: "健康肠道",
          items: [
            "屏障完整，黏膜稳态",
            "菌群多样性高",
            "免疫反应可控"
          ]
        },
        right: {
          icon: "●",
          title: "炎症肠道",
          items: [
            "屏障破坏，慢性渗漏",
            "菌群失衡与致炎因子",
            "促增殖信号持续"
          ]
        }
      }
    ]
  },
  {
    badge: { icon: "●", text: "WARNING" },
    title: { text: "高危信号与人群" },
    elements: [
      {
        step: 1,
        type: "valueCards",
        style: "margin-bottom: 2vmin;",
        items: [
          { activeStep: 1, icon: "1", title: "症状警示", desc: "持续腹痛、便血、体重下降" },
          { activeStep: 2, icon: "2", title: "高危人群", desc: "炎症性肠病病程长、家族史" },
          { activeStep: 3, icon: "3", title: "检查提示", desc: "肠镜发现不典型增生或息肉" },
          { activeStep: 4, icon: "4", title: "系统风险", desc: "免疫抑制或代谢异常叠加" }
        ]
      }
    ]
  },
  {
    badge: { icon: "▲", text: "SURVEILLANCE" },
    title: { text: "监测与早筛策略" },
    elements: [
      {
        step: 1,
        type: "timeline",
        style: "margin-bottom: 2vmin;",
        items: [
          { activeStep: 1, badge: "A", icon: "●", title: "风险评估", desc: "病程、家族史、炎症控制水平", case: "分层管理" },
          { activeStep: 2, badge: "B", icon: "●", title: "肠镜筛查", desc: "可视化评估 + 靶向活检", case: "明确病变" },
          { activeStep: 3, badge: "C", icon: "●", title: "随访节奏", desc: "基于风险等级设定频率", case: "避免遗漏" },
          { activeStep: 4, badge: "D", icon: "●", title: "动态调整", desc: "根据病情变化优化方案", case: "持续优化" }
        ]
      }
    ]
  },
  {
    badge: { icon: "■", text: "INTERVENTION" },
    title: { text: "干预重点：炎症控制 + 癌变预防" },
    elements: [
      {
        step: 1,
        type: "comparison",
        style: "width: 88%; margin-bottom: 2vmin;",
        left: {
          icon: "●",
          title: "炎症控制",
          items: [
            "规范药物管理",
            "监测病情活动度",
            "减少反复急性发作"
          ]
        },
        right: {
          icon: "▲",
          title: "癌变预防",
          items: [
            "早筛与切除可疑病灶",
            "生活方式干预",
            "长期随访与风险再评估"
          ]
        }
      },
      {
        step: 2,
        type: "quote",
        style: "background: var(--bg-tertiary);",
        text: "预防不是单点动作，而是贯穿病程的长期策略。",
        author: { icon: "*", text: "临床行动共识" }
      }
    ]
  },
  {
    badge: { icon: "*", text: "SUMMARY" },
    title: { text: "结论与行动" },
    elements: [
      {
        step: 1,
        type: "ending",
        style: "margin-top: 2vmin;",
        icon: "*",
        message: "抓住炎症管理、风险分层、持续随访三条主线，\n把结直肠癌风险前移到可控阶段。",
        thanks: "THANKS"
      }
    ]
  }
];
