# nano-claude-code 多语言实现指南

**版本**: 1.0.0
**更新日期**: 2026-03-17

---

## 📋 目录

- [多语言策略](#多语言策略)
- [语言特性对比](#语言特性对比)
- [实现规范](#实现规范)
- [代码示例对比](#代码示例对比)
- [测试策略](#测试策略)
- [文档规范](#文档规范)

---

## 多语言策略

### 为什么多语言?

1. **学习价值**: 对比不同语言实现，深入理解每种语言特性
2. **用户选择**: 用户可以选择熟悉的语言版本
3. **场景适配**: 不同场景适合不同语言（Python vs Rust）
4. **社区贡献**: 降低贡献门槛，吸引更多开发者

### 实现原则

```
功能对等 + 保持特色
    ↓
┌─────────────┬─────────────┬─────────────┐
│  Python     │ TypeScript  │    Rust     │
├─────────────┼─────────────┼─────────────┤
│• 快速开发   │• 类型安全   │• 极致性能   │
│• AI 库丰富  │• 全栈统一   │• 内存安全   │
│• 易于测试   │• 前端集成   │• 并发优秀   │
└─────────────┴─────────────┴─────────────┘
```

### 版本对应关系

```
每个语言实现相同的版本：

v01: 最小循环
├── implementations/python/v01_minimal_loop/
├── implementations/typescript/v01_minimal_loop/
└── implementations/rust/v01_minimal_loop/

v02: 工具系统
├── implementations/python/v02_tool_system/
├── implementations/typescript/v02_tool_system/
└── implementations/rust/v02_tool_system/

... (依此类推)
```

---

## 语言特性对比

### 类型系统

| 特性 | Python | TypeScript | Rust |
|------|--------|------------|------|
| **类型** | 动态 | 静态 (可选) | 静态 (强) |
| **类型推断** | 有限 | 强大 | 强大 |
| **泛型** | 有 (PEP 484) | 完整 | 完整 |
| **类型检查** | mypy (可选) | 编译时 | 编译时 |
| **示例** | `def f(x: int) -> int:` | `function f(x: number): number` | `fn f(x: i32) -> i32` |

### 错误处理

| 特性 | Python | TypeScript | Rust |
|------|--------|------------|------|
| **机制** | 异常 | 异常 | Result<T,E> |
| **强制处理** | 否 | 否 | 是 |
| **模式匹配** | match (3.10+) | switch (pattern) | match |
| **示例** | `try/except` | `try/catch` | `match result?` |

### 并发模型

| 特性 | Python | TypeScript | Rust |
|------|--------|------------|------|
| **异步** | async/await | async/await | async/await |
| **线程** | threading | Worker threads | std::thread |
| **GIL** | 有 | 无 | 无 |
| **性能** | 中 | 高 | 极高 |

### 生态系统

| 特性 | Python | TypeScript | Rust |
|------|--------|------------|------|
| **包管理** | pip | npm/yarn | cargo |
| **AI 库** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Web 库** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **系统库** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **学习曲线** | 低 | 中 | 高 |

---

## 实现规范

### 目录结构规范

```
implementations/{language}/
├── README.md              # 语言特定说明
├── {config}               # 配置文件 (package.json, Cargo.toml, etc.)
├── v01_minimal_loop/      # 版本 01
│   ├── README.md          # 版本说明
│   ├── src/               # 源代码
│   │   └── main.{ext}     # 主文件
│   ├── tests/             # 测试
│   └── docs/              # 文档
├── v02_tool_system/       # 版本 02
│   └── ...
└── ...                    # 其他版本
```

### 命名规范

| 类型 | Python | TypeScript | Rust |
|------|--------|------------|------|
| **文件** | `snake_case.py` | `kebab-case.ts` | `snake_case.rs` |
| **类/接口** | `PascalCase` | `PascalCase` | `PascalCase` |
| **函数** | `snake_case` | `camelCase` | `snake_case` |
| **常量** | `UPPER_SNAKE` | `UPPER_SNAKE` | `UPPER_SNAKE` |
| **私有** | `_leading` | private | pub(crate) |

### 代码风格

```python
# Python (PEP 8)
class AgentLoop:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def run(self, query: str) -> str:
        messages = [Message.user(query)]
        # ...
```

```typescript
// TypeScript (Standard Style)
class AgentLoop {
  constructor(private llm: LLMClient) {}

  run(query: string): string {
    const messages: Message[] = [{ role: 'user', content: query }];
    // ...
  }
}
```

```rust
// Rust (Standard Style)
pub struct AgentLoop {
    llm: Box<dyn LLMClient>,
}

impl AgentLoop {
    pub fn run(&mut self, query: &str) -> Result<String, Error> {
        let messages = vec![Message::user(query)];
        // ...
    }
}
```

---

## 代码示例对比

### 1. Agent Loop 核心循环

#### Python

```python
def agent_loop(messages: List[Message]) -> None:
    while True:
        response = llm.chat(messages, tools)
        messages.append(Message.assistant(response.content))

        if response.stop_reason != "tool_use":
            break

        results = tools.execute_all(response.tool_calls)
        messages.append(Message.tool_results(results))
```

#### TypeScript

```typescript
async function agentLoop(messages: Message[]): Promise<void> {
  while (true) {
    const response = await llm.chat(messages, tools);
    messages.push({ role: 'assistant', content: response.content });

    if (response.stopReason !== 'toolUse') {
      break;
    }

    const results = await tools.executeAll(response.toolCalls);
    messages.push({ role: 'user', content: results });
  }
}
```

#### Rust

```rust
fn agent_loop(messages: &mut Vec<Message>) -> Result<(), Error> {
    loop {
        let response = llm.chat(messages, &tools)?;
        messages.push(Message::assistant(response.content.clone()));

        if response.stop_reason != StopReason::ToolUse {
            break;
        }

        let results = tools.execute_all(&response.tool_calls)?;
        messages.push(Message::tool_results(results));
    }
    Ok(())
}
```

### 2. 工具调度器

#### Python

```python
class ToolDispatcher:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self.tools[tool.name] = tool

    def execute(self, name: str, **kwargs) -> str:
        tool = self.tools.get(name)
        if not tool:
            return f"Unknown tool: {name}"
        return tool.execute(**kwargs)
```

#### TypeScript

```typescript
class ToolDispatcher {
  private tools: Map<string, Tool> = new Map();

  register(tool: Tool): void {
    this.tools.set(tool.name, tool);
  }

  execute(name: string, args: Record<string, any>): string {
    const tool = this.tools.get(name);
    if (!tool) {
      return `Unknown tool: ${name}`;
    }
    return tool.execute(args);
  }
}
```

#### Rust

```rust
pub struct ToolDispatcher {
    tools: HashMap<String, Box<dyn Tool>>,
}

impl ToolDispatcher {
    pub fn register(&mut self, tool: Box<dyn Tool>) {
        self.tools.insert(tool.name().to_string(), tool);
    }

    pub fn execute(&self, name: &str, args: Value) -> Result<String, Error> {
        match self.tools.get(name) {
            Some(tool) => tool.execute(args),
            None => Ok(format!("Unknown tool: {}", name)),
        }
    }
}
```

### 3. Todo 管理器

#### Python

```python
class TodoManager:
    def update(self, items: List[dict]) -> str:
        validated = []
        in_progress = 0

        for item in items:
            status = item.get("status", "pending")
            if status == "in_progress":
                in_progress += 1
            validated.append(TodoItem(**item))

        if in_progress > 1:
            raise ValueError("Only one task can be in_progress")

        self.items = validated
        return self.render()
```

#### TypeScript

```typescript
class TodoManager {
  update(items: TodoItemInput[]): string {
    const validated: TodoItem[] = [];
    let inProgress = 0;

    for (const item of items) {
      const status = item.status || 'pending';
      if (status === 'in_progress') {
        inProgress++;
      }
      validated.push({ ...item, status });
    }

    if (inProgress > 1) {
      throw new Error('Only one task can be in_progress');
    }

    this.items = validated;
    return this.render();
  }
}
```

#### Rust

```rust
impl TodoManager {
    pub fn update(&mut self, items: Vec<TodoItemInput>) -> Result<String, Error> {
        let mut validated = Vec::new();
        let mut in_progress = 0;

        for item in items {
            let status = item.status.unwrap_or(Status::Pending);
            if status == Status::InProgress {
                in_progress += 1;
            }
            validated.push(TodoItem::from(item));
        }

        if in_progress > 1 {
            return Err(Error::MultipleInProgress);
        }

        self.items = validated;
        Ok(self.render())
    }
}
```

---

## 测试策略

### 测试覆盖率目标

| 语言 | 单元测试 | 集成测试 | 端到端测试 |
|------|----------|----------|------------|
| Python | > 80% | > 60% | > 40% |
| TypeScript | > 80% | > 60% | > 40% |
| Rust | > 90% | > 70% | > 50% |

### 测试框架

| 语言 | 单元测试 | 集成测试 | Mock/Stub |
|------|----------|----------|-----------|
| Python | pytest | pytest | pytest-mock |
| TypeScript | Jest | Jest | jest.mock |
| Rust | built-in | built-in | mockito |

### 测试示例

#### Python

```python
# tests/test_agent_loop.py
import pytest
from agent import AgentLoop

def test_agent_loop_single_turn(mock_llm):
    loop = AgentLoop(mock_llm)
    response = loop.run("Hello")
    assert "response" in response

def test_agent_loop_tool_call(mock_llm, mock_tools):
    loop = AgentLoop(mock_llm, mock_tools)
    response = loop.run("Execute bash command")
    mock_tools.execute.assert_called_once()
```

#### TypeScript

```typescript
// tests/agentLoop.test.ts
import { AgentLoop } from '../src/agentLoop';

describe('AgentLoop', () => {
  it('should handle single turn', async () => {
    const loop = new AgentLoop(mockLLM);
    const response = await loop.run('Hello');
    expect(response).toContain('response');
  });

  it('should execute tools', async () => {
    const loop = new AgentLoop(mockLLM, mockTools);
    await loop.run('Execute bash command');
    expect(mockTools.execute).toHaveBeenCalledTimes(1);
  });
});
```

#### Rust

```rust
// tests/agent_loop.rs
use crate::agent::AgentLoop;

#[test]
fn test_single_turn() {
    let mut loop = AgentLoop::new(mock_llm());
    let response = loop.run("Hello").unwrap();
    assert!(response.contains("response"));
}

#[test]
fn test_tool_execution() {
    let mut loop = AgentLoop::new(mock_llm());
    loop.set_tools(mock_tools());
    let _ = loop.run("Execute bash command");
    assert!(mock_tools().execute_was_called());
}
```

---

## 文档规范

### README 结构

```markdown
# nano-claude-code - {Language} Implementation

## 简介
{语言特定说明}

## 安装
```bash
{语言特定安装命令}
```

## 快速开始
```{language}
{代码示例}
```

## 版本列表
- [v01: 最小循环](./v01_minimal_loop/)
- [v02: 工具系统](./v02_tool_system/)
- ...

## 开发
{语言特定开发指南}

## 测试
```bash
{测试命令}
```

## 许可证
MIT
```

### 版本 README 结构

```markdown
# v0{version}: {Title}

> *"{Motto}"*

## 功能
- ✅ {功能 1}
- ✅ {功能 2}

## 运行
```bash
{运行命令}
```

## 测试
```bash
{测试命令}
```

## 下一步
{下一版本链接}
```

### API 文档

| 语言 | 工具 | 位置 |
|------|------|------|
| Python | Sphinx + autodoc | `docs/api/` |
| TypeScript | TypeDoc | `docs/api/` |
| Rust | rustdoc | `docs/api/` |

---

## 贡献指南

### 代码贡献流程

1. Fork 仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 代码审查清单

- [ ] 代码符合语言风格规范
- [ ] 所有测试通过
- [ ] 新功能有测试覆盖
- [ ] 文档已更新
- [ ] 无已知安全漏洞

### 多语言同步

当核心功能更新时：

1. 更新 Python 实现（参考实现）
2. 更新 TypeScript 实现
3. 更新 Rust 实现
4. 更新共享文档
5. 跨语言测试验证

---

## 性能基准

### 基准测试

| 操作 | Python | TypeScript | Rust |
|------|--------|------------|------|
| 启动时间 | ~200ms | ~100ms | ~50ms |
| 内存占用 | ~50MB | ~80MB | ~20MB |
| 单次调用 | ~500ms | ~400ms | ~300ms |
| 并发处理 | 有限 | 良好 | 优秀 |

### 优化建议

**Python**
- 使用 PyPy 加速
- 关键路径使用 Cython
- 多进程利用多核

**TypeScript**
- 使用 worker_threads
- 优化打包体积
- 启用 Tree Shaking

**Rust**
- 使用 release 模式
- 启用 LTO
- 优化热点路径

---

## 总结

多语言实现策略提供了：

1. **灵活性**: 用户可选择最适合的语言
2. **学习价值**: 对比不同语言的实现方式
3. **社区扩大**: 吸引不同技术背景的贡献者
4. **场景适配**: 不同场景使用不同实现

通过统一的接口和规范，确保多语言实现的一致性和可维护性。
