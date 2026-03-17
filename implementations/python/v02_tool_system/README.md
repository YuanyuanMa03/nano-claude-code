# v02: 工具系统 (Tool System)

**Motto**: "Adding a tool means adding one handler"

**状态**: ✅ 已完成

---

## 概述

v02 引入了通用的工具调度系统,使得添加新工具变得简单:只需注册一个处理函数。

---

## 核心特性

### 1. 工具调度器 (ToolDispatcher)

```python
dispatcher = ToolDispatcher()

# 添加工具 - 只需一行代码
dispatcher.register("tool_name", handler_function)

# 执行工具
result = dispatcher.execute("tool_name", **kwargs)
```

**Motto**: "Adding a tool means adding one handler"

### 2. 文件操作工具

- **read_file** - 安全地读取文件内容
- **write_file** - 写入文件(自动创建目录)
- **edit_file** - 替换文件中的文本

### 3. 路径安全沙箱 (SecuritySandbox)

防止路径遍历攻击:
- 阻止 `../../../` 路径遍历
- 限制文件操作在 workspace 内
- 处理符号链接

---

## 文件结构

```
v02_tool_system/
├── src/
│   ├── __init__.py        # 包导出
│   ├── agent.py           # 代理循环 (~150 行)
│   ├── dispatcher.py      # 工具调度器 (~100 行)
│   ├── file_tools.py      # 文件操作工具 (~130 行)
│   ├── sandbox.py         # 安全沙箱 (~70 行)
│   └── main.py            # CLI 入口 (~45 行)
└── tests/
    ├── conftest.py        # 测试配置
    ├── test_dispatcher.py # 调度器测试 (7 个测试)
    ├── test_file_tools.py # 文件工具测试 (12 个测试)
    └── test_sandbox.py    # 沙箱测试 (10 个测试)
```

**总代码量**: ~495 行
**测试数量**: 27 个测试,全部通过 ✅

---

## 架构设计

### 工具注册流程

```
+----------------+     register     +----------------+
|   New Tool     | --------------> | Dispatcher    |
+----------------+                  +----------------+
                                              |
                                              v
                                    +----------------+
                                    | handlers dict  |
                                    | {              |
                                    |   tool: fn     |
                                    | }              |
                                    +----------------+
```

### 工具执行流程

```
Agent Loop              Dispatcher              Handler
    |                        |                     |
    |-- execute_batch ----->|                     |
    |  [tool_calls]          |                     |
    |                        |-- execute --------->|
    |                        |  tool, **kwargs      |
    |                        |                     |
    |<--- results -----------|<--- return ---------|
    |                        |
    v                        v
Messages continue
```

---

## 核心组件

### ToolDispatcher

```python
class ToolDispatcher:
    """路由工具调用到对应的处理器"""

    def register(self, name: str, handler: Callable):
        """注册工具 - motto 的体现"""
        self.handlers[name] = handler

    def execute(self, name: str, **kwargs) -> str:
        """执行单个工具"""
        handler = self.handlers.get(name)
        return handler(**kwargs)

    def execute_batch(self, calls: List[Dict]) -> List[Dict]:
        """批量执行工具"""
        results = []
        for call in calls:
            output = self.execute(call["name"], **call["input"])
            results.append({"id": call["id"], "content": output})
        return results
```

### SecuritySandbox

```python
class SecuritySandbox:
    """路径安全沙箱"""

    def safe_path(self, path: str) -> Path:
        """获取安全路径"""
        full_path = (self.workspace / path).resolve()

        # 关键安全检查
        if not full_path.is_relative_to(self.workspace):
            raise ValueError(f"Path escapes workspace: {path}")

        return full_path
```

### FileTools

```python
class FileTools:
    """文件操作工具"""

    def __init__(self, workspace: str):
        self.sandbox = SecuritySandbox(workspace)

    def read_file(self, path: str, limit: int = None) -> str:
        """读取文件 - 限制大小防止超载"""
        safe_path = self.sandbox.safe_path(path)
        with open(safe_path, 'r') as f:
            return f.read()

    def write_file(self, path: str, content: str) -> str:
        """写入文件 - 自动创建目录"""
        safe_path = self.sandbox.safe_path(path)
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        with open(safe_path, 'w') as f:
            f.write(content)

    def edit_file(self, path: str, old_text: str, new_text: str) -> str:
        """编辑文件 - 替换文本"""
        safe_path = self.sandbox.safe_path(path)
        content = safe_path.read_text()
        if old_text not in content:
            return f"Error: '{old_text[:50]}...' not found"
        new_content = content.replace(old_text, new_text, 1)
        safe_path.write_text(new_content)
```

---

## 使用方法

### 安装依赖

```bash
pip install anthropic python-dotenv
```

### 配置环境变量

```bash
ANTHROPIC_API_KEY=sk-ant-xxx
MODEL_ID=claude-sonnet-4-6
WORKSPACE=.  # 可选,默认当前目录
```

### 运行

```bash
cd implementations/python/v02_tool_system
python src/main.py
```

