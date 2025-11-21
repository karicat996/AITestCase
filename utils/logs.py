# logs.py
import sys
from pathlib import Path
from loguru import logger
from datetime import datetime, timedelta


class LogManager:
    def __init__(self, log_dir="logs", retention_days=30):
        """
        初始化日志管理器

        Args:
            log_dir (str): 日志存储目录
            retention_days (int): 日志保留天数，默认30天
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
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

    def _add_file_handlers(self):
        """添加不同级别的文件日志处理器"""
        # DEBUG级别日志
        logger.add(
            self.log_dir / "debug_{time:YYYY-MM-DD}.log",
            level="DEBUG",
            rotation="00:00",
            retention=f"{self.retention_days} days",
            encoding="utf-8"
        )

        # INFO级别日志
        logger.add(
            self.log_dir / "info_{time:YYYY-MM-DD}.log",
            level="INFO",
            rotation="00:00",
            retention=f"{self.retention_days} days",
            encoding="utf-8"
        )

        # WARNING级别日志
        logger.add(
            self.log_dir / "warning_{time:YYYY-MM-DD}.log",
            level="WARNING",
            rotation="00:00",
            retention=f"{self.retention_days} days",
            encoding="utf-8"
        )

        # ERROR级别日志
        logger.add(
            self.log_dir / "error_{time:YYYY-MM-DD}.log",
            level="ERROR",
            rotation="00:00",
            retention=f"{self.retention_days} days",
            encoding="utf-8"
        )

    def _clean_old_logs(self):
        """清理过期日志文件"""
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)

        for log_file in self.log_dir.glob("*.log"):
            if log_file.stat().st_mtime < cutoff_date.timestamp():
                log_file.unlink(missing_ok=True)


# 创建全局实例
log_manager = LogManager()

# 导出logger对象供其他模块使用
log = logger
