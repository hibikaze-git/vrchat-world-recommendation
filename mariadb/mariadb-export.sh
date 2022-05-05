#!/bin/bash

# コンテナが全て停止している状態で実行
# 古いdumpファイルは削除されるので注意
# 一度up -dを実行して、コンテナを予め作っておく必要あり

# mariadb
rm ./mariadb/dump.sql
docker-compose start mariadb
# パスワードを入力してenter
echo 'Please input pass:'
docker-compose exec mariadb mysqldump -u mariadb -p mariadb > ./mariadb/dump.sql
# for table
# docker-compose exec mariadb mysqldump -u mariadb -p mariadb dialogue_act > ./mariadb/dialogue_act.sql
docker-compose stop mariadb