# kada-gpt

## Overview
chatGPTを用いた組織内文書検索，対話を実現するプロジェクト

## Requirement
- Docker
  - Windows
  - macOS(Intel & Apple silicon)
  - Linux
- OpenAI API key

## Usage
### 初回セットアップ
プロジェクトディレクトリ直下で操作
```bash
# 初回起動
$ docker compose up -d

# 起動
$ docker compose start

# 停止
$ docker compose stop
```

### イメージ更新
```bash
# 更新
docker compose up --build -d

# 以前のコンテナを削除してから更新
docker compose down
docker compose up -d
```

## Description
- OpenAIのAPIキー
  - `/.env.sample`をコピーして`/.env`とし，APIキーを追加
  - 参照する際は環境変数`OPENAI_API_KEY`を指定
- JupyterLab
  - ホストマシンの8888ポートにアクセスすべし
  - トークンは`stnet`
- ベクトルDB
  - Qdrant(クワッドラント)をコンテナで立ち上げている
    - ホスト名：qdrant
    - ポート番号：6333
  - ユーザ間のDB共有方法
    - 検討中
