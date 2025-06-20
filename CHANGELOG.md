# 更新日志

本文档记录了Download Assistant MCP项目的所有重要更改。

格式基于[Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循[语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2024-12-19

### 新增 ✨
- 重构为通用文件下载MCP工具
- 采用面向对象架构设计，提取BaseDownloader基类
- 支持任意类型文件下载（HTML、CSS、JS、文档、音视频、图片等）
- 添加完整的测试套件，包含单元测试、集成测试
- 增强安全机制：URL验证、文件类型检查、路径安全
- 支持批量下载和重试机制
- 添加文件信息获取功能
- 完善的配置管理系统

### 改进 🚀
- 优化代码结构，减少重复代码
- 改进错误处理和日志记录
- 增强性能：流式下载、并发控制
- 统一项目元数据和依赖管理
- 完善文档和开发指南

### 修复 🐛
- 修复文件路径安全问题
- 修复内存泄漏问题
- 修复并发下载时的竞态条件

### 安全 🔒
- 添加SSRF攻击防护
- 实现路径遍历攻击防护
- 增加文件类型白名单验证
- 添加文件大小和磁盘空间检查

### 文档 📚
- 重写README.md，添加详细的使用说明
- 添加CONTRIBUTING.md开发指南
- 添加完整的API文档
- 添加故障排除指南

### 测试 🧪
- 添加配置模块测试
- 添加工具函数测试
- 添加下载器基类测试
- 添加文件下载器测试
- 添加图片下载器测试
- 添加集成测试
- 配置测试覆盖率报告

### 开发工具 🛠️
- 配置Black代码格式化
- 配置isort导入排序
- 配置flake8代码检查
- 配置mypy类型检查
- 配置pytest测试框架
- 添加pre-commit钩子配置

## [0.1.0] - 2024-12-11

### 新增 ✨
- 初始项目创建
- 基础图片下载功能
- FastMCP集成
- 基本配置管理

### 已知问题 ⚠️
- 代码重复较多
- 缺少测试覆盖
- 文档不完整
- 安全机制不足

---

## 版本说明

### 版本号格式
本项目使用[语义化版本](https://semver.org/lang/zh-CN/)格式：`主版本号.次版本号.修订号`

- **主版本号**：不兼容的API更改
- **次版本号**：向后兼容的功能添加
- **修订号**：向后兼容的错误修复

### 更改类型
- `新增` - 新功能
- `改进` - 现有功能的改进
- `修复` - 错误修复
- `安全` - 安全相关的修复
- `文档` - 文档更新
- `测试` - 测试相关更改
- `开发工具` - 开发工具和流程改进
- `移除` - 移除的功能
- `废弃` - 即将移除的功能

### 发布周期
- **主版本**：根据需要发布，通常包含重大架构更改
- **次版本**：每月发布，包含新功能和改进
- **修订版本**：根据需要发布，主要用于错误修复

### 支持政策
- **当前版本**：完全支持，包含新功能和错误修复
- **前一个主版本**：仅提供安全更新和关键错误修复
- **更早版本**：不再提供支持

### 迁移指南
重大版本更新时，我们会提供详细的迁移指南，包括：
- 破坏性更改列表
- 迁移步骤说明
- 代码示例
- 常见问题解答

### 反馈和建议
如果您对版本发布有任何建议或发现问题，请通过以下方式联系我们：
- 创建GitHub Issue
- 参与GitHub Discussions
- 提交Pull Request