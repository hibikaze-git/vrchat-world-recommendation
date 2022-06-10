from ..scripts.twitter.recent_search import RecentSearch
from ..models.twitter_post import TwitterPost
from django.shortcuts import redirect


def update_twitter_post(request):
    recent_search_instance = RecentSearch()

    json_data = recent_search_instance.main()

    response = redirect('/')

    return response
