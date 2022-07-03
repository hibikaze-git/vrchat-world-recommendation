# vrchat-world-recommendation
- VRChatワールドの推薦システム(開発中)
- twitterで投稿されている、VRChatワールドを紹介する投稿を一覧・検索できるアプリです
- 投稿にお気に入り情報・訪問済み情報・カテゴリ情報を付与できます
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
(Googleアカウント→セキュリティ→Googleへのログインから設定)

- BEARER_TOKEN=twitterAPIのトークン
(twitterAPIの利用申請が必要)

- TEST_USER_NAME=seleniumを用いたテストで使用するdjangoのユーザー名
- TEST_USER_PASS=seleniumを用いたテストで使用するdjangoのユーザーパスワード
(初回起動時は不要。テストを行いたい場合のみ、アプリでテスト用のユーザーを作成する必要がある)

- SECRET_KEY=Djangoで生成したSECRET_KEY
(開発環境以外では、既に記載されている文字列でなく、Djangoの機能を用いて再生性した文字列を指定してください)
```
- docker-compose.ymlのmariadbパスワード等は適宜変更してください
- twitterAPIを用いて投稿データを取得したい場合には、Django管理画面でスタッフユーザを作成し、アプリにログインしてください。トップページにデータ更新ボタンが出現します

## 使用方法
- コンテナ起動
```
git clone https://github.com/hibikaze-git/vrchat-world-recommendation.git
cd vrchat-world-recommendation
docker-compose build
docker-compose up -d
```
- 初回起動時は、データベースのマイグレーションを実施してください
```
docker-compose exec django bash -c "python3 manage.py migrate"
```
- localhost:8000/にアクセス

## 構成
### django
#### accounts
- ユーザー関連の機能を扱うアプリ

### app
- twitter投稿データに関わる機能を扱うアプリ

### mariadb
- 投稿データ等を保存するデータベース