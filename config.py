import os
from typing import Dict, Any

class Config:
    def __init__(self):
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        self.LOG_FILE = os.getenv('LOG_FILE', 'logs/downloader.log')
        self.MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', '100'))
        self.MAX_CONCURRENT = int(os.getenv('MAX_CONCURRENT', '5'))
        self.DEFAULT_TIMEOUT = int(os.getenv('DEFAULT_TIMEOUT', '30'))
        self.ALLOW_LOCALHOST = os.getenv('ALLOW_LOCALHOST', 'false').lower() == 'true'
        self.ALLOW_PRIVATE_IPS = os.getenv('ALLOW_PRIVATE_IPS', 'false').lower() == 'true'
        self.RATE_LIMIT_MB_PER_SEC = float(os.getenv('RATE_LIMIT_MB_PER_SEC', '0'))
        self.SERVER_HOST = os.getenv('SERVER_HOST', 'localhost')
        self.SERVER_PORT = int(os.getenv('SERVER_PORT', '8000'))
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'log_level': self.LOG_LEVEL,
            'max_file_size': self.MAX_FILE_SIZE,
            'max_concurrent': self.MAX_CONCURRENT,
            'default_timeout': self.DEFAULT_TIMEOUT,
            'allow_localhost': self.ALLOW_LOCALHOST,
            'rate_limit': self.RATE_LIMIT_MB_PER_SEC
        }