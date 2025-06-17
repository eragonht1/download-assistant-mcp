import os
import re
import validators
from urllib.parse import urlparse
from typing import Optional

def validate_url(url: str, allow_localhost: bool = False, allow_private_ips: bool = False) -> bool:
    """验证URL格式和安全性"""
    # 先检查基本的URL格式
    try:
        parsed = urlparse(url)
        # 只允许http和https协议
        if parsed.scheme not in ['http', 'https']:
            return False
        # 必须有hostname
        if not parsed.hostname:
            return False
    except Exception:
        return False

    # 使用validators库进行更严格的验证，但对localhost特殊处理
    hostname = parsed.hostname
    if hostname not in ['localhost', '127.0.0.1']:
        # 对于非localhost的URL，使用validators库验证
        if not validators.url(url):
            return False

    # 防止访问内网地址（除非明确允许）
    if hostname:
        # 检查localhost
        if hostname in ['localhost', '127.0.0.1'] and not allow_localhost:
            return False
        # 检查私有IP
        if (hostname.startswith('192.168.') or hostname.startswith('10.') or hostname.startswith('172.')) and not allow_private_ips:
            return False

    return True

def sanitize_path(path: str) -> str:
    """清理和验证文件路径，防止路径遍历攻击"""
    # 移除危险字符
    path = path.replace('..', '').replace('//', '/')
    # 转换为绝对路径
    path = os.path.abspath(path)
    return path

def sanitize_filename(filename: str) -> str:
    """清理文件名中的危险字符"""
    # 移除或替换危险字符 (注意转义反斜杠)
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # 限制文件名长度
    if len(filename) > 100:
        name, ext = os.path.splitext(filename)
        filename = name[:95] + ext
    return filename

def get_extension_from_url(url: str) -> str:
    """从URL推断文件扩展名"""
    parsed = urlparse(url)
    path = parsed.path.lower()

    # 特殊处理常见图片扩展名
    if path.endswith(('.jpg', '.jpeg')):
        return '.jpg'
    elif path.endswith('.png'):
        return '.png'
    elif path.endswith('.gif'):
        return '.gif'
    elif path.endswith('.webp'):
        return '.webp'

    # 尝试从URL路径中提取其他扩展名
    if '.' in path:
        ext = os.path.splitext(path)[1]
        if ext and ext != '.unknown':
            return ext

    # 如果没有扩展名或是未知扩展名，返回默认的.jpg
    return '.jpg'

def generate_filename_from_url(url: str, index: int) -> str:
    """从URL生成文件名"""
    # 尝试从URL获取原始文件名
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)
    
    # 如果URL中有有效的文件名，使用它
    if filename and '.' in filename and len(filename) < 100:
        # 清理文件名中的特殊字符
        filename = sanitize_filename(filename)
        return filename
    else:
        # 否则使用序号命名
        ext = get_extension_from_url(url)
        if not ext:
            ext = '.jpg'  # 默认图片扩展名
        return f"image_{index:04d}{ext}"

def format_file_size(size_bytes: int) -> str:
    """格式化文件大小显示"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"

def ensure_safe_path(file_path: str, base_dir: Optional[str] = None) -> Optional[str]:
    """确保文件路径安全，防止路径遍历攻击

    Args:
        file_path: 要验证的文件路径
        base_dir: 基础目录，如果提供则确保路径在此目录下

    Returns:
        安全的绝对路径，如果路径不安全则返回None
    """
    try:
        # 检查原始路径是否包含路径遍历攻击
        if '..' in file_path:
            return None

        # 清理路径
        clean_path = os.path.abspath(file_path)

        # 如果指定了基础目录，确保路径在基础目录下
        if base_dir:
            base_dir = os.path.abspath(base_dir)
            if not clean_path.startswith(base_dir):
                return None

        return clean_path

    except Exception:
        return None