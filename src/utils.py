"""
ユーティリティモジュール

このモジュールは、ログ設定などの共通機能を提供します。
"""

import logging


def setup_logging():
    """
    アプリケーションのログ設定を行います。
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ) 
