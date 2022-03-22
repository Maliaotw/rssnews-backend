from django.core.management.base import BaseCommand

from app.models import Source, Category


def create_category():
    data = [
        {'name': '科技', 'defaults': {'content': '', 'code': 'tech'}},
        {'name': '商業', 'defaults': {'content': '', 'code': 'business'}},
        {'name': '寵物', 'defaults': {'content': '', 'code': 'pet'}},
        {'name': '設計', 'defaults': {'content': '', 'code': 'design'}},
        {'name': '表特', 'defaults': {'content': '', 'code': 'beauty'}},
        {'name': '博客', 'defaults': {'content': '', 'code': 'blog'}},
        {'name': '電影', 'defaults': {'content': '', 'code': 'movie'}},

    ]
    for i in data:
        obj, status = Category.objects.update_or_create(**i)


def tech():
    it_data = [
        {'name': '癮科技', 'timezone': 0, 'url': 'http://feeds.feedburner.com/engadget/cstb'},
        {'name': '重灌狂人', 'timezone': 0, 'url': 'https://briian.com/feed/'},
        {'name': '科技新報', 'timezone': 0, 'url': 'https://technews.tw/tn-rss/'},
        {'name': '爱范儿', 'timezone': 0, 'url': 'http://www.ifanr.com/feed'},
        {'name': '驱动之家', 'timezone': 0, 'url': 'http://rss.mydrivers.com/rss.aspx?Tid=1'},
        {'name': 'techweb', 'timezone': 0, 'url': 'http://www.techweb.com.cn/rss/allnews.xml'},
        {'name': 'QQ 科技', 'timezone': 0, 'url': 'http://rss.qq.com/tech.htm'},
        {'name': '51cto 運維', 'timezone': 0, 'url': 'http://www.51cto.com/php/rss.php?typeid=545'},
        {'name': 'IT之家', 'timezone': 0, 'url': 'http://www.ithome.com/rss/'},
        {'name': '威锋网', 'timezone': 0, 'url': 'http://tech.feng.com/rss.xml'},
        {'name': 'iThome', 'timezone': 0, 'url': 'http://www.ithome.com.tw/rss'},
        {'name': 'T客邦', 'timezone': 0, 'url': 'http://feeds.feedburner.com/techbang'},
        {'name': '科技報橘', 'timezone': 0, 'url': 'https://buzzorange.com/techorange/feed/'},
        {'name': '编程派', 'timezone': 0, 'url': 'http://codingpy.com/feed/'},
        {'name': 'ReadWrite［日本版］', 'timezone': 0, 'url': 'http://readwrite.jp/feed/'},
        {'name': 'AppBank', 'timezone': 0, 'url': 'http://www.appbank.net/feed'},
        {'name': 'ASCII.jp - TECH', 'timezone': 0, 'url': 'http://rss.rssad.jp/rss/ascii/it/rss.xml'},
        {'name': 'INSIDE 硬塞的網路趨勢觀察', 'timezone': 0, 'url': 'http://feeds.feedburner.com/inside-blog-taiwan'},
        {'name': 'ETNEWS 3C新聞', 'timezone': 0, 'url': 'http://feeds.feedburner.com/ettoday/teck3c'},
        {'name': '极客公园', 'timezone': 0, 'url': 'http://feeds.geekpark.net/'},
        {'name': '奇客Solidot–传递最新科技情报', 'timezone': 0, 'url': 'http://feeds.feedburner.com/solidot'},
        {'name': '小众软件', 'timezone': 0, 'url': 'http://feed.appinn.com/'},
        {'name': '月光博客', 'timezone': 0, 'url': 'http://feed.williamlong.info/'}

    ]

    it_id = Category.objects.get(code='tech').id

    for i in it_data:
        Source.objects.get_or_create(category_id=it_id, **i)

def pet():
    data_list = [
        {'name': '狗版', 'timezone': 0, 'url': 'http://rss.ptt.cc/dog.xml'},
        {'name': '寵物板', 'timezone': 0, 'url': 'http://rss.ptt.cc/pet.xml'},
    ]

    cate_id = Category.objects.get(code='pet').id

    for i in data_list:
        Source.objects.get_or_create(category_id=cate_id, **i)

def design():
    data_list = [
        {'name': '嫁給 RD 的 UI Designer', 'timezone': 0, 'url': 'https://blog.akanelee.me/index.xml'},
        {'name': '大人物', 'timezone': 0, 'url': 'https://www.damanwoo.com/daman/rss'},
        {'name': '黑秀網', 'timezone': 0, 'url': 'https://www.heyshow.com/feed'},
        {'name': '城市美學新態度', 'timezone': 0, 'url': 'http://kaiak.tw/?feed=rss2'},
        {'name': '生活藝文誌', 'timezone': 0, 'url': 'http://flipermag.com/feed/'},
    ]

    cate_id = Category.objects.get(code='design').id

    for i in data_list:
        Source.objects.get_or_create(category_id=cate_id, **i)


def movie():
    data_list = [
        {'name': '影像日报', 'timezone': 0, 'url': 'http://moviesoon.com/news/feed/'},
        {'name': '電影森林', 'timezone': 0, 'url': 'https://movieforestlitmited.blogspot.com/feeds/posts/default'}
    ]

    cate_id = Category.objects.get(code='movie').id

    for i in data_list:
        Source.objects.get_or_create(category_id=cate_id, **i)

def business():
    data_list = [
        {'name': 'Ptt金融版', 'timezone': 0, 'url': 'http://rss.ptt.cc/Finance.xml'},
        {'name': '商周', 'timezone': 0, 'url': 'http://cmsapi.businessweekly.com.tw/?CategoryId=24612ec9-2ac5-4e1f-ab04-310879f89b33&TemplateId=8E19CF43-50E5-4093-B72D-70A912962D55'},
        {'name': '經理人', 'timezone': 0, 'url': 'http://www.managertoday.com.tw/rss/'},
        {'name': '遠見雜誌', 'timezone': 0, 'url': 'http://www.gvm.com.tw/RSS/rss.asp'},
        {'name': 'The News Lens 關鍵評論網', 'timezone': 0, 'url': 'http://feeds.feedburner.com/TheNewsLens'},
    ]

    cate_id = Category.objects.get(code='business').id

    for i in data_list:
        Source.objects.get_or_create(category_id=cate_id, **i)

def beauty():
    data_list = [
        {'name': 'Ptt表特版', 'timezone': 0, 'url': 'https://www.ptt.cc/atom/beauty.xml'},
    ]

    cate_id = Category.objects.get(code='beauty').id

    for i in data_list:
        Source.objects.get_or_create(category_id=cate_id, **i)




def create_source():
    tech()
    pet()
    beauty()
    business()
    design()
    movie()


def initialize_data():
    create_category()
    create_source()


class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        print('create defaults category and source')
        initialize_data()
