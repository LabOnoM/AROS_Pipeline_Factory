const SLIDES = [
  {
    badge: { icon: "*", text: "MEDICAL BRIEF" },
    title: { text: "肠炎与结直肠癌" },
    subtitle: "从慢性炎症到癌变风险的机制与干预",
    clickHint: "2026.02.11",
    elements: [
      {
        step: 1,
        type: "quote",
        style: "border-left: 4px solid var(--accent-green);",
        text: "慢性炎症为癌变提供持续的生物学压力与微环境偏置。",
        author: { icon: "-", text: "核心判断" }
      },
      {
        step: 2,
        type: "quote",
        style: "background: var(--bg-tertiary);",
        text: "肠炎不是孤立事件，而是长期损伤与修复循环的一部分。持续的炎症信号会改变上皮细胞的分化轨迹，增加基因不稳定性。微环境改变为异常克隆扩增创造条件，因此风险管理应前移到炎症阶段。",
        author: { icon: "*", text: "讲解补充" }
      }
    ]
  },
  {
    badge: { icon: "■", text: "BURDEN" },
    title: { text: "临床负担与风险分层" },
    elements: [
      {
        step: 1,
        type: "stats",
        title: "临床上需要被持续关注的三件事",
        items: [
          { icon: "●", value: "慢性病程", label: "持续炎症与组织修复" },
          { icon: "■", value: "风险累积", label: "病程越久风险越高" },
          { icon: "▲", value: "可预防性", label: "早筛可显著降低负担" }
        ]
      },
      {
        step: 2,
        type: "quote",
        style: "background: var(--bg-tertiary);",
        text: "风险分层应综合病程长度、炎症活动度与组织学异常。病程代表累积损伤，活动度反映近期进展速度，组织学异常提示癌前演化迹象。三者联动可显著提高临床判断准确性。",
        author: { icon: "*", text: "分层原则" }
      }
    ]
  },
  {
    badge: { icon: "▲", text: "PATHWAY" },
    title: { text: "炎症到癌变的演化路径" },
    elements: [
      {
        step: 1,
        type: "timeline",
        style: "margin-bottom: 2vmin;",
        items: [
          { activeStep: 1, badge: "1", icon: "●", title: "炎症激活", desc: "免疫因子持续释放", case: "屏障功能下降" },
          { activeStep: 2, badge: "2", icon: "●", title: "上皮损伤", desc: "反复修复与异常增殖", case: "细胞周期失衡" },
          { activeStep: 3, badge: "3", icon: "●", title: "不典型增生", desc: "结构与基因异常累积", case: "癌前病变形成" },
          { activeStep: 4, badge: "4", icon: "●", title: "癌变进程", desc: "侵袭与转移风险增加", case: "结直肠癌发生" }
        ]
      },
      {
        step: 2,
        type: "quote",
        style: "background: var(--bg-tertiary);",
        text: "该路径强调异常是逐步累积的过程。炎症提供选择压力，不典型克隆在此基础上获得生存优势。识别癌前病变阶段并介入，是阻断癌变最关键的窗口。",
        author: { icon: "*", text: "机制阐释" }
      }
    ]
  },
  {
    badge: { icon: "◆", text: "MECHANISM" },
    title: { text: "关键机制：屏障破坏与微环境重塑" },
    elements: [
      {
        step: 1,
        type: "comparison",
        style: "width: 90%; margin-bottom: 2vmin;",
        left: {
          icon: "○",
          title: "健康肠道",
          items: [
            "屏障完整，稳态维持",
            "菌群多样性高",
            "免疫反应可控",
            "上皮更新节律稳定"
          ]
        },
        right: {
          icon: "●",
          title: "炎症肠道",
          items: [
            "屏障破坏，慢性渗漏",
            "菌群失衡与致炎因子",
            "促增殖信号持续",
            "DNA损伤修复压力上升"
          ]
        }
      },
      {
        step: 2,
        type: "quote",
        style: "border-left: 4px solid var(--accent-coral);",
        text: "屏障破坏导致菌群与代谢物进入黏膜层，长期刺激免疫系统。促增殖与DNA损伤压力叠加，使异常克隆更容易扩增。微环境重塑解释了“炎症持续时间”与“癌变风险”之间的强相关性。",
        author: { icon: "-", text: "机制要点" }
      }
    ]
  },
  {
    badge: { icon: "●", text: "WARNING" },
    title: { text: "高危信号与重点人群" },
    elements: [
      {
        step: 1,
        type: "valueCards",
        style: "margin-bottom: 2vmin;",
        items: [
          { activeStep: 1, icon: "1", title: "症状信号", desc: "持续腹痛、便血、体重下降" },
          { activeStep: 2, icon: "2", title: "高危人群", desc: "炎症性肠病病程长、家族史" },
          { activeStep: 3, icon: "3", title: "检查提示", desc: "肠镜出现不典型增生或息肉" },
          { activeStep: 4, icon: "4", title: "系统风险", desc: "免疫抑制或代谢异常叠加" },
          { activeStep: 5, icon: "5", title: "行为风险", desc: "饮食结构不良、久坐、吸烟" }
        ]
      },
      {
        step: 2,
        type: "quote",
        style: "background: var(--bg-tertiary);",
        text: "高危信号强调“组合效应”。单一因素未必提示高风险，但多因素叠加需要提高警惕。临床应整合症状、病史与检查结果，避免单点判断造成漏诊。",
        author: { icon: "*", text: "风险解读" }
      }
    ]
  },
  {
    badge: { icon: "◆", text: "DIAGNOSIS" },
    title: { text: "诊断路径：从症状到证据" },
    elements: [
      {
        step: 1,
        type: "timeline",
        style: "margin-bottom: 2vmin;",
        items: [
          { activeStep: 1, badge: "1", icon: "●", title: "临床提示", desc: "症状与病程评估", case: "初筛分层" },
          { activeStep: 2, badge: "2", icon: "●", title: "实验室评估", desc: "炎症指标与贫血风险", case: "辅助判断" },
          { activeStep: 3, badge: "3", icon: "●", title: "内镜与活检", desc: "可视化证据 + 病理确认", case: "关键证据" },
          { activeStep: 4, badge: "4", icon: "●", title: "风险分级", desc: "整合病理与病程", case: "制定随访" }
        ]
      },
      {
        step: 2,
        type: "quote",
        style: "background: var(--bg-tertiary);",
        text: "诊断路径强调“证据链”完整性。内镜与病理是确诊的核心节点，实验室指标用于补充炎症状态。风险分级决定随访强度与干预策略。",
        author: { icon: "*", text: "路径说明" }
      }
    ]
  },
  {
    badge: { icon: "▲", text: "SURVEILLANCE" },
    title: { text: "监测与早筛：以风险分层驱动" },
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
      },
      {
        step: 2,
        type: "quote",
        style: "background: var(--bg-tertiary);",
        text: "随访频率不是固定值，而是风险分层的函数。高风险人群需缩短间隔，低风险可适度延长。动态调整的目标是以最小成本获得最大预警收益。",
        author: { icon: "*", text: "随访原则" }
      }
    ]
  },
  {
    badge: { icon: "■", text: "INTERVENTION" },
    title: { text: "干预要点：控制炎症与预防癌变" },
    elements: [
      {
        step: 1,
        type: "comparison",
        style: "width: 88%; margin-bottom: 2vmin;",
        left: {
          icon: "●",
          title: "炎症控制",
          items: [
            "规范用药与依从性管理",
            "监测病情活动度",
            "减少复发频率",
            "降低黏膜持续损伤"
          ]
        },
        right: {
          icon: "▲",
          title: "癌变预防",
          items: [
            "早筛并切除可疑病灶",
            "生活方式干预",
            "长期随访与风险再评估",
            "关注高危分子标志"
          ]
        }
      },
      {
        step: 2,
        type: "quote",
        style: "background: var(--bg-tertiary);",
        text: "预防不是一次性动作，而是贯穿病程的管理策略。炎症控制与癌变预防需同步推进，否则风险会在“空窗期”积累。高危分子标志可提供更早的风险提示。",
        author: { icon: "*", text: "临床共识" }
      }
    ]
  },
  {
    badge: { icon: "■", text: "ACTION" },
    title: { text: "临床行动清单" },
    elements: [
      {
        step: 1,
        type: "valueCards",
        style: "margin-bottom: 2vmin;",
        items: [
          { activeStep: 1, icon: "A", title: "建立风险档案", desc: "病程、家族史、病理信息" },
          { activeStep: 2, icon: "B", title: "规范随访节奏", desc: "风险分层 + 动态调整" },
          { activeStep: 3, icon: "C", title: "强化生活方式管理", desc: "饮食、运动、戒烟" },
          { activeStep: 4, icon: "D", title: "闭环复评", desc: "随访中更新风险等级" }
        ]
      },
      {
        step: 2,
        type: "quote",
        style: "background: var(--bg-tertiary);",
        text: "行动清单的核心是将复杂风险管理转化为可执行步骤。风险档案为分层提供数据，随访节奏保证动态监测有效性。生活方式管理降低炎症触发因素，闭环复评确保策略持续优化。",
        author: { icon: "*", text: "执行原则" }
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
        message: "以炎症控制为抓手、以风险分层为框架、以持续随访为闭环，\n把结直肠癌风险前移到可控阶段。",
        thanks: "THANKS"
      },
      {
        step: 2,
        type: "quote",
        style: "background: var(--bg-tertiary);",
        text: "总体策略强调“前移与闭环”。前移到炎症阶段进行管理，闭环在随访与复评中持续优化。该框架同样适用于需要长期管理的高危慢性疾病。",
        author: { icon: "*", text: "总结延展" }
      }
    ]
  }
];
