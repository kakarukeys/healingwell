import unittest
from mock import patch, MagicMock
import os
import re
from datetime import datetime
from collections import defaultdict

from scrapy.http import HtmlResponse

import healingwell.miner.spiders.forum_spider as fs


FIXTURE_DATA_DIR = os.path.join(os.path.dirname(__file__), "fixture_data")

def read_response_from_file(filename):
    with open(os.path.join(FIXTURE_DATA_DIR, filename)) as f:
        response_body = f.read()

    return HtmlResponse(
        url=re.search(r'"(http.*)"', response_body).group(1),
        body=response_body
    )

class TestForumSpider(unittest.TestCase):
    def test_parse_datetime(self):
        dt_string = "3/6/2012 10:22 AM (GMT -7)"
        dt = fs.parse_datetime(dt_string)
        self.assertEqual(dt, datetime(2012, 3, 6, 17, 22))

        dt_string = "Yesterday 12:19 PM (GMT -7)"

        with patch("healingwell.miner.spiders.forum_spider.datetime") as mock_datetime:
            mock_datetime.utcnow.return_value = datetime(2015, 2, 4, 6, 59, 59, 677745)
            mock_datetime.strptime.side_effect = datetime.strptime

            dt = fs.parse_datetime(dt_string)

        self.assertEqual(dt, datetime(2015, 2, 2, 19, 19))

        dt_string = "Today 12:19 PM (GMT -7)"

        with patch("healingwell.miner.spiders.forum_spider.datetime") as mock_datetime:
            mock_datetime.utcnow.return_value = datetime(2015, 2, 4, 6, 59, 59, 677745)
            mock_datetime.strptime.side_effect = datetime.strptime

            dt = fs.parse_datetime(dt_string)

        self.assertEqual(dt, datetime(2015, 2, 3, 19, 19))

    def test_parse_page(self):
        response = read_response_from_file("forum_page2.html")

        spider = fs.ForumSpider()
        with patch("healingwell.miner.spiders.forum_spider.parse_datetime", MagicMock(return_value=datetime(2012, 12, 21))) as mock_parse_datetime:
            items = list(spider.parse_page(response))

            mock_parse_datetime.assert_any_call("3/6/2012 10:22 AM (GMT -7)")

        self.assertEqual(items[0]["page_url"], "http://www.healingwell.com/community/default.aspx?f=45&m=2283377&p=2")
        self.assertEqual(items[1]["section_title"], "GERD - Heartburn")
        self.assertEqual(items[2]["section_url"], "http://www.healingwell.com/community/default.aspx?f=45")
        self.assertEqual(items[3]["thread_title"], "Chronic Belching!!! Please Help")
        self.assertEqual(items[4]["thread_url"], "http://www.healingwell.com/community/default.aspx?f=45&m=2283377")

        self.assertEqual(items[1]["post_url"], "http://www.healingwell.com/community/default.aspx?f=45&m=2283377&p=2#m2361290")
        self.assertEqual(items[1]["post_author"], "LittleB72")
        self.assertEqual(items[1]["post_author_url"], "http://www.healingwell.com/community/profile.aspx?f=45&m=2283377&p=141798")
        self.assertEqual(items[1]["post_author_rank"], "New Member")
        self.assertEqual(items[1]["post_date"], datetime(2012, 12, 21))

class TestForumSpiderPropertyBased(unittest.TestCase):
    def test_parse_page(self):
        forum_page_filenames = [name for name in next(os.walk(FIXTURE_DATA_DIR))[2] if name.startswith("forum_page")]

        spider = fs.ForumSpider()
        posts = [
            item \
                for filename in forum_page_filenames \
                    for item in spider.parse_page(read_response_from_file(filename))
        ]

        self.assertEqual(len(posts), 154)

        unique_values_by_key = defaultdict(set)
        for p in posts:
            for key in ("page_url", "section_title", "section_url", "thread_title", "thread_url", "post_url", "post_author", "post_author_url", "post_author_rank", "post_date", "post_date", "post_content"):
                self.assertTrue(key in p, "{0} key is missing in {1}.".format(key, p))

                if isinstance(p[key], unicode):
                    self.assertEqual(p[key], p[key].strip(), "whitespace is not trimmed for {0} value in {1}.".format(key, p))

                self.assertTrue(p[key], "{0} value is missing in {1}.".format(key, p))

                unique_values_by_key[key].add(p[key])

            self.assertTrue(len(p["post_content"]) > 10, "post_content value is too short in {0}".format(p))

        self.assertEqual(len(unique_values_by_key["page_url"]), 10)
        self.assertEqual(len(unique_values_by_key["thread_title"]), 6)
        self.assertEqual(len(unique_values_by_key["thread_url"]), 6)
        self.assertEqual(len(unique_values_by_key["section_title"]), 5)
        self.assertEqual(len(unique_values_by_key["section_url"]), 5)
        self.assertEqual(len(unique_values_by_key["post_url"]), 154)
        self.assertEqual(len(unique_values_by_key["post_author"]), len(unique_values_by_key["post_author_url"]))
        self.assertEqual(len(unique_values_by_key["post_author_rank"]), 4)
        self.assertEqual(len(unique_values_by_key["post_date"]), 154)
        self.assertEqual(len(unique_values_by_key["post_content"]), 154)

if __name__ == "__main__":
    unittest.main()
