import requests
import os
import json


class RecentSearch():
    def __init__(self) -> None:
        # To set your environment variables in your terminal run the following line:
        # export 'BEARER_TOKEN'='<your_bearer_token>'
        self.bearer_token = os.environ.get("BEARER_TOKEN")

        self.search_url = "https://api.twitter.com/2/tweets/search/recent"

        # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
        # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
        self.query_params = {
            'query': '(#VRChat_world紹介 OR #VRChatワールド紹介) -RT',
            'tweet.fields': 'author_id,created_at,attachments,context_annotations,entities,lang',
            'expansions': 'author_id,attachments.media_keys',
            'media.fields': 'media_key,preview_image_url,type,url',
            'user.fields': 'username',
            'max_results': 100,
        }

    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r

    def connect_to_endpoint(self, url, params):
        print(self.bearer_token)
        response = requests.get(url, auth=self.bearer_oauth, params=params)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

    def main(self):
        json_response = self.connect_to_endpoint(self.search_url, params=self.query_params)

        return json_response

    def get_emb_html(self, embed_url):
        print(embed_url)

        response = requests.get(embed_url)

        json_data = response.json()

        print(json_data)

        return json_data.get("html")
