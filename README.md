# Download Assistant MCP

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[English](#english) | [中文](#chinese)

---

## English

A universal file download assistant based on FastMCP, supporting secure download and batch processing of any file type.

### Features

- **Universal File Download**: Support for any file type with security validation
- **Image Processing**: Built-in image validation and metadata extraction
- **Batch Processing**: Sequential download of multiple files
- **Security First**: File type validation, size limits, and path security
- **MCP Integration**: Seamless integration with AI tools via Model Context Protocol
- **Comprehensive Logging**: Detailed operation logs and error tracking

### Tech Stack

- **Python 3.10+**: Modern Python features support
- **FastMCP 0.2.0+**: Lightweight MCP protocol implementation
- **requests 2.31.0+**: HTTP request handling
- **Pillow 10.0.0+**: Image processing and validation
- **psutil 5.9.0+**: System resource monitoring
- **validators 0.20.0+**: URL format validation

### Quick Start

#### Installation

```bash
# Clone the repository
git clone https://github.com/eragonht1/download-assistant-mcp.git
cd download-assistant-mcp

# Install dependencies
pip install -e .

# Or using uv (recommended)
uv sync
```

#### Basic Usage

```python
# Download a single file
download_files(
    urls="https://example.com/document.pdf",
    filenames="document.pdf",
    output_dir="/downloads"
)

# Download with image validation
download_files(
    urls="https://example.com/photo.jpg",
    filenames="photo.jpg",
    output_dir="/downloads",
    validate_image=True
)

# Get file information
get_file_info("https://example.com/file.zip")

# Get detailed image information
get_file_info("https://example.com/photo.jpg", get_image_details=True)
```

### AI Tool Integration

#### Cursor IDE Configuration

```json
{
  "mcpServers": {
    "download-assistant": {
      "command": "python",
      "args": ["path/to/download-assistant-mcp/server.py"],
      "env": {
        "LOG_LEVEL": "INFO",
        "MAX_FILE_SIZE": "100"
      }
    }
  }
}
```

#### Claude Desktop Configuration

1. Find Claude config file:
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/claude/claude_desktop_config.json`

2. Add MCP server configuration (same as above)

### API Reference

#### `download_files`
Download files with optional image validation.

**Parameters:**
- `urls` (string|array): File URL(s)
- `filenames` (string|array): Filename(s)
- `output_dir` (string): Output directory
- `validate_image` (boolean, optional): Enable image validation

#### `get_file_info`
Get file information with optional image details.

**Parameters:**
- `url` (string): File URL
- `get_image_details` (boolean, optional): Get image metadata

---

## Chinese

基于FastMCP的通用文件下载助手，支持任意类型文件的安全下载和批量处理。

### 特性

- **通用文件下载**: 支持任意类型文件，内置安全验证
- **图片处理增强**: 图片完整性验证和元数据提取
- **批量处理**: 支持多文件顺序下载
- **安全优先**: 文件类型验证、大小限制、路径安全检查
- **MCP集成**: 通过模型上下文协议与AI工具无缝集成
- **完善日志**: 详细的操作日志和错误追踪

### 技术栈

- **Python 3.10+**: 现代Python特性支持
- **FastMCP 0.2.0+**: 轻量级MCP协议实现
- **requests 2.31.0+**: HTTP请求处理
- **Pillow 10.0.0+**: 图片处理和验证
- **psutil 5.9.0+**: 系统资源监控
- **validators 0.20.0+**: URL格式验证

### 快速开始

#### 安装

```bash
# 克隆项目
git clone https://github.com/eragonht1/download-assistant-mcp.git
cd download-assistant-mcp

# 安装依赖
pip install -e .

# 或使用uv (推荐)
uv sync
```

#### 基本使用

```python
# 下载单个文件
download_files(
    urls="https://example.com/document.pdf",
    filenames="document.pdf",
    output_dir="/downloads"
)

# 图片下载并验证
download_files(
    urls="https://example.com/photo.jpg",
    filenames="photo.jpg",
    output_dir="/downloads",
    validate_image=True
)

# 获取文件信息
get_file_info("https://example.com/file.zip")

# 获取图片详细信息
get_file_info("https://example.com/photo.jpg", get_image_details=True)
```

### AI工具集成

#### Cursor IDE 配置

```json
{
  "mcpServers": {
    "download-assistant": {
      "command": "python",
      "args": ["path/to/download-assistant-mcp/server.py"],
      "env": {
        "LOG_LEVEL": "INFO",
        "MAX_FILE_SIZE": "100"
      }
    }
  }
}
```

#### Claude Desktop 配置

1. 找到Claude配置文件：
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/claude/claude_desktop_config.json`

2. 添加MCP服务器配置（同上）

### API参考

#### `download_files`
下载文件，支持图片验证。

**参数:**
- `urls` (string|array): 文件URL
- `filenames` (string|array): 文件名
- `output_dir` (string): 输出目录
- `validate_image` (boolean, 可选): 启用图片验证

#### `get_file_info`
获取文件信息，支持图片详情。

**参数:**
- `url` (string): 文件URL
- `get_image_details` (boolean, 可选): 获取图片元数据

### 项目结构

```
download-assistant-mcp/
├── README.md              # 项目文档
├── LICENSE                # MIT许可证
├── pyproject.toml         # 项目配置和依赖
├── server.py              # MCP服务器主入口
├── base_downloader.py     # 下载器基类
├── file_downloader.py     # 文件下载器实现
├── config.py              # 配置管理
├── utils.py               # 工具函数
├── tests/                 # 测试文件
└── logs/                  # 日志目录
```

### 开发

```bash
# 运行测试
pytest

# 代码格式化
black .

# 类型检查
mypy .
```

### 许可证

MIT License - 查看 [LICENSE](LICENSE) 文件了解详情。