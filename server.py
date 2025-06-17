from fastmcp import FastMCP
from file_downloader import FileDownloader
from config import Config
import logging
import json
import os
from typing import Union, List
from pathlib import Path

# 初始化配置和组件
config = Config()
app = FastMCP("download-assistant")
file_downloader = FileDownloader(config)

# 配置日志
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建日志目录
log_dir = os.path.dirname(config.LOG_FILE)
if log_dir:
    os.makedirs(log_dir, exist_ok=True)



def _download_files_impl(
    urls: Union[str, List[str]],
    filenames: Union[str, List[str]],
    output_dir: str,
    max_concurrent: int = 20,
    overwrite: bool = False,
    timeout: int = 30,
    retry_count: int = 2,
    max_file_size: int = 100,
    check_file_type: bool = True,
    validate_image: bool = False
) -> str:
    """
    下载任意类型文件到指定路径，支持多文件一起下载
    
    Args:
        urls: 文件URL（字符串）或URL列表（数组）
        filenames: 文件名（字符串）或文件名列表（数组），需与urls对应
        output_dir: 保存目录路径
        max_concurrent: 多文件下载时的最大并发数，默认20（当前为顺序下载）
        overwrite: 是否覆盖已存在文件，默认False
        timeout: 下载超时时间（秒），默认30
        retry_count: 失败重试次数，默认2
        max_file_size: 最大文件大小（MB），默认100
        check_file_type: 是否检查文件类型安全性，默认True
        validate_image: 是否对图片文件进行完整性验证，默认False
    
    Returns:
        JSON格式的下载结果报告
    """
    try:
        # 验证参数匹配
        if isinstance(urls, str) and isinstance(filenames, str):
            # 单个文件下载
            output_path = os.path.join(output_dir, filenames)
            logger.info(f"开始下载文件: {urls}")
            result = file_downloader.download_file(
                urls, output_path, overwrite, timeout, max_file_size, check_file_type, validate_image
            )
            logger.info(f"下载完成: {output_path}")
            
            if result['status'] == 'success':
                return f"下载成功: {result['filepath']}\n文件类型: {result.get('content_type', 'unknown')}\n文件大小: {result['size']} 字节"
            elif result['status'] == 'skipped':
                return f"文件已存在，跳过下载: {result['filepath']}"
            else:
                return f"下载失败: {result['error']}"
                
        elif isinstance(urls, list) and isinstance(filenames, list):
            # 批量下载
            if len(urls) != len(filenames):
                return json.dumps({
                    "success": False,
                    "error": "URLs和文件名数量不匹配",
                    "urls_count": len(urls),
                    "filenames_count": len(filenames)
                })
            
            logger.info(f"开始批量下载 {len(urls)} 个文件到: {output_dir}")
            
            # 使用顺序下载避免事件循环冲突
            result = file_downloader.batch_download_sequential(
                urls, filenames, output_dir, overwrite, timeout, retry_count, max_file_size,
                check_file_type=check_file_type, validate_image=validate_image
            )
            
            # 格式化返回结果
            if len(urls) == 1:
                detail = result['details'][0]
                if detail['status'] == 'success':
                    return f"下载成功: {detail['filepath']}\n文件类型: {detail.get('content_type', 'unknown')}\n文件大小: {detail['size']} 字节"
                elif detail['status'] == 'skipped':
                    return f"文件已存在，跳过下载: {detail['filepath']}"
                else:
                    return f"下载失败: {detail['error']}"
            else:
                summary = (
                    f"批量文件下载完成！\n"
                    f"总计: {result['total']} 个文件\n"
                    f"成功: {result['success']} 个\n"
                    f"失败: {result['failed']} 个\n"
                    f"跳过: {result['skipped']} 个\n"
                    f"耗时: {result['duration']:.2f} 秒"
                )
                
                if result['success'] > 0 and result['duration'] > 0:
                    summary += f"\n平均速度: {result['success']/result['duration']:.2f} 个/秒"
                
                logger.info(summary)
                return summary
        else:
            return json.dumps({
                "success": False,
                "error": "参数类型不匹配：urls和filenames必须都是字符串或都是列表"
            })
        
    except Exception as e:
        error_msg = f"文件下载失败: {str(e)}"
        logger.error(error_msg)
        return error_msg