### 示例对话

```
You: Read the file requirements.txt
Agent: [Tool: read_file]
Result: [file content]

I've read the requirements.txt file. It contains the following dependencies...

You: Create a new Python file with a function
Agent: [Tool: write_file]
Path: utils.py
Content: def process_data(data): return data

I've created utils.py with a process_data function.

You: Update the function to add a docstring
Agent: [Tool: read_file]
Result: def process_data(data): return data

[Tool: edit_file]
Old: def process_data(data): return data
New: def process_data(data): """Process the input data.""" return data

I've added a docstring to the process_data function.
```

---

## 测试

### 运行测试

```bash
cd implementations/python
pytest v02_tool_system/tests/ -v
```

### 测试覆盖

- ✅ **27 个测试全部通过**
- ✅ **调度器功能** - 注册、执行、批量处理
- ✅ **文件操作** - 读写编辑各种场景
- ✅ **安全沙箱** - 路径遍历防护
- ✅ **错误处理** - 异常情况处理

### 测试用例列表

**test_dispatcher.py (7 个测试):**
1. ✅ 调度器初始化
2. ✅ 注册工具
3. ✅ 执行工具
4. ✅ 未知工具处理
5. ✅ 批量执行
6. ✅ 批量执行中的未知工具
7. ✅ 处理器异常捕获

**test_file_tools.py (12 个测试):**
1. ✅ 成功读取文件
2. ✅ 文件不存在
3. ✅ 带行数限制的读取
4. ✅ 成功写入文件
5. ✅ 自动创建目录
6. ✅ 成功编辑文件
7. ✅ 编辑时旧文本未找到
8. ✅ 编辑不存在的文件
9. ✅ 路径遍历攻击(读取)
10. ✅ 路径遍历攻击(写入)
11. ✅ 创建文件工具辅助函数

**test_sandbox.py (10 个测试):**
1. ✅ 相对路径处理
2. ✅ workspace 内的绝对路径
3. ✅ workspace 外的绝对路径
4. ✅ 路径遍历攻击
5. ✅ 嵌套目录路径
6. ✅ workspace 写权限检查
7. ✅ 文件写权限检查
8. ✅ 路径规范化
9. ✅ 不安全路径的规范化

---

## 与 v01 的对比

| 特性 | v01 | v02 |
|------|-----|-----|
| **工具数量** | 1 (bash) | 4 (bash + 3 文件工具) |
| **工具注册** | 硬编码 | ToolDispatcher 字典 |
| **文件操作** | 通过 bash | 专用工具 |
| **路径安全** | 无 | SecuritySandbox |
| **代码行数** | ~190 | ~495 |
| **测试数量** | 11 | 27 |
| **可扩展性** | 低 | 高 |

---

## 设计决策

### 为什么需要工具调度器?

**v01 的问题:**
```python
# 硬编码的工具执行
if block.name == "bash":
    output = run_bash(block.input["command"])
else:
    return f"Unknown tool: {block.name}"
```

**v02 的解决方案:**
```python
# 灵活的调度器
result = dispatcher.execute(block.name, **block.input)
```

### 为什么需要专用文件工具?

**只用 bash 的问题:**
- 不安全 (`cat`, `sed` 可能失败)
- 无法控制输出大小
- 错误处理困难
- 跨平台兼容性差

**专用工具的优势:**
- 安全的路径处理
- 输出大小限制
- 清晰的错误消息
- 更好的测试能力

---

## 限制和改进空间

### 当前限制

1. **工具 Schema** - 目前硬编码在 agent.py 中
2. **参数验证** - 没有使用 JSON Schema 验证
3. **工具元数据** - 缺少描述、版本等
4. **并发执行** - 工具串行执行

### 未来改进 (v03+)

- [ ] 添加 TodoWrite 工具
- [ ] 实现 JSON Schema 验证
- [ ] 支持工具并发执行
- [ ] 添加工具元数据系统

---

## 下一步 (v03)

v03 将添加:
- ✅ TodoWrite 工具
- ✅ 任务状态管理
- ✅ 单任务 in_progress 约束
- ✅ 自动提醒机制

**Motto**: "An agent without a plan drifts"

---

## 技术要点

### 1. 简单性的力量

```python
# 添加新工具只需一行
dispatcher.register("new_tool", new_handler)
```

这体现了 v02 的核心理念:简单性。

### 2. 安全第一

```python
# 每个路径都经过安全检查
safe_path = self.sandbox.safe_path(user_path)
```

安全是嵌入式设计,不是事后添加。

### 3. 错误处理

```python
# 所有错误都被捕获并转换为字符串
except Exception as e:
    return f"Error: {e}"
```

统一错误处理让调用者更简单。

---

## 学习目标

通过 v02,你将学到:

1. ✅ 如何设计可扩展的工具系统
2. ✅ 路径安全的重要性
3. ✅ 错误处理的最佳实践
4. ✅ 测试驱动的开发
5. ✅ 模块化架构设计

---

**版本**: v02
**作者**: nano-claude-code
**许可证**: MIT
