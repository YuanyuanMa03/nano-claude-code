# Python 会话 (Sessions)

这个目录包含了 nano-claude-code 的交互式学习会话,每个会话演示一个特定的核心概念。

## 会话列表

### v01_session.py - 最小循环 (Minimal Loop)
**Motto**: "One loop & Bash is all you need"

演示核心代理循环:
- `stop_reason` 机制
- 工具执行和结果反馈
- 最小可行代理

```bash
ANTHROPIC_API_KEY=xxx python v01_session.py
```

**学习目标:**
- 理解为什么 `stop_reason` 是循环控制的关键
- 看到工具结果如何反馈到模型
- 实现最简单的可用代理

### v02_session.py - 工具系统 (Tool System)
**Motto**: "Adding a tool means adding one handler"

演示工具调度系统:
- 工具注册和调度
- 文件操作工具
- 路径安全沙箱

```bash
ANTHROPIC_API_KEY=xxx python v02_session.py
```

**学习目标:**
- 如何实现可扩展的工具系统
- 为什么要用专用工具而不是 bash
- 路径安全的重要性

### v03_session.py - 任务规划 (Task Planning)
**Motto**: "An agent without a plan drifts"

演示 Todo 管理系统:
- TodoWrite 工具
- 单任务 in_progress 约束
- 自动提醒机制

```bash
ANTHROPIC_API_KEY=xxx python v03_session.py
```

**学习目标:**
- 为什么任务规划很重要
- 如何实现约束和提醒
- Todo 状态管理

### v04_session.py - 代码理解 (Code Understanding)
**Motto**: "Understand before you change"

演示代码分析能力:
- 项目结构分析
- 代码搜索
- 依赖关系图

```bash
ANTHROPIC_API_KEY=xxx python v04_session.py
```

**学习目标:**
- 如何让代理理解代码库
- 搜索和索引技术
- 依赖分析基础

## 使用方法

### 1. 设置环境变量

创建 `.env` 文件:

```bash
ANTHROPIC_API_KEY=sk-ant-xxx
MODEL_ID=claude-sonnet-4-6
# ANTHROPIC_BASE_URL=https://api.anthropic.com  # 可选
```

### 2. 运行会话

```bash
# 进入会话目录
cd implementations/python/sessions

# 运行特定会话
ANTHROPIC_API_KEY=xxx python v01_session.py
```

### 3. 交互式体验

每个会话都提供交互式命令行界面,你可以:
- 尝试示例任务
- 输入自己的任务
- 观察代理的决策过程
- 学习核心概念

## 与 learn-claude-code 的区别

| 特性 | learn-claude-code | nano-claude-code |
|------|------------------|------------------|
| **目标** | 教学理解 | 实用工具 |
| **复杂度** | 12 个会话,包含高级特性 | ~10 个版本,聚焦核心 |
| **代码风格** | 教学导向,强调清晰 | 实用导向,强调健壮性 |
| **会话** | 独立脚本,渐进式学习 | 版本实现,可增量升级 |

## 会话设计原则

1. **自包含**: 每个会话都是完整的可运行脚本
2. **教育性**: 包含详细注释和学习目标
3. **实用性**: 每个版本都是真正可用的工具
4. **渐进式**: 从简单到复杂,逐步构建

## 下一步

完成会话学习后,查看具体的实现版本:
- `v01_minimal_loop/` - v01 的完整实现
- `v02_tool_system/` - v02 的完整实现
- ...

这些实现包含:
- 模块化代码结构
- 完整的单元测试
- 生产级错误处理
- 详细的文档
