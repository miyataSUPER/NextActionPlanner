"""
ユーティリティモジュールのテスト
"""

import logging
from src.utils import setup_logging


def test_setup_logging():
    """ログ設定のテスト"""
    # 既存のハンドラーをクリア
    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # テスト実行
    setup_logging()
    
    # 検証
    assert logger.level == logging.INFO
    
    # ハンドラーの検証
    handler = logger.handlers[0]
    assert isinstance(handler, logging.StreamHandler)
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    assert handler.formatter._fmt == fmt 
