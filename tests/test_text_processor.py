"""
テキスト処理モジュールのテスト
"""

from src.text_processor import TextProcessor


def test_preprocess():
    """テキスト前処理のテスト"""
    # 入力テキスト
    input_text = """
    
    テスト1
    
    テスト2
    
    テスト3
    
    """
    
    # テスト実行
    result = TextProcessor.preprocess(input_text)
    
    # 検証（空白を完全に除去した状態で比較）
    assert ' '.join(result.split()) == 'テスト1 テスト2 テスト3'


def test_preprocess_long_text():
    """長いテキストの前処理テスト"""
    # 30000文字を超えるテキスト
    long_text = "あ" * 35000
    
    # テスト実行
    result = TextProcessor.preprocess(long_text)
    
    # 検証（厳密な長さチェック）
    assert len(result) == 30003  # "..."の3文字を含む 
