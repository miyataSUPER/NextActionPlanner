"""
テキスト処理モジュール

このモジュールは、文字起こしされたテキストの前処理を行い、
Gemini APIに送信する形式に整形する機能を提供します。
"""


class TextProcessor:
    """テキスト処理を行うクラス"""

    @staticmethod
    def preprocess(text: str) -> str:
        """
        テキストの前処理を行います。

        Args:
            text (str): 入力テキスト

        Returns:
            str: 前処理済みのテキスト
        """
        # 空白行の削除と空白の正規化
        lines = [line.strip() for line in text.split('\n')]
        lines = [line for line in lines if line]
        text = '\n'.join(lines)
        
        # 長すぎるテキストの場合は要約
        if len(text) > 30000:
            text = text[:30000] + "..."
            
        return text 
