from django import template

# Djangoのテンプレートタグライブラリ
register = template.Library()


# 指定したrecordのカテゴリを返すフィルタ
@register.filter
def return_category(liked_objects, record):
    return liked_objects.filter(twitter_post=record).first().category
