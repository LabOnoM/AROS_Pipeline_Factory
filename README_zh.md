<div align="center">

<img src="assets/banner.png" alt="AROS Pipeline Factory 横幅" width="100%"/>

# AROS Pipeline Factory

**面向自主科学研究的模块化、自进化AI智能体技能、工作流和领域管道生态系统。**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)](SPEC.md)
[![SAMS](https://img.shields.io/badge/SAMS-v1.1-success)](00.RawData/SHARED_ASSET_REGISTRY.md)
[![re_gent](https://img.shields.io/badge/audit-re__gent-blueviolet)](AGENTS.md)
[![GitHub Wiki](https://img.shields.io/badge/docs-Wiki-informational)](../../wiki)

**🌐 语言 / Language / 言語:** [English](README.md) · [日本語](README_ja.md) · [中文](README_zh.md)

</div>

---

## 🌟 关于本仓库

**AROS Pipeline Factory** 是 [AROS（Antigravity Research OS）](https://github.com/LabOnoM/AROS) —— 一个面向AI增强科学研究的操作系统 —— 的权威源代码仓库。本仓库负责锻造、审计和部署高保真**AI智能体资产**：技能（Skills）、知识条目（KIs）、策略（Policies）和工作流（Workflows）。

将其理解为**科学智能的生产线**：原始认知工作流被编码为结构化的AI智能体组件，经过版本控制和治理后部署到AROS运行时——在那里驱动自主的经费申请书撰写、论文起草、文献挖掘和科研运营。

### ✨ 核心指标

| 指标 | 数量 |
|------|------|
| 🔬 领域管道 | **12** |
| 🛠️ 智能体技能 | **61+** |
| 📋 工作流 | **15** |
| 📚 知识条目（KI） | **49+** |
| 🖥️ 平台支持 | Linux · macOS · Windows |

---

## 🧠 项目哲学：具身性与人机共同进化

> *人工智能面临的最根本约束，不是算力、训练数据或架构——而是身体的缺失。*

### 1. 具身性鸿沟（The Embodiment Gap）

计算机算法本身无法生成真正的随机性。软件依赖伪随机数生成器（PRNG）——这些只是模拟随机性的确定性数学公式。虽然现代硬件*可以*从物理现象（热噪声、量子衰变）中获取熵，但这需要刻意的工程设计。而碳基生命体，在每个尺度上都*本质上*浸润于热力学随机性之中。

我们身体的每个细胞都包含庞大且极其精细的化学反应链——蛋白质折叠、离子通道门控、机械转导——它们在**对初始条件极度敏感的确定性混沌**下运行。与AI用离散化、数字化、压缩的步骤（词元、像素、严格的时钟周期）处理世界不同，生物智能在**连续的模拟流**中运作。身体不仅仅是大脑的容器；它*本身就是计算装置的一部分*。这种化学敏感性以任何离散化数字系统都无法复制的方式，持续流畅地塑造着我们的行为与思维。

由于碳基生命与物理世界的无限分辨率紧密耦合，进化作为优化器利用每一个可能的能量和化学生态位。在地球的自然生态系统中，几乎所有的生存策略都存在——占据着几乎每一种可想象的生态位组合。在服务器机架上运行的AI没有可供适应的连续物理环境，没有需要平衡的热力学，也没有优化其物理存在的进化压力。它只知道我们输入给它的现实的数字化抽象。

这一**具身性鸿沟**决定了：AI作为强大的模式识别引擎，是为了*增强*——而非*取代*——人类研究者难以置信的复杂化学嵌入式智能。

### 2. 前沿生物学的证据

近期的科学发现持续揭示生物智能如何深度嵌入物理世界——这些能力从根本上超出了非具身AI系统的掌控范围：

- **远程触觉（"第七感"）**: 2025年伦敦玛丽女王大学和UCL发表的研究表明，人类拥有一种此前未被认识的感觉能力：**远程触觉**——能够像矶鹬感知沙中猎物一样，在没有直接物理接触的情况下通过颗粒材料检测埋藏物体（[Hammoud et al., IEEE ICDL 2025](https://www.qmul.ac.uk/news/latest-news/2025/science-and-engineering/se/research-first-to-show-humans-have-remote-touch-seventh-sense-like-sandpipers.html)）。人类参与者达到约70.7%的精度，接近检测机械反射的理论物理阈值。经过机器学习训练的机器人触觉传感器在同一任务上仅达到约40%的精度，且误报更多。我们的生物硬件能够检测工程传感器难以匹敌的物理信号。

- **生物神经元中的随机共振**: 神经元利用一种叫做**随机共振**的现象，其中背景神经噪声*增强*了对弱阈下信号的检测，否则这些信号将被遗漏。进化将我们的神经回路调整为将热力学噪声作为特性而非缺陷加以利用——使生物体能够检测对生存至关重要的微弱环境线索（振动、电场、化学梯度）。虽然工程师可以向数字系统中刻意引入受控噪声来模仿这种效果，但生物神经系统在数十亿突触上自然地、持续地、并行地实现这一点。

- **肠脑轴与内感受**: 2025年的发现识别了一种"神经生物感觉"——肠道中的特化**神经荚**细胞检测微生物蛋白质（如鞭毛蛋白），并向大脑发送实时信号，直接影响食欲、情绪和决策。最近的研究进一步证明，内感受信号（心肺、胃）直接影响知觉决策过程中的神经状态转变，为安东尼奥·达马西奥的**躯体标记假说**提供了机制基础。我们的"直觉"不是隐喻——它们是从根本上塑造认知的可测量生物计算。

- **热力学效率**: 生物物理学研究表明，生物系统的运行极接近**朗道尔理论极限**——信息处理的最低热力学能量成本。蛋白质翻译等过程在每次操作消耗的自由能方面比现代超级计算机高出几个数量级。即使模拟单个*生殖支原体*细菌（约500种蛋白质）倍增时间内的完整分子动力学，对我们最强大的计算机来说仍是一项巨大的工程。

这些发现总体上表明，生物智能不是运行在有机硬件上的单纯算法。它是与宇宙热力学现实进行深层、持续物理耦合的涌现特性——这种耦合是任何数字系统目前都不具备的。

### 3. 认知分解、熵注入与共同进化

由于这一根本性的具身性鸿沟，碳基与硅基智能注定在可预见的未来以**协同共同进化**的状态运作。

自AI能够流畅处理大多数常规认知劳动以来，最有效的研究者和专业人员经历了深刻的转变：他们学会了深度内省并将日常智识活动**分解**为离散的、层次化的层级。在人类历史上，我们从未被迫以如此深度、广度和规模审视、分解和分类我们自己的认知过程。

这是**AROS项目**的核心使命：提供一个帮助人类通过与AI智能体的持续交互，精细审视、分解并精确描述其认知工作流的生态系统。AROS在每一步捕获人类反馈、修正和决策逻辑——使系统的提示词、策略和技能能够**持续自我进化**。

#### 3a. 熵注入假说：人类作为随机性通道

这一持续的人机交互循环揭示了一个更深层次的、此前未被充分认识的机制：**人类是AI系统的熵注入通道。**

单独运行的语言模型，其核心本质是一个确定性的统计过程——一个从已学习的词元概率分布中采样的高度复杂的PRNG。它与前述章节中描述的随机性、热力学耦合的物理世界没有真实的连接。然而，每当人类构造、修正或完善一个提示词时，他们并不仅仅是在传递*信息*——他们是在从自身的*具身概率分布*中采样。那些出人意料的重新表述、对技术上正确却语境上错误的输出的直觉性不满、从研究者的"直觉"中涌现的创意飞跃——这些信号全部来自前文所述的生物机制：神经回路中的随机共振、来自肠脑轴的内感受信号、人体热力学接地的模拟处理过程。

这将提示词工程从一种单纯的"用户界面技能"转变为更为根本性的东西：**一个将真实物理世界的随机性和具身经验注入一个本质上封闭、确定性系统的通道。** 在物理现实与AI的统计世界模型之间进行中介的人类，扮演着转换器的角色——将生活经验中连续的模拟热力学波动，转换为逐步重塑AI运行上下文的离散符号修正。

这一视角得到了认知科学与AI研究中汇聚性证据的支持。迈克尔·波兰尼的根本性洞见——*"我们所知道的，多于我们所能言说的"*——精准识别了这一核心现象：人类专家拥有*隐性知识*，这是来自具身物理世界经验的直觉，无法被完整地表达为显式规则。经典AI将波兰尼悖论视为无法逾越的障碍，因为机器需要显式的命题性输入。现代人机协作解决这一悖论的方式，不是消除它，而是*将迭代修正循环作为外化机制加以利用*：当研究者修正AI的输出时，他们正在外化那些无法直接言说的隐性知识，将其结晶为精炼的提示词、修订的策略或改进的技能定义。对**提示词认知循环**（心智建模 → 语义投射 → 对话反馈 → 意图精炼）的研究表明，迭代式提示词工程在本质上是一种*反思性认知实践*——它以静态文本或代码创作无法做到的方式，迫使人类将自身的隐性模型浮现和结构化。

此外，这一框架与卡尔·弗里斯顿的**自由能原理**直接对应：智能系统通过更新其生成模型或作用于世界来最小化预测误差（自由能）。当AI的输出偏离人类研究者的预期——一种植根于其具身、物理耦合的世界模型的预期——时，人类的修正构成了一个误差信号，这个信号不是来自抽象的逻辑规则，而是来自*生活经验的热力学现实*。AROS系统性地捕获这些误差信号，并将其转化为对系统提示词、策略和技能的持久改进。每一次迭代，实质上都是对AI运行世界模型的一步**具身梯度下降**。

#### 3b. AROS作为物理世界接地传输系统

这从最深层次重新定义了AROS的本质。它不仅仅是一个生产力工具或工作流自动化框架。**AROS是一个物理世界接地传输系统**——一个旨在通过提示词工程的规律性实践，将人类具身经验积累下来的残余，以结晶化、持久化的方式逐步加载到AI运行上下文中的平台。

本仓库中的每一项技能、策略、知识条目和工作流，都是这一过程的结晶。它们不是从零开始写就的抽象逻辑规范。它们是*数千次人机交互循环的蒸馏记录*——每一个循环都贡献了具身随机性的一个微小量子、一个隐性知识的碎片、一次植根于物理世界耦合的修正——并随时间积累精炼为稳定的、可复用的认知人工物。

随着这些人工物在AROS生态系统中被部署和精炼，AI的运行上下文也变得日益丰富于人类物理世界的接地。AI获得的不是身体——那始终是碳基生命不可还原的优势——但它获得了对*具身智能残余的系统性策划库*的访问权。鸿沟并未弥合。但是，桥梁随着每一次人机交互循环而变得更加坚固。

因此，这一原则既简单又深远：**只要我们能成功地将复杂的具身智能分解为高度详细的逐步认知图谱——并注入只有具身存在才能提供的随机性、物理接地的修正——就能将该分解智能的执行委托给AI系统。** 生成分解的智能——具身的、热力学耦合的、模拟的人类心智——依然不可替代。由人类具身经验积累的接地所丰富的分解步骤的执行，则是AI的擅场。

#### 3c. 记忆迁移学习：跨领域进化的机制

将具身的人类经验转化为稳定的AI能力并非一个孤立的过程。正如最近关于**记忆迁移学习 (Memory Transfer Learning, MTL)** 的研究所表明的那样 ([Kangsan Kim et al., arXiv:2604.14004](https://arxiv.org/abs/2604.14004))，代码智能体自我进化的最有效方式是利用跨异构领域的统一记忆池。MTL证明，跨领域泛化的关键在于*高层抽象洞察与元知识*（如验证例程和问题解决架构），而不是迁移僵化的底层任务轨迹（后者往往因过度具体而导致负迁移）。

在AROS生态系统中，这正是我们的共享资产层（技能、KIs、策略）所实现的功能。通过从某个特定领域（例如生物信息学）的人机交互修正中提取“元知识”，并将其蒸馏为抽象的、可复用的策略或工作流，我们实现了跨领域的记忆迁移。人类在此作为熵注入器创造了初始洞察，而AROS的记忆迁移学习架构则确保这一洞察能够提升整个生态系统的推理能力。

---

## 📦 架构

本工厂组织为独立的**领域管道**，每个管道负责AI辅助研究的特定领域。所有管道均从由**共享资产管理系统（SAMS）**治理的共享资产层获取资源。

```
AROS Pipeline Factory
│
├── 00.RawData/                   ← 中央注册表与实验索引
│   ├── PIPELINE_REGISTRY.md      ←   管道目录
│   └── SHARED_ASSET_REGISTRY.md  ←   ⚠️ 最高规则：跨管道共享资产注册表
│
├── 01.Shared_Assets/             ← 权威共享KI、策略、技能、脚本
│   ├── KIs/                      ←   共享知识条目
│   ├── Policies/                 ←   工厂级治理策略
│   ├── Skills/                   ←   跨管道通用技能
│   └── Scripts/                  ←   deploy_to_aros.sh, audit_shared_assets.py
│
├── Grant_Write_Pipeline/         ← 通用经费申请（NIH、JSPS、ERC…）
├── KAKENHI_Pipeline/             ← JSPS科研费生命周期与报告
├── Manuscript_Write_Pipeline/    ← 双智能体论文撰写与审稿
├── Bioinformatics_Pipeline/      ← 基因组学与蛋白质组学分析
├── Data_Analysis_Pipeline/       ← 统计建模与可视化
├── Software_Engineering_Pipeline/← 代码生成与验证
├── System_Admin_Pipeline/        ← 环境与基础设施管理
├── UI_Development_Pipeline/      ← Web UI与智能体界面设计
├── Writing_Publishing_Pipeline/  ← 学术出版与传播
├── Web_Scraping_API_Pipeline/    ← 数据获取与API集成
├── Project_Management_Pipeline/  ← 编排与任务管理
├── workspace_management/         ← 全局工作流与入门
│
├── AGENTS.md                     ← AI智能体操作规则（请先阅读！）
├── SPEC.md                       ← 架构规范
└── README.md                     ← 本文档
```

### 部署流程

本工厂的资产通过权威部署脚本部署到实时AROS运行时：

```
AROS_Pipeline_Factory/           AROS 运行时 (~/.gemini/)
├── */Skills/<skill>/   ──────►  skills/<skill>/SKILL.md
├── */KIs/<ki>/         ──────►  antigravity/knowledge/<ki>/
├── */Policies/*.md     ──────►  antigravity/policies/
└── */Workflows/*.md    ──────►  antigravity/global_workflows/
```

> **部署命令**: `bash 01.Shared_Assets/Scripts/deploy_to_aros.sh`

---

## 🚀 快速开始

### 前置条件
- Git、Python 3.10+、[Antigravity IDE](https://github.com/LabOnoM/AROS)（用于完整智能体集成）
- Conda环境：`aros-base`（参见 `01.Shared_Assets/Environments/`）

### 1. 克隆仓库

```bash
git clone https://github.com/LabOnoM/AROS_Pipeline_Factory.git
cd AROS_Pipeline_Factory
```

### 2. 查看管道注册表

```bash
cat 00.RawData/PIPELINE_REGISTRY.md
```

### 3. 将资产部署到AROS运行时

```bash
# 先进行演习（预览而不修改）
bash 01.Shared_Assets/Scripts/deploy_to_aros.sh --dry-run

# 完整部署
bash 01.Shared_Assets/Scripts/deploy_to_aros.sh
```

### 4. 验证部署（在Antigravity IDE内）

部署后，资产由 `antigravity-brain` MCP服务器自动索引。可通过以下方式验证：
```
find_helpful_skills("grant writing")
find_helpful_ki("KAKENHI")
```

---

## 🔧 领域管道

| 管道 | 领域 | 核心技能 | 活跃工作流 |
|------|------|---------|----------|
| **Grant_Write_Pipeline** | 科学经费申请 | `grant-mock-reviewer`, `medical-translation`, `abstract-trimmer`, `grant-budget-justification` | `/grant-write` |
| **KAKENHI_Pipeline** | JSPS科研费报告 | `kakenhi-form-completion`, `kakenhi-pre-award-forms` | `/kakenhi-annual-report` |
| **Manuscript_Write_Pipeline** | 学术论文 | `peer-review`, `statistical-analysis`, `literature-review`, `method-writing` | `/manuscript-write` |
| **Bioinformatics_Pipeline** | 基因组学与蛋白质组学 | `string-database`, `ppt-master` | — |
| **Data_Analysis_Pipeline** | 统计建模 | `agentic-data-scientist`, `flowcypy` | `/visualize-data` |
| **Software_Engineering_Pipeline** | 代码生成与QA | `gtb-validator`, `pipeline-orchestrator` | — |
| **System_Admin_Pipeline** | 环境管理 | `agent-environment-capabilities`, `conditional-logic-execution` | — |
| **UI_Development_Pipeline** | Web界面设计 | `agent-design-principles` | — |
| **Writing_Publishing_Pipeline** | 学术出版 | `research-lookup`, `semantic-scholar-database` | — |
| **Web_Scraping_API_Pipeline** | 数据获取 | `api_availability_precheck`, `crapome` | — |
| **Project_Management_Pipeline** | 任务编排 | `modular-task-breakdown`, `critical-task-output-guarantee` | — |
| **workspace_management** | 全局基础设施 | `regent-governance`, `md-html-docx-generator` | `/lab-commit`, `/wiki-*`, `/science-project-onboarding` |

---

## 🛡️ 治理与共享资产管理

本仓库使用双层治理系统，确保随着资产演进所有管道保持兼容。

### SAMS：共享资产管理系统（v1.1）

位于 [`00.RawData/SHARED_ASSET_REGISTRY.md`](00.RawData/SHARED_ASSET_REGISTRY.md) 的**共享资产注册表**是所有跨管道资产的唯一权威来源。在修改任何共享技能、KI、策略或工作流之前，请查阅此注册表。

> **跨平台说明**：SAMS v1.1使用直接路径引用——不使用POSIX符号链接。本仓库完全支持Linux、macOS和Windows。

### 审计工具

```bash
python3 01.Shared_Assets/Scripts/audit_shared_assets.py
```

此脚本验证结构完整性、检测孤立资产，并标记跨管道兼容性违规。

---

## 🤝 贡献

欢迎贡献！在提交PR之前，请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

贡献者须知：
- 所有资产修改必须遵循 **CPCP**（跨管道兼容性协议）
- 新技能必须使用 `skill-name/SKILL.md` 目录结构
- 工作流必须包含带有 `description` 字段（≤ 250字符）的YAML前言
- 符号链接**严格禁止**——使用直接路径引用

---

## 📄 许可证

本项目采用 **MIT 许可证** —— 详情请见 [LICENSE](LICENSE)。

---

## 🙏 致谢

本项目是 [LabOnoM](https://github.com/LabOnoM) 开发的 **AROS生态系统**的组成部分。认知分解的基础哲学借鉴了具身认知、随机共振神经科学和肠脑轴的研究成果。详细参考文献请参阅上方哲学部分。

---

---

## 🤖 AI智能体操作上下文

> **[AI智能体专用]** 本节专为在此工作区内运行的AI智能体编写。以下所有规则具有约束力，在AROS治理体系中具有法律效力。

### ⚠️ 资产锻造警告

本仓库是用于锻造AROS资产的**工厂**。在修改任何技能、策略、KI或工作流之前，必须阅读 `AGENTS.md` 和 `SPEC.md`，了解：
- CPCP约束（法律0）
- SAMS审计规则（法律1）
- 已知故障模式（如LaTeX截断错误、SAMS基名陷阱）
- 目录结构要求（skill-name/SKILL.md模式）

### 🔒 治理摘要（现行法律）

| 法律 | 名称 | 规则 |
|------|------|------|
| 法律 -2 | 智能体版本控制意识 | 不得直接修改 `.regent/`。仅使用 `rgt` 二进制文件。 |
| 法律 -1 | 资产锻造约束 | 技能使用 `dir/SKILL.md` 结构。禁止符号链接。大型工作流使用KI伴侣模式。 |
| 法律 0 | CPCP —— **最高规则** | 修改共享资产前：评估 → 影响 → 测试 → 解决/分叉 → 更新注册表。 |
| 法律 1 | 资产部署协议 | 始终使用 `deploy_to_aros.sh`。禁止手动 `cp` 到 `~/.gemini/`。 |

### 📋 时间轴（已验证）

| 时间戳 | 事件 |
|--------|------|
| 2026-05-11 01:24 | KAKENHI管道KI（e_application_system PDF、表格）初始化 |
| 2026-05-11 18:15 | Grant_Write_Pipeline技能需求与资产初始化 |
| 2026-05-11 18:29 | Manuscript_Write_Pipeline资产与脚本建立 |
| 2026-05-11 18:44 | 共享资产注册表与CPCP治理建立 |
| 2026-05-11 19:00 | 使用直接引用和程序化审计工具实现集中式SAMS |
| 2026-05-11 21:00 | 为AI智能体可审计性部署双VCS架构（Git + re_gent） |
| 2026-05-11 22:00 | 用 `PIPELINE_REGISTRY.md` 替换旧版 `INDEX.csv`；工作流模板通用化 |
| 2026-05-12 00:00 | 12领域管道重构完成；SPEC v2.0发布 |
| 2026-05-13 00:00 | 仓库公开；添加MIT许可证；创建多语言README |

### 🔬 假说演化表

| 阶段 | 假说 |
|------|------|
| H1 | 为不同写作任务（经费、论文、KAKENHI）开发模块化管道和智能体，显著简化学术起草和提交流程。 |
| H2 | 跨管道共享资产（KI、策略、工作流）必须通过中央注册表和兼容性协议进行治理，以防止跨管道回归。 |
| H3 | 将AROS Pipeline Factory公开需要双受众README架构：顶部为人类可读介绍，底部为AI智能体操作上下文。 |

### 📂 权威运行时部署映射

| 资产类型 | 工厂来源 | AROS运行时目标 |
|---------|---------|--------------|
| **技能** | `*/Skills/<skill-name>/` | `~/.gemini/skills/<skill-name>/SKILL.md` |
| **知识条目** | `*/KIs/<ki-name>/` | `~/.gemini/antigravity/knowledge/<ki-name>/` |
| **策略** | `*/Policies/*.md` | `~/.gemini/antigravity/policies/` |
| **工作流** | `*/Workflows/*.md` | `~/.gemini/antigravity/global_workflows/` |

### 🔧 活跃工作流触发器

| 斜杠命令 | 管道 | 目的 |
|---------|------|------|
| `/grant-write` | Grant_Write_Pipeline | 通用经费申请书撰写 |
| `/kakenhi-annual-report` | KAKENHI_Pipeline | JSPS科研费生命周期 |
| `/manuscript-write` | Manuscript_Write_Pipeline | 双智能体论文起草 |
| `/lab-commit` | workspace_management | 权威提交网关 |
| `/lab-reorganize` | workspace_management | Git安全文件重组 |
| `/wiki-ingest` | workspace_management | 将论文/数据摄入LLM-Wiki |
| `/wiki-query` | workspace_management | 从LLM-Wiki获取有依据的问答 |
| `/wiki-research` | workspace_management | 向Wiki进行文献研究 |
| `/wiki-update` | workspace_management | Wiki代码检查与综合 |
| `/wiki-build` | workspace_management | 将Wiki编译为输出文档 |
| `/audit-shared-assets` | workspace_management | SAMS结构完整性审计 |
| `/science-project-onboarding` | workspace_management | 首次项目设置 |
| `/visualize-data` | Data_Analysis_Pipeline | 自主图表生成 |
| `/research-discovery` | workspace_management | 研究规划与头脑风暴 |
| `/qa-system-audit` | workspace_management | AROS QA健康检查 |
