# Next Action Planner (NAP)

## 概要
会議の音声やテキストから次のアクションを自動的に抽出し、効率的にタスク管理を行うためのツールです。
音声認識とAIを活用して、会議の内容から具体的なアクションアイテムを生成し、優先度や期限を設定して管理することができます。

## 主な機能

### 1. 多様な入力方式
- MP4動画ファイルのアップロード（最大サイズ: 200MB）
- YouTubeリンクからの音声抽出
- テキストの直接入力

### 2. アクション抽出
- Whisperによる高精度な音声認識
- Gemini AIによるアクション項目の自動抽出
- 構造化されたアクション情報の生成
  - タスク内容
  - 担当者
  - 優先度（1-5）
  - 期限
  - 必要なリソース
  - 依存関係

### 3. タスク管理
- 優先度に基づく表示
- 進捗状況の追跡
- 完了タスクの管理
- 統計情報の表示

## 技術スタック

### フロントエンド
- Streamlit: 直感的なWebインターフェース

### バックエンド
- Python 3.9
- PostgreSQL: タスクデータの永続化
- Docker & Docker Compose: 環境の一貫性確保

### AI/ML
- OpenAI Whisper: 音声認識
- Google Gemini: テキスト解析・アクション抽出

## セットアップ方法

### 前提条件
- Docker Desktop (Mac/Windows) または Docker Engine (Linux)
- Docker Compose
- Google Cloud Platformアカウントと有効なGemini APIキー

### 1. 環境構築
```bash
# リポジトリのクローン
git clone https://github.com/miyata-h256/NextActionPlanner.git
cd NextActionPlanner

# 環境変数ファイルの作成
cp .env.example .env

# 環境変数の設定
# .envファイルを編集し、以下の項目を設定：
# - GEMINI_API_KEY: Google Cloud PlatformのGemini APIキー
# - MAX_FILE_SIZE: アップロード可能な最大ファイルサイズ（デフォルト: 200MB）
# - WHISPER_MODEL: 使用するWhisperモデル（"base"/"small"/"medium"/"large"）
# - POSTGRES_*: データベース接続設定
```

### 2. アプリケーションの起動
```bash
# Dockerコンテナのビルドと起動
docker-compose up --build

# バックグラウンドで実行する場合
docker-compose up -d --build
```

### 3. アクセス
ブラウザで http://localhost:8501 にアクセス

## 開発者向け情報

### テストの実行
```bash
# 全テストの実行
docker-compose run --rm test pytest

# カバレッジレポートの生成
docker-compose run --rm test pytest --cov=src tests/

# 特定のテストファイルの実行
docker-compose run --rm test pytest tests/test_database.py
```

### プロジェクト構造
```
NextActionPlanner/
├── docker/                 # Docker設定
│   ├── Dockerfile
│   └── requirements.txt
├── src/                   # ソースコード
│   ├── core/             # コア機能
│   │   ├── audio.py     # 音声処理
│   │   └── text.py      # テキスト処理
│   ├── db/              # データベース
│   │   └── database.py  # DB操作
│   ├── api/             # 外部API
│   │   └── gemini.py    # Gemini API
│   ├── utils/           # ユーティリティ
│   │   └── config.py    # 設定管理
│   └── main.py          # メインアプリケーション
├── tests/                # テストコード
├── .env.example         # 環境変数テンプレート
├── docker-compose.yml   # Docker Compose設定
├── pytest.ini          # Pytestの設定
└── README.md           # プロジェクト説明
```

## 使用方法

1. アプリケーションにアクセス（http://localhost:8501）
2. 入力方式を選択
   - MP4ファイルのアップロード
   - YouTubeリンクの入力
   - テキストの直接入力
3. データの処理を待機
   - 動画/音声の場合：音声認識処理
   - テキストの場合：直接アクション抽出へ
4. 生成されたアクションの確認・編集
   - 優先度の調整
   - 期限の設定
   - 担当者の割り当て
5. タスクの進捗管理
   - 完了状態の更新
   - 統計情報の確認

## 注意事項

- 音声認識の精度は入力音声の品質に依存します
- 長時間の動画は処理に時間がかかる場合があります
- APIキーは適切に管理し、公開リポジトリにコミットしないでください
- 大きなファイルをアップロードする場合は、環境変数の`MAX_FILE_SIZE`を適切に設定してください

## ライセンス
MIT License

## 作者
宮田大資  
京都産業大学 情報理工学部データサイエンスコース  
- Mail: miyata.aistart@gmail.com
- Tel: 080-2999-8873

## 貢献
バグ報告や機能改善の提案は、GitHubのIssueやPull Requestsで受け付けています。

---

※ このプロジェクトは開発中であり、機能は予告なく変更される可能性があります。
