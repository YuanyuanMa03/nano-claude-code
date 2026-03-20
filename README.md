# nano-claude-code

**从 0 到 1 构建实用的 AI 编程助手**

[English](./README.md) | [中文](./README-zh.md)

---

## 📖 项目简介

`nano-claude-code` 是一个轻量级、实用的 AI 编程助手项目，从零开始构建（from 0 to 1）。

### 核心特性

- ✅ **实用工具导向**: 不仅理解原理，更注重实际可用性
- ✅ **渐进式开发**: 从最简单的 MVP 开始，逐步添加功能
- ✅ **多语言实现**: Python、TypeScript、Rust 版本，支持对比学习
- ✅ **双前端**: 桌面 GUI 应用 + Web 应用
- ✅ **多模型支持**: 兼容 Anthropic API 的多个提供商
- ✅ **通用语言支持**: 通过配置支持任意编程语言

---

## 🎯 项目定位

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

**核心差异**: `learn-claude-code` 回答"AI 编程代理是如何工作的？"，而 `nano-claude-code` 回答"如何构建一个实用的 AI 编程助手？"

---

## 🚀 快速开始

### 环境要求

- Python 3.10+ / Node.js 20+ / Rust 1.70+
- ANTHROPIC_API_KEY

### 安装

```bash
# 克隆仓库
git clone https://github.com/YuanyuanMa03/nano-claude-code
cd nano-claude-code

# Python 实现
cd implementations/python/v01_minimal_loop
pip install -r requirements.txt

# 运行
python main.py
```

---

## 📝 使用示例

### Python 实现 (v01)

```bash
cd implementations/python/v01_minimal_loop

# 运行
python main.py
```

**对话示例**:
```
You > 帮我用 Python 写一个斐波那契数列
Agent > 好的，我来为你编写斐波那契数列的实现...
[生成代码]

You > 解释一下这个函数的时间复杂度
Agent > 这个函数的时间复杂度是 O(n)，因为...
[解释]
```

### TypeScript 实现 (v01)

```bash
cd implementations/typescript/v01_minimal_loop

# 安装依赖
npm install

# 运行
npm start
```

### Rust 实现 (v01)

```bash
cd implementations/rust/v01_minimal_loop

# 构建
cargo build --release

# 运行
./target/release/nano-claude-code
```

---

## 🏗️ 架构设计

### 核心循环（v01）

```python
while True:
    # 1. 获取用户输入
    user_input = get_user_input()

    # 2. 调用 LLM
    response = call_llm(user_input, context)

    # 3. 解析响应（是否需要工具调用）
    if needs_tool_call(response):
        # 4. 执行工具
        result = execute_tool(response.tool_name, response.tool_args)

        # 5. 将结果反馈给 LLM
        response = call_llm(user_input, context, tool_result=result)

    # 6. 显示响应
    print(response.message)

    # 7. 更新上下文
    update_context(response)
```

---

## 📚 文档

- [总体设计方案](./docs/plans/2026-03-17-nano-claude-code-design.md)
- [架构设计](./docs/plans/architecture.md)
- [版本演进路线图](./docs/plans/version-roadmap.md)
- [多语言实现指南](./docs/plans/multi-language-guide.md)
- [工具系统设计](./docs/tools-system.md)
- [任务规划算法](./docs/task-planning.md)

---

## 🛣️ 版本路线

```
Phase 1: 核心循环 (v01-v04)
v01: 最小循环 - "One loop & Bash is all you need"
v02: 工具系统 - "Adding a tool means adding one handler"
v03: 任务规划 - "An agent without a plan drifts"
v04: 代码理解 - "Understand before you change"

Phase 2: 实用增强 (v05-v07)
v05: 上下文管理 - "Context will fill up; make room"
v06: 代码生成 - "Generate with intent, not by accident"
v07: 多语言支持 - "Config over code"

Phase 3: 完整体验 (v08-v10)
v08: 持久化 - "State survives sessions"
v09: GUI 前端 - "See what's happening"
v10: 插件系统 - "Extend without modifying"
```

---

## 🏗️ 项目结构

```
nano-claude-code/
├── docs/                      # 共享文档
│   └── plans/               # 设计方案
├── implementations/           # 多语言实现
│   ├── python/              # Python 实现
│   │   ├── v01_minimal_loop/
│   │   ├── v02_tools/
│   │   └── ...
│   ├── typescript/           # TypeScript 实现
│   │   └── v01_minimal_loop/
│   └── rust/                # Rust 实现
│       └── v01_minimal_loop/
├── shared/                    # 共享资源
│   ├── prompts/            # 提示模板
│   └── config/            # 配置示例
├── web/                       # Web 前端
│   └── index.html
└── desktop/                   # 桌面应用
    └── tauri-app/
```

---

## 🔧 配置

### API Key 配置

```bash
# 设置环境变量
export ANTHROPIC_API_KEY=sk-ant-...
```

或在项目根目录创建 `.env` 文件：

```
ANTHROPIC_API_KEY=sk-ant-...
```

### 模型配置

```python
# implementations/python/v01_minimal_loop/config.py
MODEL_CONFIG = {
    'provider': 'anthropic',
    'model': 'claude-3-opus-20240229',
    'max_tokens': 4096,
    'temperature': 0.7
}
```

---

## 🧪 测试

```bash
# Python 测试
cd implementations/python/v01_minimal_loop
pytest tests/

# TypeScript 测试
cd implementations/typescript/v01_minimal_loop
npm test

# Rust 测试
cd implementations/rust/v01_minimal_loop
cargo test
```

---

## 🤝 贡献

欢迎贡献！请查看 [贡献指南](./CONTRIBUTING.md)。

### 开发流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 贡献类型

- 🐛 Bug 修复
- ✨ 新功能
- 📝 文档改进
- 🎨 代码优化
- ⚡ 性能提升
- ✅ 测试覆盖

---

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE)

---

## 🙏 致谢

本项目深受以下项目启发：

- [learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) - 理解代理核心机制
- [OpenClaw](https://github.com/openclaw/openclaw) - 实用的 AI 助手框架
- [Claude](https://www.anthropic.com/claude) - 强大的 AI 模型

---

## 📊 对比其他项目

| 特性 | learn-claude-code | nano-claude-code | OpenClaw |
|------|------------------|------------------|-----------|
| **定位** | 教学项目 | 实用工具 | 生产级框架 |
| **代码量** | 简单 | 中等 | 复杂 |
| **功能完整性** | 基础 | 完整 | 企业级 |
| **多语言支持** | 单语言 | ✅ 多语言 | 单语言 |
| **GUI 前端** | ❌ | ✅ | ✅ |
| **Web 前端** | ❌ | ✅ | ✅ |
| **插件系统** | ❌ | 规划中 | ✅ |
| **适合人群** | 学习原理 | 日常使用 | 专业开发 |

---

**"从 0 到 1，构建你自己的 AI 编程助手"** 🚀

---

**当前版本**: v0.1.0
**维护者**: [YuanyuanMa03](https://github.com/YuanyuanMa03)
**许可证**: MIT
