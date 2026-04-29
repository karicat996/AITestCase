# logs.py
import sys
from pathlib import Path
from loguru import logger
from datetime import datetime, timedelta


class LogManager:
    _initialized = False # 防止重复初始化导致日志重复输出

    def __init__(self, log_dir="logs", retention_days=30):
        """
        初始化日志管理器

        Args:
            log_dir (str): 日志存储目录（可以是相对路径或绝对路径）
            retention_days (int): 日志保留天数，默认30天
        """
        if LogManager._initialized:
            return
            
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True) # parents=True 确保多级目录创建
        self.retention_days = retention_days

        # 移除默认的日志处理器
        logger.remove()

        # 添加控制台输出（带颜色）
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                   "<level>{level: <8}</level> | "
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="DEBUG",
            colorize=True
        )

        # 添加文件输出（按日期分割）
        self._add_file_handlers()

        # 启动时清理过期日志
        self._clean_old_logs()
        
        LogManager._initialized = True

    def _add_file_handlers(self):
        """添加文件日志处理器（按日期分割的单一日志文件）"""
        # 使用单个日志文件，包含所有级别的日志
        logger.add(
            self.log_dir / "app_{time:YYYY-MM-DD}.log",
            level="DEBUG",
            rotation="00:00",  # 每天午夜自动切换新文件
            retention=f"{self.retention_days} days",  # 自动删除过期日志
            encoding="utf-8",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            enqueue=True,  # 异步写入，提高性能
            backtrace=True,  # 显示完整的异常堆栈
            diagnose=True  # 显示详细的异常信息
        )

    def _clean_old_logs(self):
        """清理过期日志文件"""
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)

        for log_file in self.log_dir.glob("*.log"):
            if log_file.stat().st_mtime < cutoff_date.timestamp():
                log_file.unlink(missing_ok=True)

