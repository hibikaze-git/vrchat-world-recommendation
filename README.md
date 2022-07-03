# vrchat-world-recommendation
- VRChatワールドの推薦システム(開発中)
- twitterで投稿されている、VRChatワールドを紹介する投稿を一覧・検索
- 投稿のお気に入り機能・カテゴリ設定機能
- 将来的には、お気に入りに設定している投稿と類似した投稿をユーザーに推薦できるようにする予定です

## 開発の進捗
- [x] ユーザー認証・twitter投稿一覧表示等の基本的な機能
- [ ] カテゴリ管理機能
- [ ] VRChatワールドの推薦機能

## 開発環境・使用前の準備
- docker, docker-composeを使用しています
- docker-compose.ymlの以下の項目を事前に設定してください
```
- DEFAULT_FROM_EMAIL=パスワード再設定機能で使用するGmailアドレス
- EMAIL_HOST_USER=パスワード再設定機能で使用するGmailアドレス
- EMAIL_HOST_PASSWORD=Googleアカウントのアプリパスワード
- BEARER_TOKEN=twitterAPIのトークン
- TEST_USER_NAME=seleniumを用いたテストで使用するdjangoのユーザー名
- TEST_USER_PASS=seleniumを用いたテストで使用するdjangoのユーザーパスワード
```
- docker-compose.ymlのmariadbパスワード等は変更してください

## 使用方法
```
git clone https://github.com/hibikaze-git/vrchat-world-recommendation.git
cd vrchat-world-recommendation
docker-compose build
docker-compose up -d
localhost:8000/にアクセス
```

## 構成
### django
#### accounts
- ユーザー関連の機能を扱うアプリ

### app
- twitter投稿データに関わる機能を扱うアプリ

### mariadb
- 投稿データ等を保存するデータベース