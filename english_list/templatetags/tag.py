from django import template

register = template.Library() # Djangoのテンプレートタグライブラリ

@register.simple_tag
def url_replace(request, field, value):
    """
    URLのクエリパラメータを置き換える
    :param request:DjangoのHttpRequestオブジェクトで、現在のページのURLの情報を持つ。
    :param field:置き換えるクエリパラメータの名前 ex)page
    :param value:置き換えるクエリパラメータの値 ex)1や2,3,4
    :return:辞書オブジェクト url_dict をクエリ文字列に変換
            つまり、URLの ? 以降の部分。　ex) keyword=p&page=2
    """

    print(field,value,'--field,value--')
    #　現在のURLのクエリパラメータの情報を取得し、それを辞書型オブジェクト url_dict にコピー
    url_dict = request.GET.copy()
    print(url_dict,'--url_dict--')
    #　<QueryDict: {'category': ['IT'], 'page': ['4']}> --url_dict--

    url_dict[field] = str(value)
    print(url_dict[field],'--url_dict[field]--')
    # 2 - -url_dict[field] - -

    print(url_dict.urlencode(),'--return--')
    # category=IT&page=2 --return--

    return url_dict.urlencode()
