"""
音声処理モジュールのテスト
"""

import pytest
from unittest.mock import Mock, patch
from src.audio_processor import AudioProcessor
import tempfile
import os


@pytest.fixture
def mock_whisper():
    """Whisperモデルのモック"""
    with patch('src.audio_processor.whisper') as mock:
        model = Mock()
        model.transcribe.return_value = {"text": "テスト音声のテキスト"}
        mock.load_model.return_value = model
        yield mock


def test_process_video_file(mock_whisper):
    """動画ファイル処理のテスト"""
    # テスト用の動画ファイルを作成
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_file:
        tmp_file.write(b"test video content")
        tmp_file.seek(0)
        
        # ファイルオブジェクトをモック
        mock_file = Mock()
        mock_file.read.return_value = tmp_file.read()
        
        # テスト実行
        result = AudioProcessor.process_video_file(mock_file)
        
        # 検証
        assert result == "テスト音声のテキスト"
        assert mock_whisper.load_model.called
        
    # クリーンアップ
    os.unlink(tmp_file.name)


def test_process_youtube_video(mock_whisper):
    """YouTube動画処理のテスト"""
    with patch('src.audio_processor.YouTube') as mock_youtube:
        # YouTubeダウンロードのモック設定
        mock_stream = Mock()
        mock_stream.download.return_value = None
        mock_youtube.return_value.streams.filter.return_value.first.return_value = mock_stream
        
        # テスト実行
        result = AudioProcessor.process_youtube_video("https://youtube.com/test")
        
        # 検証
        assert result == "テスト音声のテキスト"
        assert mock_youtube.called
        assert mock_whisper.load_model.called 
