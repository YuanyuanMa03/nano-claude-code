# v01: 最小循环 (Minimal Loop)

**Motto**: "One loop & Bash is all you need"

**状态**: ✅ 已完成

---

## 概述

v01 是 nano-claude-code 的第一个版本，实现了最基础的 AI 编程助手核心循环。这个版本展示了代理系统的最本质特征：**循环执行**直到完成任务。

---

## 核心特性

### 1. 代理循环 (Agent Loop)

实现了一个完整的 `while` 循环，包含以下步骤：

1. **发送消息给 LLM** - 将用户查询和工具定义发送给模型
2. **检查 stop_reason** - 判断模型是否需要使用工具
3. **执行工具** - 如果需要，运行 bash 工具
4. **收集结果** - 将工具输出添加到消息列表
5. **循环返回** - 重复步骤 1，直到任务完成

### 2. Bash 工具

实现了基础的 bash 工具，可以：
- 执行任意 shell 命令
- 设置超时限制（默认 120 秒）
- 捕获 stdout 和 stderr
- 处理执行错误

---

## 文件结构

```
v01_minimal_loop/
├── src/
│   ├── __init__.py       # 包初始化
│   ├── agent.py          # 代理循环核心 (~120 行)
│   ├── bash_tool.py      # Bash 工具实现 (~25 行)
│   └── main.py           # 命令行入口 (~45 行)
└── tests/
    ├── conftest.py       # 测试配置
    ├── test_agent.py     # 代理测试
    └── test_bash_tool.py # 工具测试
```

**总代码量**: ~190 行

---

## 架构设计

### 数据流

```
User Query
    │
    ▼
┌─────────────────┐
│  Agent Loop     │◄─────┐
│                 │      │
│  1. Call LLM    │      │
│     │           │      │
│     ▼           │      │
│  2. Check       │      │
│     stop_reason │      │
│     │           │      │
│     ├─ No ──► Return  │
│     │                   │
│     ├─ Yes ──► 3. Run  │
│     │              bash │
│     │                 ││
│     └─────────────────┘│
│              4. Append │
│                 results│
└────────────────────────┘
```

### 核心组件

#### AgentLoop 类

```python
class AgentLoop:
    def __init__(self, api_key: str, model: str):
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.tools = [bash_tool_schema]

    def run(self, user_query: str) -> str:
        # 核心循环逻辑
        while True:
            response = self.client.messages.create(...)
            if response.stop_reason != "tool_use":
                break
            # 执行工具并继续循环
```

---

## 使用方法

### 安装依赖

```bash
pip install anthropic python-dotenv
```

### 配置环境变量

创建 `.env` 文件：

```bash
ANTHROPIC_API_KEY=sk-ant-xxx
MODEL_ID=claude-sonnet-4-6  # 可选
```

### 运行

```bash
cd implementations/python/v01_minimal_loop
python src/main.py
```

### 示例对话

```
You: Create a file called hello.py
Agent: I'll create a hello.py file for you.

[Tool: bash]
Command: touch hello.py

I've created the file hello.py.

You: Now write a Python function in it
Agent: I'll add a simple function to hello.py.

[Tool: bash]
Command: echo 'def greet(name): return f"Hello, {name}!"' > hello.py

I've added a greet function to hello.py.

You: Verify the file content
Agent: I'll read the file to verify.

[Tool: bash]
Command: cat hello.py

def greet(name): return f"Hello, {name}!"

The file contains the greet function as expected.
```

---

## 测试

### 运行测试

```bash
cd implementations/python/v01_minimal_loop
pytest tests/ -v
```

### 测试覆盖

- ✅ Bash 工具执行
- ✅ 命令超时处理
- ✅ 错误处理
- ✅ 代理循环逻辑
- ✅ 工具调用流程
- ✅ 文本提取

---

## 限制

当前版本的限制：

1. **单一工具** - 只有 bash 工具
2. **无文件操作** - 文件操作需要通过 bash 命令
3. **无任务规划** - 没有 Todo 系统
4. **无代码理解** - 不能分析项目结构
5. **无上下文管理** - 长对话可能超限

这些限制将在后续版本中逐步解决。

---

## 下一步 (v02)

v02 将添加：
- ✅ 工具调度系统
- ✅ 文件操作工具 (read_file, write_file, edit_file)
- ✅ 路径安全沙箱

---

## 技术要点

### 1. stop_reason 的关键作用

`stop_reason` 是循环控制的核心：
- `tool_use` - 需要执行工具，继续循环
- `end_turn` - 模型完成响应，退出循环
- `max_tokens` - 达到 token 限制，退出循环

### 2. 消息累积

每次循环都会：
1. 将助手响应添加到消息列表
2. 将工具结果添加到消息列表
3. 将完整消息列表发送给 LLM

这保持了完整的对话上下文。

### 3. 工具结果格式

工具结果必须使用特定格式：

```python
{
    "type": "tool_result",
    "tool_use_id": block.id,  # 匹配 tool_use 的 id
    "content": "实际输出"
}
```

---

## 学习目标

通过 v01，你将学到：

1. ✅ 如何实现一个基本的代理循环
2. ✅ 如何与 Anthropic API 交互
3. ✅ 如何处理工具调用
4. ✅ 如何构建可测试的代码
5. ✅ 如何设计清晰的模块结构

---

**版本**: v01
**作者**: nano-claude-code
**许可证**: MIT
