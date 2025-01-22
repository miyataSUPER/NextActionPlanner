"""
メインアプリケーションのテスト
"""

import pytest
from src.main import parse_actions


def test_parse_actions():
    """アクション解析のテスト"""
    markdown_text = """
## アクション1
- 作業内容: テストタスク
- 担当者: テストユーザー
- 優先度: 1
- 期限: 2024-03-20
- 必要なリソース: なし
"""
    
    actions = parse_actions(markdown_text)
    assert len(actions) == 1
    assert actions[0]['content'] == 'テストタスク'
    assert actions[0]['assignee'] == 'テストユーザー'
    assert actions[0]['priority'] == 1


@pytest.mark.skip(reason="Streamlitの統合テストは別途実施")
def test_main():
    """メインアプリケーションのテスト"""
    # Streamlitの統合テストは複雑なので、別途実施
    pass 
