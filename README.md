# Next Action Planner (NAP)

## 概要
会議の音声やテキストから次のアクションを自動的に抽出し、効率的にタスク管理を行うためのツールです。
音声認識とAIを活用して、会議の内容から具体的なアクションアイテムを生成し、優先度や期限を設定して管理することができます。

## 主な機能

### 1. 多様な入力方式
- MP4動画ファイルのアップロード
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
- PostgreSQL 14: タスクデータの永続化
- Docker: 環境の一貫性確保

### AI/ML
- OpenAI Whisper: 音声認識
- Google Gemini: テキスト解析・アクション抽出

## セットアップ方法

### 前提条件
- Dockerがインストールされていること
- Google Gemini APIキーを取得していること

### 1. 環境構築
\`\`\`bash
# リポジトリのクローン
git clone https://github.com/yourusername/NextActionPlanner.git
cd NextActionPlanner

# 環境変数ファイルの作成
cp .env.example .env

# 環境変数の設定
# .envファイルを編集し、以下の項目を設定：
# - GEMINI_API_KEY
# - その他必要な設定
\`\`\`

### 2. アプリケーションの起動
\`\`\`bash
# Dockerコンテナのビルドと起動
docker-compose up --build
\`\`\`

### 3. アクセス
ブラウザで http://localhost:8501 にアクセス

## 開発者向け情報

### テストの実行
\`\`\`bash
# 全テストの実行
docker-compose run test

# カバレッジレポートの生成
docker-compose run test pytest --cov=src tests/
\`\`\`

### プロジェクト構造
\`\`\`
action-extractor/
├── docker/                   # Docker設定
│   ├── Dockerfile
│   └── requirements.txt
├── src/                     # ソースコード
│   ├── core/               # コア機能
│   │   ├── audio.py       # 音声処理
│   │   ├── text.py        # テキスト処理
│   │   └── actions.py     # アクション生成
│   ├── db/                # データベース
│   │   ├── models.py
│   │   └── operations.py
│   ├── api/               # 外部API
│   │   └── gemini.py
│   └── utils/             # ユーティリティ
│       ├── logger.py
│       └── config.py
├── tests/                  # テストコード
└── data/                   # データ保存
\`\`\`

## 使用方法

1. アプリケーションにアクセス
2. 入力方式を選択（動画/YouTube/テキスト）
3. データをアップロード or 入力
4. アクションの自動生成を待機
5. 生成されたアクションを確認・編集
6. タスクの進捗を管理

## 注意事項

- 音声認識の精度は入力音声の品質に依存します
- 長時間の動画は処理に時間がかかる場合があります
- APIキーは適切に管理してください

## ライセンス
MIT License

## 作者
宮田大資
- Mail: miyata.aistart@gmail.com

## 貢献
バグ報告や機能改善の提案は、GitHubのIssueやPull Requestsで受け付けています。

---

※ このプロジェクトは開発中であり、機能は予告なく変更される可能性があります。
