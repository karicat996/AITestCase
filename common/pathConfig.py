# -*- coding: utf-8 -*-
"""
路径配置集中管理模块

设计原则：
1. 单例模式，全局只读取一次 systemConfig.yaml
2. 统一提供项目路径常量（默认输出目录、日志目录等）
3. 提供 resolve_path 方法实现「传参优先 → 配置默认 → 抛异常」三级回退
"""
import os
from pathlib import Path
from loguru import logger

from common.fileProcessor import fileProcessor
from utils.logs import LogManager


# ==================== 项目根路径常量 ====================
# common/ 的父目录即为项目根目录 D:\AIGeneration
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 默认输出目录
DEFAULT_OUTPUT_DIR = str(PROJECT_ROOT / "testcase")

# 日志目录
DEFAULT_LOG_DIR = str(PROJECT_ROOT / "utils" / "logs")

# 配置文件路径
CONFIG_FILE = str(PROJECT_ROOT / "config" / "systemConfig.yaml")

# 初始化日志管理器（只初始化一次，LogManager 内部有 _initialized 防重入）
LogManager(log_dir=DEFAULT_LOG_DIR)


class PathConfig:
    """
    路径配置管理器（单例）

    全局只读取一次 systemConfig.yaml，后续通过缓存提供配置项。
    所有需要路径的类应通过此类获取默认值或调用 resolve_path。
    """

    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if PathConfig._config is None:
            self._load_config()

    def _load_config(self):
        """读取 systemConfig.yaml，结果缓存到类变量"""
        try:
            fp = fileProcessor()
            config = fp.find_and_read_file(
                "config/systemConfig.yaml", type="yaml"
            )
            PathConfig._config = config if config else {}
            logger.debug("PathConfig: 配置文件加载完成")
        except Exception as e:
            logger.error(f"PathConfig: 加载配置文件失败: {e}")
            PathConfig._config = {}

    # ==================== 属性访问 ====================

    @property
    def config(self) -> dict:
        """返回完整配置字典"""
        return PathConfig._config

    def get(self, key: str, default=None):
        """获取单个配置项"""
        return PathConfig._config.get(key, default)

    # ==================== 路径解析核心方法 ====================

    @staticmethod
    def resolve_path(
        path_param,
        config_key=None,
        raise_if_missing=True,
        name="路径"
    ):
        """
        三级回退路径解析：传参 → 配置默认 → 抛异常

        Args:
            path_param:    调用方传入的路径参数（优先级最高）
            config_key:    systemConfig.yaml 中的键名（第二优先级）
            raise_if_missing: 当传参与配置都不存在时是否抛异常
            name:          路径名称，用于异常提示信息

        Returns:
            str: 解析后的路径

        Raises:
            ValueError: 当 path_param 和 config_key 对应的配置都为空，
                        且 raise_if_missing=True 时
        """
        # 第一优先级：传入参数（非空字符串）
        if path_param and isinstance(path_param, str) and path_param.strip():
            return path_param

        # 第二优先级：配置文件默认值
        if config_key:
            config_val = PathConfig._config.get(config_key) if PathConfig._config else None
            if config_val and isinstance(config_val, str) and config_val.strip():
                return config_val

        # 第三级：抛异常或返回 None
        if raise_if_missing:
            hint = f"（配置键: {config_key}）" if config_key else ""
            raise ValueError(
                f"{name}未配置，请传入路径参数或在 systemConfig.yaml 中设置{hint}"
            )
        return None

    @staticmethod
    def resolve_output_dir(output_dir_param=None):
        """
        解析输出目录：传参 → 配置 OUTPUT_JSON_PATH 的目录 → 默认 testcase 目录

        Args:
            output_dir_param: 传入的输出目录参数

        Returns:
            str: 输出目录绝对路径
        """
        if output_dir_param and isinstance(output_dir_param, str) and output_dir_param.strip():
            dir_path = output_dir_param
        else:
            # 尝试从配置的 OUTPUT_JSON_PATH 推导目录
            config_path = PathConfig._config.get("OUTPUT_JSON_PATH") if PathConfig._config else None
            if config_path and isinstance(config_path, str) and config_path.strip():
                dir_path = os.path.dirname(config_path)
            else:
                dir_path = DEFAULT_OUTPUT_DIR

        os.makedirs(dir_path, exist_ok=True)
        return dir_path


# ==================== 模块级单例 ====================
path_config = PathConfig()
