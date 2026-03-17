# nano-claude-code 设计方案

**项目**: nano-claude-code
**版本**: 1.0.0
**创建日期**: 2026-03-17
**状态**: 设计阶段

---

## 📋 目录

- [项目概述](#项目概述)
- [核心定位](#核心定位)
- [与 learn-claude-code 的区别](#与-learn-claude-code-的区别)
- [技术栈选择](#技术栈选择)
- [版本演进路径](#版本演进路径)
- [多语言实现策略](#多语言实现策略)
- [项目结构](#项目结构)
- [核心功能设计](#核心功能设计)
- [用户界面设计](#用户界面设计)
- [实施路线图](#实施路线图)

---

## 项目概述

**nano-claude-code** 是一个轻量级、实用的 AI 编程助手，从零开始构建（from 0 to 1）。

### 核心特性

- ✅ **实用工具导向**: 不仅理解原理，更注重实际可用性
- ✅ **渐进式开发**: 从最简单的 MVP 开始，逐步添加功能
- ✅ **多语言实现**: Python、TypeScript、Rust 版本，支持对比学习
- ✅ **双前端**: 桌面 GUI 应用 + Web 应用
- ✅ **多模型支持**: 兼容 Anthropic API 的多个提供商
- ✅ **通用语言支持**: 通过配置支持任意编程语言

### 目标用户

1. **学习者**: 想要理解 AI 编程助手工作原理的开发者
2. **贡献者**: 希望参与开源 AI 工具开发的开发者
3. **用户**: 需要轻量级 AI 编程助手的日常开发者

---

## 核心定位

### 项目类型：实用工具 + 学习资源

```
                    纯教学项目
                        ↓
              learn-claude-code
                        ↓
              理解代理核心机制
                        ↓
                nano-claude-code
                        ↓
                    实用工具
                        ↓
              日常可用的 AI 编程助手
```

### 核心价值

1. **从 0 到 1**: 完整展示如何从零构建一个 AI 编程助手
2. **实用性优先**: 每个版本都是可用的，不是玩具代码
3. **多语言对比**: 同一功能在不同语言中的实现差异
4. **可扩展性**: 清晰的架构，便于添加新功能

---

## 与 learn-claude-code 的区别

| 维度 | learn-claude-code | nano-claude-code |
|------|------------------|------------------|
| **主要目标** | 教学理解代理核心机制 | 构建实用的 AI 编程助手 |
| **复杂度** | 12 个会话，包含高级特性 | ~10 个版本，聚焦核心功能 |
| **包含特性** | 团队协作、工作树隔离、子代理 | 代码理解、持久化、GUI |
| **前端** | 可视化教学平台 (Next.js) | 实际 GUI 应用 + Web |
| **会话管理** | 每次会话独立 | 持久化会话和历史 |
| **代码风格** | 教学导向，强调清晰 | 实用导向，强调健壮性 |
| **语言支持** | 仅 Python | Python + TypeScript + Rust |
| **使用场景** | 学习和理解 | 日常开发工具 |

### 核心差异总结

**learn-claude-code** 回答 "AI 编程代理是如何工作的？"
**nano-claude-code** 回答 "如何构建一个实用的 AI 编程助手？"

两者互补，可以结合学习：
1. 先通过 `learn-claude-code` 理解核心机制
2. 再通过 `nano-claude-code` 学习如何构建实用工具

---

## 技术栈选择

### 后端语言

```
Python          TypeScript        Rust
─────────       ──────────        ──────
• AI 库丰富     • 全栈统一        • 极致性能
• 学习曲线平缓  • 前端集成        • 内存安全
• 快速原型      • 生态成熟        • 编译产物小
• 易于测试      • 类型安全        • 并发优秀
```

**选择策略**: 三种语言并行实现，用户可按需选择

### 前端技术栈

#### Web 应用
- **框架**: Next.js 15 (App Router)
- **UI 库**: shadcn/ui + Tailwind CSS
- **状态管理**: Zustand
- **API 层**: tRPC (类型安全)

#### 桌面应用

**Electron** (主力版本)
- 成熟稳定
- 生态丰富
- 容易开发

**Tauri** (轻量版本)
- 体积小
- 性能好
- 安全性高

### AI 模型集成

采用 **Anthropic-compatible API** 策略：

```python
# 配置示例
ANTHROPIC_API_KEY=sk-ant-xxx
MODEL_ID=claude-sonnet-4-6
ANTHROPIC_BASE_URL=https://api.anthropic.com  # 可替换为其他提供商
```

**支持的提供商**:
- Anthropic (Claude)
- MiniMax
- GLM (智谱)
- Kimi (Moonshot)
- DeepSeek
- 其他兼容 Anthropic API 的服务

---

## 版本演进路径

### Phase 1: 核心循环 (v01-v04)

#### v01: 最小循环
**Motto**: "One loop & Bash is all you need"

```
User → LLM → Tool → Result → Loop
```

**功能**:
- ✅ 基础 Agent 循环
- ✅ Bash 工具
- ✅ 简单的命令行界面

**代码量**: ~100 行

---

#### v02: 工具系统
**Motto**: "Adding a tool means adding one handler"

```
Tool Dispatch Map
├── bash
├── read_file
├── write_file
└── edit_file
```

**功能**:
- ✅ 工具调度系统
- ✅ 文件操作工具
- ✅ 路径安全沙箱

**新增**: ~150 行

---

#### v03: 任务规划
**Motto**: "An agent without a plan drifts"

```
TodoManager
├── pending
├── in_progress
└── completed
```

**功能**:
- ✅ TodoWrite 工具
- ✅ 任务状态管理
- ✅ 提醒系统

**新增**: ~200 行

---

#### v04: 代码理解
**Motto**: "Understand before you change"

```
Code Understanding
├── 文件结构分析
├── 代码搜索
└── 依赖关系图
```

**功能**:
- ✅ 代码库探索
- ✅ Grep 搜索工具
- ✅ 项目结构分析

**新增**: ~250 行

---

### Phase 2: 实用增强 (v05-v07)

#### v05: 上下文管理
**Motto**: "Context will fill up; make room"

```
Context Compression
├── Token 统计
├── 摘要压缩
└── 历史归档
```

**功能**:
- ✅ Token 使用追踪
- ✅ 自动上下文压缩
- ✅ 对话历史管理

**新增**: ~300 行

---

#### v06: 代码生成
**Motto**: "Generate with intent, not by accident"

```
Code Generation
├── 模板系统
├── 代码补全
└── 组件生成
```

**功能**:
- ✅ 代码模板引擎
- ✅ 智能代码补全
- ✅ 项目脚手架

**新增**: ~350 行

---

#### v07: 多语言支持
**Motto**: "Config over code"

```
Language Config
├── 运行命令
├── 测试框架
├── 构建工具
└── 包管理器
```

**功能**:
- ✅ 语言特定的配置文件
- ✅ 自动检测项目类型
- ✅ 自适应工具调用

**新增**: ~200 行

---

### Phase 3: 完整体验 (v08-v10)

#### v08: 持久化
**Motto**: "State survives sessions"

```
Persistence
├── 会话存储
├── 任务历史
└── 配置管理
```

**功能**:
- ✅ SQLite/JSON 持久化
- ✅ 会话恢复
- ✅ 配置同步

**新增**: ~400 行

---

#### v09: GUI 前端
**Motto**: "See what's happening"

```
Desktop/Web UI
├── 聊天界面
├── 文件浏览器
├── 任务面板
└── 设置页面
```

**功能**:
- ✅ Electron/Tauri 桌面应用
- ✅ Next.js Web 应用
- ✅ 实时状态显示

**新增**: ~2000 行

---

#### v10: 插件系统
**Motto**: "Extend without modifying"

```
Plugin System
├── 自定义工具
├── 扩展加载
└── 钩子系统
```

**功能**:
- ✅ 插件 API
- ✅ 自定义工具注册
- ✅ 生命周期钩子

**新增**: ~500 行

---

## 多语言实现策略

### 实现原则

1. **功能对等**: 每个版本在不同语言中实现相同的核心功能
2. **保持特色**: 利用每种语言的特性，不强行统一风格
3. **代码示例**: 在文档中展示关键功能的跨语言对比
4. **渐进实现**: 按版本顺序实现，不跳跃

### 语言特性对比

| 特性 | Python | TypeScript | Rust |
|------|--------|------------|------|
| **类型系统** | 动态 | 静态 (可选) | 静态 (强) |
| **并发模型** | GIL/async | async/await | async/await |
| **错误处理** | 异常 | 异常 | Result<T,E> |
| **包管理** | pip | npm/yarn | cargo |
| **AI 库** | 丰富 | 良好 | 发展中 |
| **学习曲线** | 低 | 中 | 高 |
| **性能** | 中 | 中 | 高 |

### 实现优先级

```
Phase 1: Python 优先
• 快速原型
• 验证设计
• 文档先行

Phase 2: TypeScript 并行
• 前后端统一
• 全栈能力
• 生态优势

Phase 3: Rust 补充
• 性能关键组件
• 系统级操作
• 生产优化
```

---

## 项目结构

```
nano-claude-code/
├── README.md                      # 项目介绍
├── LICENSE                        # MIT 许可证
├── .github/                       # GitHub 配置
│   └── workflows/                 # CI/CD 工作流
│
├── docs/                          # 共享文档
│   ├── plans/                     # 设计文档
│   │   ├── 2026-03-17-nano-claude-code-design.md  # 主设计文档 (本文件)
│   │   ├── architecture.md        # 架构设计
│   │   ├── version-roadmap.md     # 版本路线图
│   │   └── multi-language-guide.md # 多语言指南
│   │
│   ├── en/                        # 英文文档
│   │   ├── getting-started.md
│   │   ├── architecture.md
│   │   └── api-reference.md
│   │
│   ├── zh/                        # 中文文档
│   │   └── (对应英文结构)
│   │
│   └── ja/                        # 日文文档
│       └── (对应英文结构)
│
├── implementations/               # 多语言实现
│   │
│   ├── python/                    # Python 实现
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   ├── pyproject.toml
│   │   │
│   │   ├── v01_minimal_loop/      # v01: 最小循环
│   │   │   ├── agent.py
│   │   │   ├── tools.py
│   │   │   └── main.py
│   │   │
│   │   ├── v02_tool_system/       # v02: 工具系统
│   │   │   ├── agent.py
│   │   │   ├── tools/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── bash.py
│   │   │   │   ├── file_ops.py
│   │   │   │   └── dispatch.py
│   │   │   └── main.py
│   │   │
│   │   ├── v03_task_planning/     # v03: 任务规划
│   │   │   ├── agent.py
│   │   │   ├── tools/
│   │   │   ├── todo_manager.py
│   │   │   └── main.py
│   │   │
│   │   ├── v04_code_understanding/ # v04: 代码理解
│   │   │   └── ...
│   │   │
│   │   ├── v05_context_management/ # v05: 上下文管理
│   │   │   └── ...
│   │   │
│   │   ├── v06_code_generation/   # v06: 代码生成
│   │   │   └── ...
│   │   │
│   │   ├── v07_multi_language/    # v07: 多语言支持
│   │   │   └── ...
│   │   │
│   │   ├── v08_persistence/       # v08: 持久化
│   │   │   └── ...
│   │   │
│   │   ├── v09_gui_frontend/      # v09: GUI 前端
│   │   │   ├── backend/
│   │   │   └── frontend/
│   │   │
│   │   └── v10_plugin_system/     # v10: 插件系统
│   │       └── ...
│   │
│   ├── typescript/                # TypeScript 实现
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   ├── src/
│   │   │   ├── v01_minimal_loop/
│   │   │   ├── v02_tool_system/
│   │   │   └── ...
│   │   └── (与 Python 相同的版本结构)
│   │
│   └── rust/                      # Rust 实现
│       ├── Cargo.toml
│       ├── src/
│       │   ├── v01_minimal_loop/
│       │   ├── v02_tool_system/
│       │   └── ...
│       └── (与 Python 相同的版本结构)
│
├── shared/                        # 跨语言共享资源
│   ├── prompts/                   # 系统提示词
│   │   ├── default.md
│   │   ├── coding.md
│   │   └── expert.md
│   │
│   ├── configs/                   # 配置示例
│   │   ├── languages/
│   │   │   ├── python.yaml
│   │   │   ├── typescript.yaml
│   │   │   ├── rust.yaml
│   │   │   ├── go.yaml
│   │   │   └── javascript.yaml
│   │   │
│   │   ├── models/
│   │   │   ├── claude.yaml
│   │   │   └── openai.yaml
│   │   │
│   │   └── .env.example
│   │
│   └── tests/                     # 测试用例
│       ├── unit/
│       └── integration/
│
├── web/                           # Web 前端 (Next.js)
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── chat/
│   │   ├── files/
│   │   └── settings/
│   ├── components/
│   │   ├── ui/                    # shadcn/ui 组件
│   │   ├── ChatInterface.tsx
│   │   ├── FileExplorer.tsx
│   │   ├── TaskPanel.tsx
│   │   └── Settings.tsx
│   ├── lib/
│   │   ├── api.ts                 # API 客户端
│   │   ├── store.ts               # Zustand 状态
│   │   └── utils.ts
│   └── public/
│
└── desktop/                       # 桌面应用
    ├── electron/                  # Electron 版本
    │   ├── package.json
    │   ├── main/
    │   │   ├── main.ts
    │   │   ├── ipc/
    │   │   └── windows/
    │   └── renderer/              # 复用 web/ 前端
    │
    └── tauri/                     # Tauri 版本
        ├── src-tauri/
        │   ├── Cargo.toml
        │   ├── src/
        │   │   ├── main.rs
        │   │   └── commands.rs
        │   └── tauri.conf.json
        └── src/                   # 复用 web/ 前端
```

---

## 核心功能设计

### 1. Agent 循环 (核心)

```python
def agent_loop(messages: List[Message]) -> None:
    """
    核心代理循环

    流程:
    1. 发送消息和工具定义给 LLM
    2. 检查 stop_reason
    3. 如果是 tool_use，执行工具并收集结果
    4. 将结果追加到消息列表
    5. 循环回到步骤 1
    """
    while True:
        response = llm.chat(messages, tools)

        messages.append({
            "role": "assistant",
            "content": response.content
        })

        if response.stop_reason != "tool_use":
            break

        results = execute_tools(response.tool_calls)
        messages.append({
            "role": "user",
            "content": results
        })
```

### 2. 工具系统

```python
class ToolDispatcher:
    """
    工具调度器

    职责:
    - 注册工具处理器
    - 调度工具调用
    - 处理工具结果
    """

    def __init__(self):
        self.handlers: Dict[str, Callable] = {}

    def register(self, name: str, handler: Callable):
        """注册工具处理器"""
        self.handlers[name] = handler

    def dispatch(self, tool_name: str, **kwargs) -> str:
        """调度工具调用"""
        handler = self.handlers.get(tool_name)
        if not handler:
            return f"Unknown tool: {tool_name}"
        return handler(**kwargs)
```

### 3. Todo 管理器

```python
class TodoManager:
    """
    任务管理器

    特性:
    - 只能有一个任务处于 in_progress
    - 自动提醒机制
    - 状态持久化
    """

    def __init__(self):
        self.items: List[TodoItem] = []
        self.nag_counter = 0

    def update(self, items: List[TodoItem]) -> str:
        """更新任务列表"""
        self._validate(items)
        self.items = items
        self.nag_counter = 0
        return self.render()

    def should_nag(self) -> bool:
        """判断是否需要提醒"""
        self.nag_counter += 1
        return self.nag_counter >= 3

    def render(self) -> str:
        """渲染任务列表"""
        return "\n".join(
            f"{item.status_emoji} {item.text}"
            for item in self.items
        )
```

### 4. 代码理解工具

```python
class CodeAnalyzer:
    """
    代码分析器

    功能:
    - 项目结构分析
    - 代码搜索
    - 依赖关系图
    """

    def analyze_structure(self, path: str) -> ProjectStructure:
        """分析项目结构"""
        # 扫描目录树
        # 识别文件类型
        # 构建结构模型
        pass

    def search_code(self, pattern: str, path: str) -> List[Match]:
        """搜索代码"""
        # 使用 ripgrep
        # 返回匹配结果
        pass

    def build_dependency_graph(self, path: str) -> DependencyGraph:
        """构建依赖关系图"""
        # 分析 import/require
        # 构建依赖图
        pass
```

---

## 用户界面设计

### Web 应用布局

```
┌─────────────────────────────────────────────────────────────┐
│  Logo    nano-claude-code    [Settings]    [GitHub]         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐  ┌────────────────────────────────────────┐│
│  │             │  │                                         ││
│  │   Files     │  │         Chat Interface                 ││
│  │             │  │                                         ││
│  │  📁 src/    │  │  User: Help me refactor this function  ││
│  │  📁 tests/  │  │  ──────────────────────────────────────││
│  │  📄 main.py │  │  Agent: I'll help you refactor...      ││
│  │  📄 utils.py│  │                                         ││
│  │             │  │  Tool: read_file("main.py")            ││
│  │  [Upload]   │  │  Result: [file content]                ││
│  │             │  │                                         ││
│  └─────────────┘  └────────────────────────────────────────┘│
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Tasks                                    [+ Add Task] │ │
│  │  ─────────────────────────────────────────────────────│ │
│  │  ☐ Analyze current code structure                     │ │
│  │  ⬝ Refactor main.py                                   │ │
│  │  ☐ Add tests for new functions                        │ │
│  │  ☐ Update documentation                               │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 桌面应用布局

```
┌─────────────────────────────────────────────────────────────┐
│  ┌─┐  nano-claude-code           [_] [□] [×]              │
│  │ │                                                         │
├────┴─────────────────────────────────────────────────────────┤
│ File  Edit  View  Tools  Help                                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐  ┌───────────────────────────────────────────┐│
│  │          │  │                                           ││
│  │ Explorer │  │              Chat                         ││
│  │          │  │                                           ││
│  │ ▶ src/   │  │  User: Implement a new feature           ││
│  │ ▶ tests/ │  │  ────────────────────────────────────────││
│  │   main.py│  │  Agent: I'll help you with that...       ││
│  │   utils.py│  │                                           ││
│  │          │  │  🔧 Running: npm test                     ││
│  │          │  │  ✓ All tests passed                       ││
│  └──────────┘  └───────────────────────────────────────────┘│
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Tasks (3 active)                           [Clear All] │ │
│  │  ─────────────────────────────────────────────────────│ │
│  │  ⬝ Implement feature X                        [In Prog]│ │
│  │  ☐ Write unit tests                          [Pending]│ │
│  │  ☐ Update docs                                [Pending]│ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Status: Ready  │  Model: claude-sonnet-4-6  │  Tokens: 2.3k│
└─────────────────────────────────────────────────────────────┘
```

---

## 实施路线图

### Phase 1: 基础设施 (Week 1-2)

- [x] 创建项目结构
- [ ] 初始化 Git 仓库
- [ ] 设置 CI/CD
- [ ] 编写基础文档

### Phase 2: Python 实现 (Week 3-6)

- [ ] v01: 最小循环
- [ ] v02: 工具系统
- [ ] v03: 任务规划
- [ ] v04: 代码理解
- [ ] v05: 上下文管理
- [ ] v06: 代码生成
- [ ] v07: 多语言支持

### Phase 3: TypeScript 实现 (Week 7-10)

- [ ] 复刻 Python 版本 v01-v07
- [ ] 类型安全的 API 设计
- [ ] 前后端代码共享

### Phase 4: 前端实现 (Week 11-14)

- [ ] Web 应用 (Next.js)
- [ ] 桌面应用 (Electron)
- [ ] UI/UX 优化

### Phase 5: 高级特性 (Week 15-18)

- [ ] v08: 持久化
- [ ] v09: GUI 前端集成
- [ ] v10: 插件系统

### Phase 6: Rust 实现 (Week 19-22)

- [ ] 核心组件 Rust 化
- [ ] 性能优化
- [ ] 生产就绪

---

## 成功标准

### 功能完整性

- ✅ 所有 10 个版本都实现完成
- ✅ 三种语言功能对等
- ✅ 文档覆盖率 100%

### 代码质量

- ✅ 单元测试覆盖率 > 80%
- ✅ 类型安全 (TS/Rust)
- ✅ 无已知安全漏洞

### 用户体验

- ✅ 响应时间 < 2s
- ✅ 错误处理完善
- ✅ 界面直观易用

### 社区

- ✅ Star 数 > 1000
- ✅ 贡献者 > 20
- ✅ 活跃的 Issue/PR

---

## 许可证

MIT License - 见 [LICENSE](../LICENSE) 文件

---

## 联系方式

- GitHub: [nano-claude-code](https://github.com/YuanyuanMa03/nano-claude-code)
- Issues: [GitHub Issues](https://github.com/YuanyuanMa03/nano-claude-code/issues)

---

**"从 0 到 1，构建你自己的 AI 编程助手"**
