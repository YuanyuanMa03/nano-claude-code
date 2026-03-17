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

## 📚 文档

- [总体设计方案](./docs/plans/2026-03-17-nano-claude-code-design.md)
- [架构设计](./docs/plans/architecture.md)
- [版本演进路线图](./docs/plans/version-roadmap.md)
- [多语言实现指南](./docs/plans/multi-language-guide.md)

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
├── implementations/           # 多语言实现
│   ├── python/
│   ├── typescript/
│   └── rust/
├── shared/                    # 共享资源
├── web/                       # Web 前端
└── desktop/                   # 桌面应用
```

---

## 🤝 贡献

欢迎贡献！请查看 [贡献指南](./CONTRIBUTING.md)

---

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE)

---

## 🙏 致谢

本项目深受 [learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) 启发

---

**"从 0 到 1，构建你自己的 AI 编程助手"**
