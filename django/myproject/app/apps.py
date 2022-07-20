from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        """
        スクリプトの定期実行
        """
        from .scheduler.update_twitter_post import start
        start()
