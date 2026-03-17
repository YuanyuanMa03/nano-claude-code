# nano-claude-code 架构设计

**版本**: 1.0.0
**更新日期**: 2026-03-17

---

## 📋 目录

- [整体架构](#整体架构)
- [核心组件](#核心组件)
- [数据流设计](#数据流设计)
- [工具系统架构](#工具系统架构)
- [多语言实现对比](#多语言实现对比)
- [安全设计](#安全设计)
- [性能优化](#性能优化)

---

## 整体架构

### 系统分层

```
┌─────────────────────────────────────────────────────────────┐
│                         用户界面层                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Web UI     │  │  Desktop UI  │  │   CLI UI     │      │
│  │  (Next.js)   │  │  (Electron)  │  │  (Terminal)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         API 网关层                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   REST API   │  │   WebSocket  │  │   tRPC       │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         业务逻辑层                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Agent Loop  │  │ Tool System  │  │ Todo Manager │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │Code Analyzer │  │Context Mgr   │  │Code Generator│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         数据访问层                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   File System│  │   Database   │  │   Cache      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         外部服务层                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  LLM APIs    │  │  Git APIs    │  │  File APIs   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 架构原则

1. **分层清晰**: 每层职责明确，易于维护和扩展
2. **低耦合**: 层间通过接口通信，便于替换实现
3. **高内聚**: 相关功能集中在同一模块
4. **可测试**: 每层都可独立测试

---

## 核心组件

### 1. Agent Loop (代理循环)

**职责**: 协调整个代理的执行流程

```python
class AgentLoop:
    """
    代理循环核心

    流程:
    1. 接收用户输入
    2. 调用 LLM
    3. 执行工具
    4. 收集结果
    5. 循环或终止
    """

    def __init__(
        self,
        llm_client: LLMClient,
        tool_dispatcher: ToolDispatcher,
        context_manager: ContextManager,
    ):
        self.llm = llm_client
        self.tools = tool_dispatcher
        self.context = context_manager

    def run(self, query: str) -> AgentResponse:
        """执行代理循环"""
        messages = [Message.user(query)]

        while True:
            # 调用 LLM
            response = self.llm.chat(
                messages=messages,
                tools=self.tools.get_schemas(),
            )

            # 添加助手响应
            messages.append(Message.assistant(response.content))

            # 检查是否需要调用工具
            if response.stop_reason != "tool_use":
                break

            # 执行工具
            results = self.tools.execute_batch(response.tool_calls)

            # 添加工具结果
            messages.append(Message.tool_results(results))

            # 管理上下文
            self.context.maybe_compress(messages)

        return AgentResponse(
            content=response.content,
            messages=messages,
        )
```

### 2. Tool System (工具系统)

**职责**: 管理和执行所有工具

```python
class ToolDispatcher:
    """
    工具调度器

    特性:
    - 动态工具注册
    - 参数验证
    - 错误处理
    - 权限检查
    """

    def __init__(self, sandbox: Path):
        self.tools: Dict[str, Tool] = {}
        self.sandbox = sandbox

    def register(self, tool: Tool):
        """注册工具"""
        self._validate(tool)
        self.tools[tool.name] = tool

    def get_schemas(self) -> List[dict]:
        """获取所有工具的 Schema"""
        return [tool.schema for tool in self.tools.values()]

    def execute(self, name: str, **kwargs) -> str:
        """执行单个工具"""
        tool = self.tools.get(name)
        if not tool:
            return f"Error: Unknown tool '{name}'"

        # 参数验证
        try:
            tool.validate(**kwargs)
        except ValidationError as e:
            return f"Error: {e}"

        # 权限检查
        if not self._check_permission(tool, kwargs):
            return f"Error: Permission denied"

        # 执行工具
        try:
            return tool.execute(**kwargs)
        except Exception as e:
            return f"Error: {e}"

    def execute_batch(self, calls: List[ToolCall]) -> List[ToolResult]:
        """批量执行工具"""
        results = []
        for call in calls:
            output = self.execute(call.name, **call.arguments)
            results.append(ToolResult(
                id=call.id,
                content=output,
            ))
        return results
```

### 3. Todo Manager (任务管理)

**职责**: 管理任务列表和状态

```python
class TodoManager:
    """
    任务管理器

    特性:
    - 单任务 in_progress 约束
    - 自动提醒机制
    - 状态持久化
    - 进度追踪
    """

    def __init__(self, storage: Storage):
        self.items: List[TodoItem] = []
        self.storage = storage
        self.nag_counter = 0
        self.last_update = time.time()

    def update(self, items: List[dict]) -> str:
        """更新任务列表"""
        # 验证
        validated = self._validate(items)

        # 检查约束
        in_progress = [i for i in validated if i.status == "in_progress"]
        if len(in_progress) > 1:
            raise ValueError("Only one task can be in_progress")

        # 更新
        self.items = validated
        self.nag_counter = 0
        self.last_update = time.time()

        # 持久化
        self.storage.save(self.items)

        # 渲染
        return self._render()

    def should_nag(self) -> bool:
        """判断是否需要提醒"""
        self.nag_counter += 1
        return self.nag_counter >= 3

    def get_progress(self) -> float:
        """获取总体进度"""
        if not self.items:
            return 0.0
        completed = sum(1 for i in self.items if i.status == "completed")
        return completed / len(self.items)
```

### 4. Context Manager (上下文管理)

**职责**: 管理对话上下文和 Token 使用

```python
class ContextManager:
    """
    上下文管理器

    特性:
    - Token 统计
    - 自动压缩
    - 历史归档
    - 智能裁剪
    """

    def __init__(self, max_tokens: int = 100000):
        self.max_tokens = max_tokens
        self.compression_strategy = CompressionStrategy()

    def maybe_compress(self, messages: List[Message]):
        """可能压缩上下文"""
        current_tokens = self._count_tokens(messages)

        if current_tokens > self.max_tokens * 0.8:
            self._compress(messages)

    def _compress(self, messages: List[Message]):
        """压缩上下文"""
        # 策略 1: 压缩旧的工具结果
        # 策略 2: 摘要长对话
        # 策略 3: 移除低优先级内容
        self.compression_strategy.apply(messages)

    def _count_tokens(self, messages: List[Message]) -> int:
        """统计 Token 数量"""
        return sum(msg.token_count for msg in messages)
```

### 5. Code Analyzer (代码分析器)

**职责**: 分析和理解代码库

```python
class CodeAnalyzer:
    """
    代码分析器

    功能:
    - 项目结构分析
    - 代码搜索
    - 依赖分析
    - 代码度量
    """

    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.indexer = CodeIndexer(workspace)
        self.searcher = CodeSearcher(workspace)

    def analyze_structure(self) -> ProjectStructure:
        """分析项目结构"""
        return ProjectStructure(
            files=self._scan_files(),
            directories=self._scan_directories(),
            languages=self._detect_languages(),
            dependencies=self._build_dependency_graph(),
        )

    def search(self, query: str, pattern: str = None) -> List[Match]:
        """搜索代码"""
        if pattern:
            return self.searcher.regex_search(pattern)
        return self.searcher.semantic_search(query)

    def get_dependencies(self, path: str) -> DependencyGraph:
        """获取依赖关系"""
        return self.indexer.build_graph(path)
```

---

## 数据流设计

### 请求流程

```
┌─────────┐
│  User   │
└────┬────┘
     │ query
     ▼
┌─────────────┐
│   UI Layer  │
└────┬────────┘
     │ HTTP/WS
     ▼
┌─────────────┐
│ API Gateway │
└────┬────────┘
     │ route
     ▼
┌─────────────┐
│Agent Loop   │
│             │◄────┐
└────┬────────┘     │
     │ chat         │
     ▼              │
┌─────────────┐     │
│  LLM Client │─────┘
└────┬────────┘
     │ response
     ▼
┌─────────────┐
│Tool Dispatch│
└────┬────────┘
     │ execute
     ▼
┌─────────────┐
│   Tools     │
├─────────────┤
│ • bash      │
│ • read_file │
│ • write_file│
│ • edit_file │
│ • search    │
└─────────────┘
```

### 数据模型

```typescript
// 核心消息类型
interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string | ContentBlock[];
  timestamp?: number;
}

interface ContentBlock {
  type: 'text' | 'tool_use' | 'tool_result';
  text?: string;
  tool_use?: ToolUse;
  tool_result?: ToolResult;
}

// 工具调用
interface ToolUse {
  id: string;
  name: string;
  input: Record<string, any>;
}

interface ToolResult {
  id: string;
  content: string;
  error?: boolean;
}

// 任务项
interface TodoItem {
  id: string;
  text: string;
  status: 'pending' | 'in_progress' | 'completed';
  created_at: number;
}

// 项目结构
interface ProjectStructure {
  files: FileInfo[];
  directories: DirectoryInfo[];
  languages: string[];
  dependencies: DependencyGraph;
}
```

---

## 工具系统架构

### 工具定义

```python
from abc import ABC, abstractmethod
from typing import Any, Dict

class Tool(ABC):
    """工具基类"""

    @property
    @abstractmethod
    def name(self) -> str:
        """工具名称"""
        pass

    @property
    @abstractmethod
    def schema(self) -> dict:
        """工具 Schema (JSON Schema)"""
        pass

    @abstractmethod
    def execute(self, **kwargs) -> str:
        """执行工具"""
        pass

    def validate(self, **kwargs):
        """验证参数"""
        # 使用 JSON Schema 验证
        jsonschema.validate(kwargs, self.schema)
```

### 内置工具

```python
# Bash 工具
class BashTool(Tool):
    name = "bash"
    schema = {
        "type": "object",
        "properties": {
            "command": {"type": "string"},
            "timeout": {"type": "number", "default": 120},
        },
        "required": ["command"],
    }

    def execute(self, command: str, timeout: int = 120) -> str:
        # 安全检查
        if self._is_dangerous(command):
            return "Error: Dangerous command blocked"

        # 执行命令
        result = subprocess.run(
            command,
            shell=True,
            timeout=timeout,
            capture_output=True,
        )

        return result.stdout + result.stderr

# 文件读取工具
class ReadFileTool(Tool):
    name = "read_file"
    schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string"},
            "limit": {"type": "integer"},
        },
        "required": ["path"],
    }

    def execute(self, path: str, limit: int = None) -> str:
        # 路径安全检查
        full_path = self._safe_path(path)

        # 读取文件
        content = full_path.read_text()

        # 限制行数
        if limit:
            lines = content.splitlines()[:limit]
            content = "\n".join(lines)

        return content[:50000]  # 限制大小
```

### 工具安全

```python
class SecuritySandbox:
    """
    安全沙箱

    特性:
    - 路径隔离
    - 命令过滤
    - 资源限制
    """

    def __init__(self, workspace: Path):
        self.workspace = workspace.resolve()

    def safe_path(self, path: str) -> Path:
        """获取安全路径"""
        full_path = (self.workspace / path).resolve()

        # 检查是否逃逸
        if not full_path.is_relative_to(self.workspace):
            raise SecurityError(f"Path escapes workspace: {path}")

        return full_path

    def is_dangerous_command(self, command: str) -> bool:
        """检查危险命令"""
        dangerous = [
            "rm -rf /",
            "rm -rf /*",
            "sudo",
            "shutdown",
            "reboot",
            "> /dev/",
            ":(){ :|:& };:",  # fork bomb
        ]

        return any(d in command for d in dangerous)
```

---

## 多语言实现对比

### Python 实现

```python
# 优势
# • AI 库丰富
# • 快速开发
# • 易于测试

class AgentLoop:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools

    def run(self, query: str) -> str:
        messages = [{"role": "user", "content": query}]

        while True:
            response = self.llm.chat(messages, self.tools.schemas)
            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason != "tool_use":
                break

            results = self.tools.execute_all(response.tool_calls)
            messages.append({"role": "user", "content": results})

        return response.content
```

### TypeScript 实现

```typescript
// 优势
// • 类型安全
// • 全栈统一
// • 生态成熟

interface AgentLoop {
  llm: LLMClient;
  tools: ToolDispatcher;
}

class AgentLoop implements AgentLoop {
  constructor(llm: LLMClient, tools: ToolDispatcher) {
    this.llm = llm;
    this.tools = tools;
  }

  async run(query: string): Promise<string> {
    const messages: Message[] = [{ role: 'user', content: query }];

    while (true) {
      const response = await this.llm.chat(
        messages,
        this.tools.schemas
      );

      messages.push({ role: 'assistant', content: response.content });

      if (response.stopReason !== 'tool_use') {
        break;
      }

      const results = await this.tools.executeAll(response.toolCalls);
      messages.push({ role: 'user', content: results });
    }

    return response.content;
  }
}
```

### Rust 实现

```rust
// 优势
// • 极致性能
// • 内存安全
// • 并发优秀

pub struct AgentLoop {
    llm: Box<dyn LLMClient>,
    tools: ToolDispatcher,
}

impl AgentLoop {
    pub fn new(llm: Box<dyn LLMClient>, tools: ToolDispatcher) -> Self {
        Self { llm, tools }
    }

    pub fn run(&mut self, query: &str) -> Result<String, Error> {
        let mut messages = vec![Message::user(query)];

        loop {
            let response = self.llm.chat(&messages, &self.tools.schemas())?;
            messages.push(Message::assistant(response.content.clone()));

            if response.stop_reason != StopReason::ToolUse {
                break;
            }

            let results = self.tools.execute_all(&response.tool_calls)?;
            messages.push(Message::tool_results(results));
        }

        Ok(response.content)
    }
}
```

---

## 安全设计

### 安全层次

```
┌─────────────────────────────────────────────────────────────┐
│                    应用层安全                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  权限检查    │  │  输入验证    │  │  输出过滤    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    沙箱层安全                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  路径隔离    │  │  命令过滤    │  │  资源限制    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    系统层安全                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  文件权限    │  │  进程隔离    │  │  网络隔离    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 安全检查清单

- [ ] 路径遍历防护
- [ ] 命令注入防护
- [ ] 资源限制 (CPU, 内存, 磁盘)
- [ ] API 密钥保护
- [ ] 敏感数据过滤
- [ ] 审计日志

---

## 性能优化

### 优化策略

1. **并发执行**: 工具调用可以并发执行
2. **缓存机制**: 缓存文件内容和搜索结果
3. **流式响应**: 支持流式输出
4. **连接池**: 复用 HTTP 连接
5. **懒加载**: 按需加载大型依赖

### 性能指标

| 指标 | 目标值 | 测量方法 |
|------|--------|----------|
| 首次响应 | < 2s | 时间戳差值 |
| 工具执行 | < 500ms | 工具计时 |
| 内存使用 | < 500MB | 内存分析 |
| CPU 使用 | < 50% | 系统监控 |

---

## 扩展性设计

### 插件系统

```python
class Plugin:
    """插件基类"""

    @property
    def name(self) -> str:
        pass

    @property
    def version(self) -> str:
        pass

    def register_tools(self, dispatcher: ToolDispatcher):
        """注册工具"""
        pass

    def on_agent_start(self, context: AgentContext):
        """代理启动钩子"""
        pass

    def on_agent_stop(self, context: AgentContext):
        """代理停止钩子"""
        pass
```

### 自定义工具

```python
# 用户可以定义自己的工具
class CustomTool(Tool):
    name = "custom_tool"
    schema = {
        "type": "object",
        "properties": {
            "param1": {"type": "string"},
        },
        "required": ["param1"],
    }

    def execute(self, param1: str) -> str:
        # 自定义逻辑
        return f"Processed: {param1}"

# 注册工具
dispatcher.register(CustomTool())
```

---

## 总结

本架构设计遵循以下原则：

1. **简洁性**: 核心逻辑清晰，易于理解
2. **模块化**: 组件独立，便于替换
3. **可扩展**: 支持插件和自定义工具
4. **安全性**: 多层安全防护
5. **性能**: 支持并发和缓存

通过这个架构，我们可以构建一个功能强大、易于使用的 AI 编程助手。
