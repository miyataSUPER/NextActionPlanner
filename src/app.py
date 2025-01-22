"""
メインアプリケーションモジュール

このモジュールは、Streamlitベースのユーザーインターフェースを提供します。
"""

import streamlit as st
from core.audio import AudioProcessor
from core.text import TextProcessor
from api.gemini import GeminiClient
from db.operations import Database
from utils.logger import setup_logging
from utils.config import app_config 
