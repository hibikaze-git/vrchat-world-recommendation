import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from ..views import twitter_view


def start():
    """
    最新の投稿を定期的に取得
    """
    # 日時を設定
    today = datetime.date.today()
    start_time = datetime.datetime(today.year, today.month, today.day, 0, 30) + datetime.timedelta(days=1)

    scheduler = BackgroundScheduler()

    scheduler.add_job(twitter_view.create_twitter_post, 'interval', minutes=1, start_date=start_time)

    scheduler.start()
