# 贡献指南

感谢您对Download Assistant MCP项目的关注！本文档将帮助您了解如何为项目做出贡献。

## 🚀 快速开始

### 开发环境设置

1. **克隆项目**
```bash
git clone https://github.com/eragonht1/download-assistant-mcp.git
cd download-assistant-mcp
```

2. **创建虚拟环境**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows
```

3. **安装开发依赖**
```bash
pip install -e ".[dev]"
```

4. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件设置开发配置
```

## 🧪 开发流程

### 代码规范

我们使用以下工具确保代码质量：

- **Black**: 代码格式化
- **isort**: 导入排序
- **flake8**: 代码风格检查
- **mypy**: 类型检查
- **pytest**: 单元测试

### 提交前检查

在提交代码前，请运行以下命令：

```bash
# 格式化代码
black .
isort .

# 检查代码风格
flake8

# 类型检查
mypy .

# 运行测试
pytest

# 生成测试覆盖率报告
pytest --cov=. --cov-report=html
```

### Git工作流

1. **创建特性分支**
```bash
git checkout -b feature/your-feature-name
```

2. **进行开发**
   - 编写代码
   - 添加测试
   - 更新文档

3. **提交更改**
```bash
git add .
git commit -m "feat: add your feature description"
```

4. **推送分支**
```bash
git push origin feature/your-feature-name
```

5. **创建Pull Request**

### 提交信息规范

我们使用[Conventional Commits](https://www.conventionalcommits.org/)规范：

- `feat:` 新功能
- `fix:` 错误修复
- `docs:` 文档更新
- `style:` 代码格式化
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具的变动

示例：
```
feat: add batch download progress tracking
fix: handle network timeout in file downloader
docs: update API documentation
test: add unit tests for config module
```

## 🏗️ 架构指南

### 代码组织

```
download-assistant-mcp/
├── base_downloader.py     # 抽象基类
├── file_downloader.py     # 具体实现
├── utils.py               # 工具函数
├── config.py              # 配置管理
├── server.py              # MCP服务器
└── tests/                 # 测试文件
```

### 设计原则

1. **单一职责原则**: 每个类和函数只负责一个功能
2. **开闭原则**: 对扩展开放，对修改关闭
3. **里氏替换原则**: 子类可以替换父类
4. **接口隔离原则**: 使用小而专一的接口
5. **依赖倒置原则**: 依赖抽象而不是具体实现

### 添加新功能

#### 1. 添加新的下载器类型

```python
from base_downloader import BaseDownloader

class VideoDownloader(BaseDownloader):
    """视频文件下载器"""
    
    def _validate_file_type(self, response, url, **kwargs):
        content_type = response.headers.get('content-type', '')
        return content_type.startswith('video/')
    
    def _post_download_validation(self, output_path, **kwargs):
        # 验证视频文件完整性
        pass
```

#### 2. 添加新的MCP工具

```python
@app.tool()
def download_videos(urls, filenames, output_dir, **kwargs):
    """下载视频文件"""
    video_downloader = VideoDownloader(config)
    return video_downloader.batch_download_sequential(
        urls, filenames, output_dir, **kwargs
    )
```

#### 3. 添加工具函数

在`utils.py`中添加新函数：

```python
def validate_video_url(url: str) -> bool:
    """验证视频URL"""
    # 实现验证逻辑
    pass
```

## 🧪 测试指南

### 测试结构

```
tests/
├── conftest.py              # 测试配置和fixtures
├── test_config.py           # 配置模块测试
├── test_utils.py            # 工具函数测试
├── test_base_downloader.py  # 基类测试
├── test_file_downloader.py  # 文件下载器测试
└── test_integration.py      # 集成测试
```

### 编写测试

1. **单元测试**: 测试单个函数或方法
2. **集成测试**: 测试模块间的交互
3. **Mock测试**: 使用mock对象模拟外部依赖

示例测试：

```python
def test_download_file_success(file_downloader, temp_dir, mock_response):
    """测试文件下载成功"""
    with patch('requests.Session.get', return_value=mock_response):
        result = file_downloader.download_file(
            'http://example.com/test.txt',
            os.path.join(temp_dir, 'test.txt')
        )
        assert result['status'] == 'success'
```

### 测试覆盖率

目标测试覆盖率：**90%+**

运行覆盖率检查：
```bash
pytest --cov=. --cov-report=html --cov-fail-under=90
```

## 📚 文档指南

### 文档类型

1. **API文档**: 函数和类的docstring
2. **用户文档**: README.md
3. **开发文档**: CONTRIBUTING.md
4. **变更日志**: CHANGELOG.md

### Docstring规范

使用Google风格的docstring：

```python
def download_file(self, url: str, output_path: str, **kwargs) -> Dict[str, Any]:
    """下载单个文件到指定路径.
    
    Args:
        url: 文件URL
        output_path: 输出文件路径
        **kwargs: 其他参数
        
    Returns:
        包含下载结果的字典
        
    Raises:
        ValueError: 当URL无效时
        IOError: 当文件写入失败时
    """
```

## 🐛 问题报告

### Bug报告

请包含以下信息：

1. **环境信息**: Python版本、操作系统
2. **重现步骤**: 详细的操作步骤
3. **期望行为**: 应该发生什么
4. **实际行为**: 实际发生了什么
5. **错误日志**: 相关的错误信息
6. **配置信息**: 相关的配置设置

### 功能请求

请包含以下信息：

1. **用例描述**: 为什么需要这个功能
2. **解决方案**: 建议的实现方式
3. **替代方案**: 其他可能的解决方案
4. **影响评估**: 对现有功能的影响

## 🎯 发布流程

### 版本号规范

使用[语义化版本](https://semver.org/)：

- `MAJOR.MINOR.PATCH`
- `MAJOR`: 不兼容的API更改
- `MINOR`: 向后兼容的功能添加
- `PATCH`: 向后兼容的错误修复

### 发布检查清单

- [ ] 所有测试通过
- [ ] 代码覆盖率达标
- [ ] 文档更新完整
- [ ] 变更日志更新
- [ ] 版本号更新
- [ ] 标签创建

## 💬 社区

### 沟通渠道

- **GitHub Issues**: 问题报告和功能请求
- **GitHub Discussions**: 一般讨论和问答
- **Pull Requests**: 代码贡献

### 行为准则

我们致力于创建一个友好、包容的社区环境。请遵循以下原则：

1. **尊重他人**: 尊重不同的观点和经验
2. **建设性反馈**: 提供有用的、建设性的反馈
3. **协作精神**: 乐于帮助他人和接受帮助
4. **专业态度**: 保持专业和友好的交流方式

感谢您的贡献！🎉