def _get_file_info_impl(url: str, timeout: int = 30, get_image_details: bool = False) -> str:
    """
    获取文件基本信息

    Args:
        url: 文件URL
        timeout: 请求超时时间（秒），默认30
        get_image_details: 是否获取图片详细信息（尺寸、格式等），默认False

    Returns:
        文件信息（类型、大小等）
    """
    try:
        logger.info(f"获取文件信息: {url}")

        # 如果需要图片详细信息，使用图片信息获取方法
        if get_image_details:
            info = file_downloader.get_image_info(url, timeout)
        else:
            info = file_downloader.get_file_info(url, timeout)

        if 'error' in info:
            return f"获取文件信息失败: {info['error']}"

        result = f"文件信息:\n"
        result += f"URL: {info['url']}\n"
        result += f"内容类型: {info['content_type']}\n"

        if info.get('file_extension'):
            result += f"文件扩展名: {info['file_extension']}\n"

        # 图片特定信息
        if info.get('is_image'):
            result += f"文件类型: 图片\n"
            if info.get('format'):
                result += f"图片格式: {info['format']}\n"
            if info.get('width') and info.get('height'):
                result += f"图片尺寸: {info['width']}x{info['height']}\n"

        if info.get('file_size_mb'):
            result += f"文件大小: {info['file_size_mb']} MB\n"
        elif info.get('file_size_bytes'):
            result += f"文件大小: {info['file_size_bytes']} 字节\n"

        if not info.get('is_image'):
            result += f"文件类型安全: {'是' if info.get('is_safe_type', False) else '否'}"

        return result

    except Exception as e:
        error_msg = f"获取文件信息失败: {str(e)}"
        logger.error(error_msg)
        return error_msg

# MCP tool wrappers
@app.tool()
def download_files(
    urls: Union[str, List[str]],
    filenames: Union[str, List[str]],
    output_dir: str,
    max_concurrent: int = 20,
    overwrite: bool = False,
    timeout: int = 30,
    retry_count: int = 2,
    max_file_size: int = 100,
    check_file_type: bool = True,
    validate_image: bool = False
) -> str:
    """
    下载任意类型文件到指定路径，支持多文件一起下载

    Args:
        urls: 文件URL（字符串）或URL列表（数组）
        filenames: 文件名（字符串）或文件名列表（数组），需与urls对应
        output_dir: 保存目录路径
        max_concurrent: 多文件下载时的最大并发数，默认20（当前为顺序下载）
        overwrite: 是否覆盖已存在文件，默认False
        timeout: 下载超时时间（秒），默认30
        retry_count: 失败重试次数，默认2
        max_file_size: 最大文件大小（MB），默认100
        check_file_type: 是否检查文件类型安全性，默认True
        validate_image: 是否对图片文件进行完整性验证，默认False

    Returns:
        JSON格式的下载结果报告
    """
    return _download_files_impl(urls, filenames, output_dir, max_concurrent, overwrite, timeout, retry_count, max_file_size, check_file_type, validate_image)

@app.tool()
def get_file_info(url: str, timeout: int = 30, get_image_details: bool = False) -> str:
    """
    获取文件基本信息

    Args:
        url: 文件URL
        timeout: 请求超时时间（秒），默认30
        get_image_details: 是否获取图片详细信息（尺寸、格式等），默认False

    Returns:
        文件信息（类型、大小等）
    """
    return _get_file_info_impl(url, timeout, get_image_details)

if __name__ == "__main__":
    logger.info("启动媒体工具MCP服务器...")
    logger.info(f"配置信息: {config.to_dict()}")
    app.run()