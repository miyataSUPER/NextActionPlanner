"""
設定管理モジュール

このモジュールは、環境変数やアプリケーション設定を管理します。
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class DatabaseConfig:
    """データベース設定"""
    user: str = os.getenv('DB_USER', 'postgres')
    password: str = os.getenv('DB_PASSWORD', 'password')
    host: str = os.getenv('DB_HOST', 'db')
    port: str = os.getenv('DB_PORT', '5432')
    name: str = os.getenv('DB_NAME', 'action_db')


@dataclass
class AppConfig:
    """アプリケーション設定"""
    debug: bool = os.getenv('DEBUG', 'false').lower() == 'true'
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    max_video_size: int = int(os.getenv('MAX_VIDEO_SIZE', 104857600))
    max_text_length: int = int(os.getenv('MAX_TEXT_LENGTH', 30000))
    whisper_model: str = os.getenv('WHISPER_MODEL', 'base')
    language: str = os.getenv('LANGUAGE', 'ja')
    gemini_api_key: Optional[str] = os.getenv('GEMINI_API_KEY')


# グローバル設定インスタンス
db_config = DatabaseConfig()
app_config = AppConfig() 
