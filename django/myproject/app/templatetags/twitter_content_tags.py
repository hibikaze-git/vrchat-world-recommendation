from django import template

# Djangoのテンプレートタグライブラリ
register = template.Library()


# 指定したrecordのカテゴリを返すフィルタ
@register.filter
def remove_script(emb_html):

    return emb_html.split("<script async src=")[0]
