const SLIDES = [
  {
    badge: { icon: "*", text: "CLINICAL BRIEF" },
    title: { text: "骨关节炎的临床治疗" },
    subtitle: "以疼痛控制、功能改善与疾病进展管理为核心",
    clickHint: "2026.02.09",
    elements: [
      {
        step: 1,
        type: "quote",
        style: "border-left: 4px solid var(--accent-green);",
        text: "骨关节炎治疗的核心目标不是“治愈”，而是延缓进展并提升生活质量。",
        author: { icon: "-", text: "治疗原则" }
      },
      {
        step: 2,
        type: "quote",
        style: "background: var(--bg-tertiary);",
        text: "治疗策略应围绕疼痛缓解、功能恢复与长期管理三条主线展开。随着病程推进，治疗目标从“缓解症状”逐渐转向“结构保护与风险控制”。不同人群对治疗手段的耐受性差异显著，需强调个体化路径。",
        author: { icon: "*", text: "概述" }
      }
    ]
  },
  {
    badge: { icon: "■", text: "BURDEN" },
    title: { text: "疾病负担与临床需求" },
    elements: [
      {
        step: 1,
        type: "stats",
        title: "临床上需要被持续关注的三件事",
        items: [
          { icon: "●", value: "慢性进展", label: "症状波动但趋势上行" },
          { icon: "■", value: "功能受限", label: "关节活动与日常能力下降" },
          { icon: "▲", value: "高龄人群", label: "共病增加管理复杂度" }
        ]
      },
      {
        step: 2,
        type: "quote",
        style: "background: var(--bg-tertiary);",
        text: "临床需求不仅在于止痛，还包括维持活动能力与减少并发风险。高龄与合并代谢性疾病常使治疗选择受限。对患者而言，功能与生活质量的改善往往比影像学指标更具意义。",
        author: { icon: "*", text: "需求解读" }
      }
    ]
  },
  {
    badge: { icon: "▲", text: "PATHWAY" },
    title: { text: "病理进展与治疗窗口" },
    elements: [
      {
        step: 1,
        type: "timeline",
        style: "margin-bottom: 2vmin;",
        items: [
          { activeStep: 1, badge: "1", icon: "●", title: "软骨退变", desc: "基质降解与细胞凋亡", case: "早期结构改变" },
          { activeStep: 2, badge: "2", icon: "●", title: "滑膜炎症", desc: "炎症因子驱动疼痛", case: "症状加重" },
          { activeStep: 3, badge: "3", icon: "●", title: "骨下硬化", desc: "力学负荷异常", case: "进展加速" },
          { activeStep: 4, badge: "4", icon: "●", title: "结构塌陷", desc: "关节间隙明显变窄", case: "功能受限" }
        ]
      },
      {
        step: 2,
        type: "quote",
        style: "background: var(--bg-tertiary);",
        text: "治疗窗口存在于“症状驱动与结构损伤”之间的过渡期。早期以生活方式与非药物干预为主，中期强调药物与注射治疗，晚期则更多依赖手术介入。识别进展阶段可提升治疗效率与安全性。",
        author: { icon: "*", text: "窗口提示" }
      }
    ]
  },
  {
    badge: { icon: "◆", text: "DIAGNOSIS" },
    title: { text: "诊断与分级依据" },
    elements: [
      {
        step: 1,
        type: "comparison",
        style: "width: 90%; margin-bottom: 2vmin;",
        left: {
          icon: "○",
          title: "临床评估",
          items: [
            "疼痛部位与程度",
            "活动受限与功能评分",
            "体征与关节稳定性"
          ]
        },
        right: {
          icon: "●",
          title: "影像与分级",
          items: [
            "X 线为基础筛查",
            "MRI 评估软组织损伤",
            "K-L 分级辅助决策"
          ]
        }
      },
      {
        step: 2,
        type: "quote",
        style: "border-left: 4px solid var(--accent-coral);",
        text: "分级不仅用于诊断确认，更用于选择治疗强度与随访节奏。临床症状与影像学常存在错配，需综合评估。功能评分是治疗效果追踪的关键指标。",
        author: { icon: "-", text: "分级说明" }
      }
    ]
  },
  {
    badge: { icon: "●", text: "NON-PHARM" },
    title: { text: "非药物治疗：基础但关键" },
    elements: [
      {
        step: 1,
        type: "valueCards",
        style: "margin-bottom: 2vmin;",
        items: [
          { activeStep: 1, icon: "1", title: "体重管理", desc: "降低关节负荷，延缓进展" },
          { activeStep: 2, icon: "2", title: "运动康复", desc: "增强肌力与关节稳定性" },
          { activeStep: 3, icon: "3", title: "物理治疗", desc: "改善疼痛与活动度" },
          { activeStep: 4, icon: "4", title: "辅具支持", desc: "分担负荷并减少疼痛" }
        ]
      },
      {
        step: 2,
        type: "quote",
        style: "background: var(--bg-tertiary);",
        text: "非药物治疗是长期管理的基座。其价值在于降低疼痛强度、延缓结构性进展并减少药物依赖。临床应强调可执行性与持续性，避免“短期干预、长期失效”。",
        author: { icon: "*", text: "临床要点" }
      }
    ]
  },
  {
    badge: { icon: "▲", text: "PHARM" },
    title: { text: "药物治疗：分层与安全性" },
    elements: [
      {
        step: 1,
        type: "timeline",
        style: "margin-bottom: 2vmin;",
        items: [
          { activeStep: 1, badge: "A", icon: "●", title: "镇痛起始", desc: "对乙酰氨基酚或外用NSAIDs", case: "轻度症状" },
          { activeStep: 2, badge: "B", icon: "●", title: "抗炎强化", desc: "口服NSAIDs或短期弱阿片", case: "中重度疼痛" },
          { activeStep: 3, badge: "C", icon: "●", title: "注射治疗", desc: "玻璃酸钠/糖皮质激素", case: "局部顽固症状" },
          { activeStep: 4, badge: "D", icon: "●", title: "合并管理", desc: "关注心肾胃安全性", case: "高龄或共病" }
        ]
      },
      {
        step: 2,
        type: "quote",
        style: "background: var(--bg-tertiary);",
        text: "药物治疗需遵循“最低有效剂量与最短疗程”原则。高龄与共病患者更需要安全性平衡。注射治疗适用于短期缓解，但无法替代长期康复管理。",
        author: { icon: "*", text: "用药策略" }
      }
    ]
  },
  {
    badge: { icon: "■", text: "SURGERY" },
    title: { text: "手术治疗：适应证与时机" },
    elements: [
      {
        step: 1,
        type: "comparison",
        style: "width: 88%; margin-bottom: 2vmin;",
        left: {
          icon: "●",
          title: "保守失败",
          items: [
            "持续严重疼痛",
            "功能明显受限",
            "保守治疗效果差"
          ]
        },
        right: {
          icon: "▲",
          title: "手术选择",
          items: [
            "关节镜评估/处理",
            "截骨或置换",
            "术后康复与随访"
          ]
        }
      },
      {
        step: 2,
        type: "quote",
        style: "background: var(--bg-tertiary);",
        text: "手术时机应以功能受限与生活质量下降为核心指标。过早手术可能带来不必要风险，过迟则错失功能恢复窗口。术后康复决定最终疗效。",
        author: { icon: "*", text: "决策提示" }
      }
    ]
  },
  {
    badge: { icon: "◆", text: "FOLLOW-UP" },
    title: { text: "随访与长期管理" },
    elements: [
      {
        step: 1,
        type: "valueCards",
        style: "margin-bottom: 2vmin;",
        items: [
          { activeStep: 1, icon: "A", title: "症状追踪", desc: "疼痛评分与活动能力" },
          { activeStep: 2, icon: "B", title: "功能评估", desc: "步态与关节活动度" },
          { activeStep: 3, icon: "C", title: "治疗调整", desc: "根据疗效优化方案" },
          { activeStep: 4, icon: "D", title: "风险管理", desc: "关注共病与用药安全" }
        ]
      },
      {
        step: 2,
        type: "quote",
        style: "background: var(--bg-tertiary);",
        text: "长期管理强调连续性与个体化。随访不仅评估疼痛，还应评估生活质量与功能目标达成度。治疗调整需动态完成，避免固定方案造成效率损失。",
        author: { icon: "*", text: "随访原则" }
      }
    ]
  },
  {
    badge: { icon: "*", text: "SUMMARY" },
    title: { text: "结论与临床行动" },
    elements: [
      {
        step: 1,
        type: "ending",
        style: "margin-top: 2vmin;",
        icon: "*",
        message: "以非药物干预为基础，以药物治疗分层推进，\n在合适窗口引入手术，形成长期闭环管理。",
        thanks: "THANKS"
      },
      {
        step: 2,
        type: "quote",
        style: "background: var(--bg-tertiary);",
        text: "骨关节炎的临床治疗需要“目标一致、手段分层、随访闭环”。只有将疼痛控制与功能恢复并行推进，才能实现长期获益。该框架适用于多数慢性退变性关节疾病。",
        author: { icon: "*", text: "总结延展" }
      }
    ]
  }
];
