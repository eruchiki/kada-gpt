# KadaGPT

[**アプリ用のマニュアル**](./doc/manual.md)

## Overview
chatGPTを用いた組織内文書検索，対話を実現するプロジェクト

## Requirement
- Docker
  - Windows
  - macOS(Intel & Apple silicon)
  - Linux
- OpenAI API key

## エラーが出る場合

- "Error response from daemon: can't access specified distro mount service"
  - DockerでWSL integrationを有効化してください
  - Settings > Resources > WSL integration のチェックボックスをONにする
