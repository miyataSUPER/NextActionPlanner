"""
データベース操作のテスト
"""

from datetime import datetime, timedelta
import pytest
from src.database import Database


@pytest.fixture
def db(database_url):
    """テスト用のデータベースインスタンス"""
    # 各テストで新しいデータベース接続を作成
    database = Database()
    
    # テスト前にデータをクリーンアップ
    with database.conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE actions RESTART IDENTITY")
        database.conn.commit()
    
    yield database
    
    # テスト後に接続を閉じる
    database.conn.close()


def test_add_action(db):
    """アクション追加のテスト"""
    # データベースが空であることを確認
    initial_actions = db.get_pending_actions()
    assert len(initial_actions) == 0

    # テストデータ
    content = "テストアクション"
    assignee = "テストユーザー"
    due_date = datetime.now() + timedelta(days=1)
    priority = 1
    resources = "テストリソース"

    # アクション追加
    action_id = db.add_action(
        content=content,
        assignee=assignee,
        due_date=due_date,
        priority=priority,
        resources=resources
    )

    assert action_id > 0

    # 追加したアクションを取得して確認
    actions = db.get_pending_actions()
    assert len(actions) == 1
    action = actions[0]
    assert action['content'] == content
    assert action['assignee'] == assignee
    assert action['priority'] == priority
    assert action['resources'] == resources


def test_complete_action(db):
    """アクション完了のテスト"""
    # データベースが空であることを確認
    initial_actions = db.get_pending_actions()
    assert len(initial_actions) == 0

    # アクションを追加
    action_id = db.add_action(content="完了テスト")
    
    # 追加直後は1件存在することを確認
    actions_before = db.get_pending_actions()
    assert len(actions_before) == 1
    
    # アクションを完了状態に更新
    db.complete_action(action_id)
    
    # 完了後は未完了アクションが0件になることを確認
    actions_after = db.get_pending_actions()
    assert len(actions_after) == 0


def test_get_action_stats(db):
    """統計情報取得のテスト"""
    # データベースが空であることを確認
    initial_stats = db.get_action_stats()
    assert initial_stats['pending_count'] == 0
    assert initial_stats['completed_count'] == 0
    
    # 複数のアクションを追加
    db.add_action(content="統計テスト1")
    action_id = db.add_action(content="統計テスト2")
    db.add_action(content="統計テスト3")
    
    # 1つのアクションを完了状態に
    db.complete_action(action_id)
    
    # 統計情報を取得して確認
    stats = db.get_action_stats()
    assert stats['pending_count'] == 2
    assert stats['completed_count'] == 1 
