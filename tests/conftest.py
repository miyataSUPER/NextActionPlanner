"""
テストの共通設定を提供するモジュール
"""

import os
import pytest
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


@pytest.fixture(scope="session")
def database_url():
    """テスト用データベースのURL"""
    return {
        'dbname': 'test_action_db',
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'password'),
        'host': os.getenv('DB_HOST', 'db'),  # localhostからdbに変更
        'port': os.getenv('DB_PORT', '5432')
    }


@pytest.fixture(scope="session")
def setup_test_db(database_url):
    """テスト用データベースのセットアップ"""
    # システムデータベースに接続
    conn = psycopg2.connect(
        dbname='postgres',
        user=database_url['user'],
        password=database_url['password'],
        host=database_url['host'],
        port=database_url['port']
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    with conn.cursor() as cur:
        # テスト用データベースを作成
        cur.execute(f"DROP DATABASE IF EXISTS {database_url['dbname']}")
        cur.execute(f"CREATE DATABASE {database_url['dbname']}")

    conn.close()

    # テスト用データベースに接続
    conn = psycopg2.connect(**database_url)
    
    # テーブルを作成
    with conn.cursor() as cur:
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
        conn.commit()

    yield conn
    
    conn.close()

    # クリーンアップ
    conn = psycopg2.connect(
        dbname='postgres',
        user=database_url['user'],
        password=database_url['password'],
        host=database_url['host'],
        port=database_url['port']
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {database_url['dbname']}")

    conn.close()
