## 開発を始める(初回起動時)
### 前提条件
VSCode及びDocker(Docker Desktop)が導入済みかつ，VSCodeの拡張機能のRemote Developmentがインストールされていること

### 初期設定
`front-end/chat`に`.env.local`を用意する．`.env.local.sample`を参考に，IPアドレスの部分は，コンテナを動かしているホストマシンのLAN内IPを書く．  
Windowsの場合はCMDなどで`ipconfig`で確認できる．  
開発環境の場合はIPアドレス以外コピペでも良い．

### 手順
左カラムからリモートエクスプローラーを選択
- `開発コンテナ`リストが表示されるので，その欄の右にある`+`ボタンをクリック
- `コンテナーでフォルダーを開く`を選択
- 本プロジェクトの`front-end`を選択
- 右下の開くをクリック

初回起動時は開発環境のセットアップに時間がかかるため，待つ  
セットアップ終了時にリロードするか聞かれる場合があるので，その場合はリロードボタンをクリック

## 開発コンテナ(2回目以降)
リモートエクスプローラーから開発コンテナを選択すればOK

## 本番環境
本ディレクトリ(./back-end 配下)で以下のコマンドを実行
```bash
docker compose up -d
```

## 初期設定
api側のグループとUserを作成しておく．  
またapi側のUserと同一のnameを持つKeycloakアカウントを用意する．  
keycloakへのアクセスはまず[http://localhost:8081/admin/master/console/#/KadaGPT/users](http://localhost:8081/admin/master/console/#/KadaGPT/users)にアクセスし，`admin`，`hogehoge`でログイン，`Add user`からユーザ追加する．  
ユーザ名，メアド，氏名を入力して保存した後，その画面のまま`Credetials`タブに移動し，パスワードを追加する．
`Temporary`オプションはoffにしたほうが良い．

## アクセス
ブラウザから`IPアドレス:3000`にアクセスすることで確認できる．
コンテナ内で編集を行った場合，即座に反映される(ホットリロード)
