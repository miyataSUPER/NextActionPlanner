"""
音声処理モジュール

このモジュールは、動画ファイルやYouTube動画から音声を抽出し、
テキストに変換する機能を提供します。
"""

import os
import tempfile
from pathlib import Path
import whisper
from pytube import YouTube


class AudioProcessor:
    """音声処理を行うクラス"""

    def __init__(self):
        """音声認識モデルの初期化"""
        self.model = whisper.load_model("base")

    @staticmethod
    def process_video_file(video_file) -> str:
        """
        アップロードされた動画ファイルから音声を抽出し、テキストに変換します。

        Args:
            video_file: アップロードされた動画ファイル

        Returns:
            str: 文字起こしされたテキスト
        """
        with tempfile.NamedTemporaryFile(
            delete=False, suffix='.mp4'
        ) as tmp_file:
            tmp_file.write(video_file.read())
            video_path = tmp_file.name

        try:
            model = whisper.load_model("base")
            result = model.transcribe(video_path, language="ja")
            return result["text"]
        finally:
            os.unlink(video_path)

    @staticmethod
    def process_youtube_video(url: str) -> str:
        """
        YouTube動画をダウンロードし、音声をテキストに変換します。

        Args:
            url (str): YouTube動画のURL

        Returns:
            str: 文字起こしされたテキスト
        """
        try:
            # YouTube動画をダウンロード
            yt = YouTube(url)
            audio_stream = yt.streams.filter(only_audio=True).first()
            
            with tempfile.TemporaryDirectory() as tmp_dir:
                audio_path = Path(tmp_dir) / "audio.mp4"
                audio_stream.download(filename=str(audio_path))
                
                # 音声認識を実行
                model = whisper.load_model("base")
                result = model.transcribe(str(audio_path), language="ja")
                return result["text"]
                
        except Exception as e:
            raise Exception(f"YouTube動画の処理中にエラーが発生しました: {str(e)}") 
