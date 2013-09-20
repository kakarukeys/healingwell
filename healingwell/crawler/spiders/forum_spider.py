import re
from datetime import datetime, timedelta
from itertools import takewhile, imap, ifilter

from lxml.html import fragment_fromstring
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from scrapy.selector import HtmlXPathSelector

from healingwell.crawler.items import Post


P_RE = re.compile("&p=\d+")
DATETIME_RE = re.compile("(.+) \(GMT ([+-]\d+)\)")
UNRELATED_MARKERS = ('<hr class="PostHR">', "<!-- Edit -->")

def preserve_emoticons(element):
    """add some text so that when img tag is removed, the text will remain"""
    for img in element.xpath('//img[starts-with(@src, "/community/emoticons")]'):
        img.text = " emoticon-" + img.attrib["alt"] + ' '
    return element

def extract_text(html_string):
    return preserve_emoticons(fragment_fromstring(html_string, create_parent="div")) \
        .text_content() \
        .replace(u'\u00a0', ' ') \
        .strip()

def is_related(html_string):
    return all(marker not in html_string for marker in UNRELATED_MARKERS)

def clean_post_content(loader_context, html_strings):
    return ifilter(bool,
        imap(extract_text,
            takewhile(is_related, html_strings)))

class PostLoader(XPathItemLoader):
    default_output_processor = TakeFirst()

    post_content_in = clean_post_content
    post_content_out = Join()

def parse_datetime(dt_string):
    m = DATETIME_RE.match(dt_string)
    dt = datetime.strptime(m.group(1), "%m/%d/%Y %I:%M %p")
    return dt - timedelta(hours=int(m.group(2)))

class ForumSpider(CrawlSpider):
    name = "healingwell"
    allowed_domains = ["healingwell.com"]
    start_urls = ["http://www.healingwell.com/community/default.aspx?f=45&p=84&x=100&ord=ld"]
    rules = [
        Rule(SgmlLinkExtractor(allow=['/community/default\.aspx\?f=45&'], restrict_xpaths=("//td[starts-with(@class,'msgSm')]",))),
        Rule(SgmlLinkExtractor(allow=['/community/default\.aspx\?f=45&'], restrict_xpaths=("//td[starts-with(@class,'msgTopic ')]",)), 'parse_thread'),
    ]

    def parse_thread(self, response):
        x = HtmlXPathSelector(response)

        l1 = PostLoader(item=Post(), selector=x)

        l1.add_value("page_url", response.url)
        l1.add_xpath("section_title", "//div[@id='Breadcrumbs']/a[3]/text()")
        l1.add_xpath("section_url", "//div[@id='Breadcrumbs']/a[3]/@href", MapCompose(lambda s: "http://www.healingwell.com" + s))
        l1.add_xpath("thread_title", "//div[@id='Breadcrumbs']/text()[3]", MapCompose(lambda s: s.strip()), re="> (.*)")
        l1.add_value("thread_url", P_RE.sub('', response.url))

        for b in x.select("//table[@class='PostBox']"):
            l2 = PostLoader(item=Post(l1.load_item()), selector=b)

            l2.add_xpath("post_url", ".//a[@name]/@name", MapCompose(lambda s: response.url + '#' + s))
            l2.add_xpath("post_author", ".//td[@class='msgUser']/a[2]/text()")
            l2.add_xpath("post_author_url", ".//td[@class='msgUser']/a[2]/@href", MapCompose(lambda s: "http://www.healingwell.com" + s))
            l2.add_xpath(
                "post_date",
                ".//td[@class='msgThreadInfo PostThreadInfo']/text()",
                MapCompose(lambda s: s.strip(), parse_datetime),
                re="Posted (.*)"
            )
            l2.add_xpath("post_content", ".//div[@class='PostMessageBody']/node()[not(@class='PostToTopLink')][not(@class='msgQuoteWrap')]")
            l2.add_xpath("post_content", ".//div[@class='PostBoxWrapper']/node()[not(@class='PostMessageBody')][not(@class='PostToTopLink')][not(@class='msgQuoteWrap')]")

            yield l2.load_item()
