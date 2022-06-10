from ..scripts.twitter.recent_search import RecentSearch
from ..models.twitter_post import TwitterPost
from django.shortcuts import redirect

recent_search_instance = RecentSearch()


def update_twitter_post(request):
    all_tweet_id_list = TwitterPost.objects.values_list("tweet_id", flat=True)

    json_data = recent_search_instance.main()

    data_list = json_data.get("data")
    media_list = json_data.get("includes").get("media")
    users_list = json_data.get("includes").get("users")

    media_dic = {}

    for media in media_list:
        media_dic[media.get("media_key")] = media.get("url")

    users_dic = {}
    for user in users_list:
        users_dic[user.get("id")] = user.get("username")

    for data in data_list:
        tweet_id = data.get("id")

        if tweet_id in all_tweet_id_list:
            continue

        author_id = data.get("author_id")
        username = users_dic.get(data.get("author_id"))
        text = data.get("text")

        attachments = data.get("attachments")

        if attachments is None:
            continue

        media_keys = attachments.get("media_keys")

        media_list = []

        for key in media_keys:
            media_list.append(media_dic.get(key))

        print(username)
        print(tweet_id)

        emb_url = f"https://publish.twitter.com/oembed?url=https://twitter.com/{username}/status/{tweet_id}&hide_thread=true"

        emb_html = recent_search_instance.get_emb_html(emb_url)

        emb_html = emb_html.replace("\n", "")
        emb_html = emb_html.replace('\"', '"')

        try:
            TwitterPost.objects.create(
                tweet_id=tweet_id,
                author_id=author_id,
                username=username,
                text=text,
                media_urls=",".join(media_list),
                emb_url=emb_url,
                emb_html=emb_html
            )
        except:
            print("error")

    response = redirect('/')

    return response
