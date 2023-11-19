## pyproject.tomlとpoetry.lockを作成する
pyproject.tomlがない場合や，更新したい場合は本ディレクトリ(./back-end 配下)で以下のコマンドを実行
それ以外の場合はこの手順をスキップして初回起動へ
```bash
docker compose -f compose.dev.yml run --rm --entrypoint "poetry init --name api --dependency fastapi --dependency uvicorn[standard] --dependency gunicorn --dependency python-multipart --dependency python-jose" api
```
基本的にはEnter
`Author`は`n`
`Compatible Python versions`と出てくるので`>=3.11,<3.12`とする
```bash
docker compose -f compose.dev.yml run --rm --entrypoint "poetry add --group data-science numpy" api
docker compose -f compose.dev.yml run --rm --entrypoint "poetry add --group llm openai langchain llama-index qdrant-client" api
docker compose -f compose.dev.yml run --rm --entrypoint "poetry add --group document ndjson pymupdf" api
docker compose -f compose.dev.yml run --rm --entrypoint "poetry add --group database sqlalchemy aiomysql" api
```

## 初回起動(VSCode)
### 前提条件
VSCode及びDocker(Docker Desktop)が導入済みかつ，VSCodeの拡張機能のRemote Developmentがインストールされていること

### 手順
左カラムからリモートエクスプローラーを選択
- `コンテナーでフォルダーを開く`を選択
- 本プロジェクトの`back-end`を選択
- 右下の開くをクリック

初回起動時は開発環境のセットアップに時間がかかるため，数分待つ
セットアップ終了時にリロードするか聞かれる場合があるので，その場合はリロードボタンをクリック

## 開発コンテナ(VSCode)
リモートエクスプローラーから開発コンテナを選択すればOK

## 本番環境
本ディレクトリ(./back-end 配下)で以下のコマンドを実行
```bash
docker compose up -d
```
