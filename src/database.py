"""
データベース操作モジュール

このモジュールは、アクションアイテムのデータベース操作を提供します。
"""

import os
from datetime import datetime
from typing import List, Optional
import psycopg2
from psycopg2.extras import DictCursor


class Database:
    """データベース操作クラス"""

    def __init__(self):
        """データベース接続の初期化"""
        self.conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        self._create_tables()

    def _create_tables(self):
        """必要なテーブルを作成"""
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS actions (
                    id SERIAL PRIMARY KEY,
                    content TEXT NOT NULL,
                    assignee TEXT,
                    due_date DATE,
                    priority INTEGER,
                    status TEXT DEFAULT 'pending',
                    resources TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP
                )
            """)
            self.conn.commit()

    def add_action(
        self,
        content: str,
        assignee: Optional[str] = None,
        due_date: Optional[datetime] = None,
        priority: Optional[int] = None,
        resources: Optional[str] = None
    ) -> int:
        """
        新しいアクションをデータベースに追加

        Args:
            content: アクションの内容
            assignee: 担当者
            due_date: 期限
            priority: 優先度（1-5）
            resources: 必要なリソース

        Returns:
            int: 追加されたアクションのID
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO actions 
                (content, assignee, due_date, priority, resources)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (content, assignee, due_date, priority, resources)
            )
            action_id = cur.fetchone()[0]
            self.conn.commit()
            return action_id

    def get_pending_actions(self) -> List[dict]:
        """未完了のアクションを取得"""
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT * FROM actions 
                WHERE status = 'pending'
                ORDER BY priority ASC NULLS LAST, due_date ASC NULLS LAST
            """)
            return [dict(row) for row in cur.fetchall()]

    def complete_action(self, action_id: int):
        """アクションを完了状態に更新"""
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE actions 
                SET status = 'completed', completed_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (action_id,))
            self.conn.commit()

    def get_action_stats(self) -> dict:
        """アクションの統計情報を取得"""
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                """
                SELECT 
                    COUNT(*) FILTER (WHERE status = 'pending') as pending_count,
                    COUNT(*) FILTER (WHERE status = 'completed') as completed_count,
                    AVG(EXTRACT(EPOCH FROM (completed_at - created_at)) / 3600) 
                        FILTER (WHERE status = 'completed') as avg_completion_time
                FROM actions
                """
            )
            return dict(cur.fetchone()) 
