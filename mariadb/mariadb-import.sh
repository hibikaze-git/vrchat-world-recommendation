#!/bin/bash

# コンテナが全て停止している状態で実行
# 古いdumpファイルは削除されるので注意
# 一度up -dを実行して、コンテナを予め作っておく必要あり
# 各コンテナのフォルダ直下にimportしたいデータを配置

# mariadb
# mariadb-export.shを使用すると不要な情報がdumpファイルの1行目に追加されてしまうので、削除
sed '1d' ./mariadb/dump.sql > ./mariadb/dump_modify.sql
docker-compose start mariadb
docker cp ./mariadb/dump_modify.sql $(docker-compose ps -q mariadb):/tmp/dump_modify.sql
docker-compose exec mariadb bash -c "mysql -u mariadb -p mariadb < /tmp/dump_modify.sql"
# パスワードを入力してenter
docker-compose stop mariadb

rm ./mariadb/dump_modify.sql