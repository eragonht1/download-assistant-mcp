# Download Assistant MCP - Makefile
# 自动化常见开发任务

.PHONY: help install install-dev test test-cov lint format type-check clean build docs serve

# 默认目标
help:
	@echo "Download Assistant MCP - 可用命令:"
	@echo ""
	@echo "  install      - 安装项目依赖"
	@echo "  install-dev  - 安装开发依赖"
	@echo "  test         - 运行测试"
	@echo "  test-cov     - 运行测试并生成覆盖率报告"
	@echo "  lint         - 运行代码检查"
	@echo "  format       - 格式化代码"
	@echo "  type-check   - 运行类型检查"
	@echo "  clean        - 清理临时文件"
	@echo "  build        - 构建项目"
	@echo "  docs         - 生成文档"
	@echo "  serve        - 启动MCP服务器"
	@echo ""

# 安装依赖
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

# 测试
test:
	pytest -v

test-cov:
	pytest --cov=. --cov-report=html --cov-report=term-missing

test-watch:
	pytest-watch

# 代码质量
lint:
	flake8 .
	mypy .

format:
	black .
	isort .

type-check:
	mypy .

# 清理
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

# 构建
build: clean
	python -m build

# 文档
docs:
	@echo "生成API文档..."
	@echo "文档已在README.md中提供"

# 服务器
serve:
	python server.py

# 开发环境设置
setup-dev: install-dev
	@echo "开发环境设置完成!"
	@echo "运行 'make test' 验证安装"

# 发布前检查
pre-release: format lint test-cov
	@echo "发布前检查完成!"

# 快速检查
check: format lint test
	@echo "快速检查完成!"

# 全面检查
full-check: clean install-dev format lint type-check test-cov
	@echo "全面检查完成!"