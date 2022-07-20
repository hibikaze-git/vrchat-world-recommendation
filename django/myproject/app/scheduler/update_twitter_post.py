from apscheduler.schedulers.background import BackgroundScheduler

from ..views import twitter_view


def start():
    """
    最新の投稿を定期的に取得
    """
    scheduler = BackgroundScheduler()

    scheduler.add_job(twitter_view.create_twitter_post, 'cron', hour=4, minute=30)
    scheduler.start()
