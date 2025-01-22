"""
Gemini API クライアントモジュール

このモジュールは、Google Gemini APIと通信し、
テキストから次のアクションを生成する機能を提供します。
"""

import os
import google.generativeai as genai


class GeminiClient:
    """Gemini APIクライアントクラス"""

    def __init__(self):
        """
        Gemini APIクライアントの初期化
        """
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEYが設定されていません")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_actions(self, text: str) -> str:
        """
        テキストから次のアクションを生成します。

        Args:
            text (str): 入力テキスト

        Returns:
            str: Markdown形式のアクションリスト
        """
        prompt = f"""
以下の会議内容から、次に取るべき具体的なアクションリストを作成してください。
各アクションは以下の形式でMarkdown形式で記述してください：

## アクション{{index}}
- 作業内容: [具体的なタスクの説明]
- 担当者: [担当者名または役割]
- 優先度: [1-5の数値（1が最高優先）]
- 期限: [YYYY-MM-DD形式の日付]
- 必要なリソース: [必要な道具、予算、人員等]
- 依存関係: [前提となる他のタスク（ある場合）]

以下の点に注意して作成してください：
1. 優先度は必ず1-5の数値で指定すること
2. 期限は具体的な日付で指定すること
3. 依存関係がある場合は、他のアクション番号を参照すること
4. 作業内容は具体的で実行可能な形で記述すること

会議内容：
{text}
"""
        
        response = self.model.generate_content(prompt)
        return response.text 
