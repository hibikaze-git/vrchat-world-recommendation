from django.shortcuts import redirect

from ..models.twitter_post import TwitterPost
from ..scripts.twitter.recent_search import RecentSearch

recent_search_instance = RecentSearch()


def update_twitter_post(request):
    """
    twitterの最新の投稿100件を取得し、データベースに格納
    """

    # 登録済みのtwitter_id
    all_tweet_id_list = TwitterPost.objects.values_list("tweet_id", flat=True)

    # データ取得
    json_data = recent_search_instance.main()

    data_list = json_data.get("data")
    media_list = json_data.get("includes").get("media")
    users_list = json_data.get("includes").get("users")

    # media_urls
    media_dic = {}

    for media in media_list:
        media_dic[media.get("media_key")] = media.get("url")

    # username
    users_dic = {}
    for user in users_list:
        users_dic[user.get("id")] = user.get("username")

    # データベースに格納
    for data in data_list:

        # 保存積みの投稿ならスキップ
        tweet_id = data.get("id")

        if tweet_id in all_tweet_id_list:
            continue

        # 画像等の添付がないものはスキップ
        attachments = data.get("attachments")

        if attachments is None:
            continue

        author_id = data.get("author_id")
        username = users_dic.get(data.get("author_id"))
        text = data.get("text")
        media_keys = attachments.get("media_keys")

        if media_keys is None:
            continue

        # 画像等のurlの一覧をリストにする
        media_list = []

        for key in media_keys:
            media_url = media_dic.get(key)
            if media_url is not None:
                media_list.append(media_dic.get(key))

        if media_list:
            media_urls = ",".join(media_list)
        else:
            media_urls = "none"

        # 埋め込み用htmlを取得
        emb_url = f"https://publish.twitter.com/oembed?url=https://twitter.com/{username}/status/{tweet_id}&hide_thread=true&align=center"

        emb_html = recent_search_instance.get_emb_html(emb_url)

        emb_html = emb_html.replace("\n", "")
        emb_html = emb_html.replace('\"', '"')

        # データベースに保存
        TwitterPost.objects.create(
            tweet_id=tweet_id,
            author_id=author_id,
            username=username,
            text=text,
            media_urls=media_urls,
            emb_url=emb_url,
            emb_html=emb_html
        )

    # トップページに移動
    response = redirect('/')

    return response
