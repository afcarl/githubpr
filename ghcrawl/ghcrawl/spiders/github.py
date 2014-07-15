from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from ghcrawl.items import Link
import re

class GithubSpider(CrawlSpider):
  name = "github"
  allowed_domains = ["github.com"]
  start_urls = ["http://www.github.com/"]

  rules = (
    Rule(SgmlLinkExtractor(allow=r".*github\.com/\w+/\w+/?$"), callback="parse_item", follow=True),
    Rule(SgmlLinkExtractor(allow=r".*github\.com/\w+$"), callback=None, follow=True),
  )

  def parse_item(self, response):
    project_expr = re.compile(".*github\.com/\w+/\w+/?$")
    sel = Selector(response)
    for anchor in sel.css("#readme a::attr(href)").extract():
      if project_expr.match(anchor):
        yield  Link(source=response.url, target=anchor)