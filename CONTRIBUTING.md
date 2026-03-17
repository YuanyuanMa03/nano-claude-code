# Contributing to nano-claude-code

感谢你有兴趣为 nano-claude-code 做贡献！

## 贡献方式

### 报告 Bug

在 [GitHub Issues](https://github.com/YuanyuanMa03/nano-claude-code/issues) 提交 Bug 报告时，请包含：

- 清晰的标题和描述
- 复现步骤
- 期望行为 vs 实际行为
- 环境信息（操作系统、语言版本等）
- 相关日志或截图

### 提交功能建议

在提交功能建议前，请先检查：

- 是否已有类似的 Issue
- 是否符合项目目标
- 实现的复杂度

### 代码贡献

#### 开发流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

#### 代码规范

**Python**
- 遵循 PEP 8
- 使用类型提示
- 添加 docstring

**TypeScript**
- 使用 ESLint
- 遵循 Standard Style
- 添加 JSDoc 注释

**Rust**
- 使用 `cargo fmt` 格式化
- 通过 `cargo clippy` 检查
- 添加文档注释

#### 测试要求

- 单元测试覆盖率 > 80%
- 所有测试必须通过
- 新功能必须有测试

#### 提交信息

使用约定式提交：

```
feat: add new feature
fix: fix bug
docs: update documentation
test: add tests
refactor: refactor code
```

---

## 多语言同步

当更新核心功能时，请按以下顺序更新：

1. Python 实现（参考实现）
2. TypeScript 实现
3. Rust 实现
4. 共享文档

---

## 社区准则

- 尊重他人
- 欢迎新手
- 建设性反馈
- 专注技术讨论

---

有任何问题，请在 [Discussions](https://github.com/YuanyuanMa03/nano-claude-code/discussions) 中提问！
