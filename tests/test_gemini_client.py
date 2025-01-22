"""
Gemini APIクライアントのテスト
"""

import pytest
from unittest.mock import Mock, patch
from src.gemini_client import GeminiClient


@pytest.fixture
def mock_genai():
    """Gemini APIのモック"""
    with patch('src.gemini_client.genai') as mock:
        yield mock


@pytest.fixture
def client(mock_genai):
    """テスト用のGeminiClientインスタンス"""
    with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
        return GeminiClient()


def test_generate_actions(client, mock_genai):
    """アクション生成のテスト"""
    # モックレスポンスの設定
    mock_response = Mock()
    mock_response.text = """
## アクション1
- 作業内容: テストタスク1
- 担当者: テストユーザー1
- 優先度: 1
- 期限: 2024-03-20
- 必要なリソース: なし
- 依存関係: なし

## アクション2
- 作業内容: テストタスク2
- 担当者: テストユーザー2
- 優先度: 2
- 期限: 2024-03-21
- 必要なリソース: テストリソース
- 依存関係: アクション1
"""
    client.model.generate_content.return_value = mock_response

    # テスト実行
    result = client.generate_actions("テストミーティングの内容")

    # 結果の検証
    assert "アクション1" in result
    assert "アクション2" in result
    assert "優先度: 1" in result
    assert "優先度: 2" in result 
