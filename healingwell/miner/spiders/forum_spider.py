import re
from datetime import datetime, timedelta
from itertools import takewhile

from lxml.html import fragment_fromstring
from scrapy import log
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join

from healingwell.miner.items import Post


PAGE_RE = re.compile(r"&p=\d+")
POST_DATE_RE = re.compile(r"Posted (.+)")
DATETIME_RE = re.compile(r"([A-Za-z]*)(.+) \(GMT ([+-]?\d+)\)")
UNRELATED_MARKERS = ('<hr class="PostHR">', "<!-- Edit -->")

def _parse_natural_date(d_string, utc_offset):
    if d_string == "Yesterday":
        day_difference = -1
    elif d_string == "Today":
        day_difference = 0
    else:
        raise ValueError("Can't parse d_string: {0}".format(d_string))

    local_now = datetime.utcnow() + utc_offset
    return local_now.date() + timedelta(days=day_difference)

def parse_datetime(dt_string):
    m = DATETIME_RE.match(dt_string)
    utc_offset = timedelta(hours=int(m.group(3)))

    natural_date_string = m.group(1)
    if natural_date_string:
        d = _parse_natural_date(natural_date_string, utc_offset)
        dt = datetime.strptime(m.group(2), " %I:%M %p").replace(d.year, d.month, d.day)
    else:
        dt = datetime.strptime(m.group(2), "%m/%d/%Y %I:%M %p")

    return dt - utc_offset

def _preserve_emoticons(element):
    """add some text so that when img tag is removed, the text will remain"""
    for img in element.xpath('//img[starts-with(@src, "/community/emoticons")]'):
        img.text = " emoticon-{0} ".format(img.attrib["alt"])
    return element

def _extract_text(html_string):
    element = fragment_fromstring(
        html_string.replace("<br>", '\n'),
        create_parent="div"
    )
    return _preserve_emoticons(element) \
        .text_content() \
        .replace(u'\u00a0', ' ') \
        .strip()

def _is_relevant(html_string):
    return all(marker not in html_string for marker in UNRELATED_MARKERS)

def clean_post_content(loader_context, html_strings):
    return filter(bool,
        map(_extract_text,
            takewhile(_is_relevant, html_strings)))


class ForumPostLoader(ItemLoader):
    default_output_processor = TakeFirst()

    post_content_in = clean_post_content
    post_content_out = Join()


class ForumSpider(CrawlSpider):
    name = "healingwell.com"
    allowed_domains = ["healingwell.com"]

    start_urls = ["http://www.healingwell.com/community/default.aspx?c=4"]

    rules = [
        Rule(LinkExtractor(
            allow=(r"community/default\.aspx\?f=\d+",),             # forum sections
            restrict_xpaths=("//td[@class='msgTopic ForumName']",)  # in table column
        )),

        Rule(LinkExtractor(
            allow=(r"community/default\.aspx\?f=\d+&p=\d+",),                 # forum section pages
            restrict_xpaths=("(//td[@class='msgSm'][@align='right'])[2]",)    # at top right
        )),

        Rule(LinkExtractor(
            allow=(r"community/default\.aspx\?f=\d+&m=\d+",),        # topics
            restrict_xpaths=("//td[@class='msgTopic TopicTitle']",)  # in table column
        ), callback="parse_page"),

        Rule(LinkExtractor(
            allow=(r"community/default\.aspx\?f=\d+&m=\d+&p=\d+",),         # topic pages
            restrict_xpaths=("(//td[@class='msgSm'][@align='right'])[1]",)  # at top right
        ), callback="parse_page"),
    ]

    def __init__(self, *args, **kwargs):
        log.start()
        super(ForumSpider, self).__init__()

    def parse_page(self, response):
        self.log(response.body, level=0)

        l1 = ForumPostLoader(item=Post(), response=response)

        thread_url = PAGE_RE.sub('', response.url)
        section_url = thread_url.rpartition('&')[0]

        l1.add_value("page_url", response.url)
        l1.add_xpath("section_title", "//div[@id='Breadcrumbs']/a[3]/text()")
        l1.add_value("section_url", section_url)
        l1.add_xpath("thread_title", "//*[@id='PageTitle']/h1/text()")
        l1.add_value("thread_url", thread_url)

        for post_box in response.xpath("//table[@class='PostBox']"):
            self.log(post_box.extract(), level=0)

            l2 = ForumPostLoader(item=l1.load_item().copy(), selector=post_box)

            l2.add_xpath("post_url", ".//a[@name]/@name", MapCompose(lambda s: response.url + '#' + s))
            l2.add_xpath("post_author", ".//td[@class='msgUser']/a[2]/text()")
            l2.add_xpath("post_author_url", ".//td[@class='msgUser']/a[2]/@href", MapCompose("http://www.healingwell.com{0}".format))
            l2.add_xpath("post_author_rank", "(.//td[@class='msgUser']//text())[3]")
            l2.add_xpath(
                "post_date",
                ".//td[@class='msgThreadInfo PostThreadInfo']/text()",
                MapCompose(lambda s: s.strip(), parse_datetime),
                re=POST_DATE_RE
            )
            l2.add_xpath("post_content", ".//div[@class='PostMessageBody']/node()[not(@class='PostToTopLink')][not(@class='msgQuoteWrap')]")
            l2.add_xpath("post_content", ".//div[@class='PostBoxWrapper']/node()[not(@class='PostMessageBody')][not(@class='PostToTopLink')][not(@class='msgQuoteWrap')]")

            yield l2.load_item()
