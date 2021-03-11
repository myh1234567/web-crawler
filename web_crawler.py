import multiprocessing as mp
from urllib.request import urlopen, urljoin
from bs4 import BeautifulSoup
import re

#aaa
base_url = "https://github.com/myhpiok"

def crawl(url):
    response = urlopen(url)
    return response.read().decode()

def parse(html):
    soup = BeautifulSoup(html,"lxml")
    urls = soup.find_all("a",{"href":re.compile("^/.+?/$")})
    title = soup.find("h1").get_text().strip()
    page_urls = set([urljoin(base_url,url["href"]) for url in urls])
    url = soup.find("meta",{"property":"og:url"})["content"]
    return title,page_urls,url


unseen = set([base_url,])
seen = set()

count = 1

while len(unseen) != 0:
    print("Crawling...")
    htmls = [crawl(url) for url in unseen]
    print("Parsing...")
    results = [parse(html) for html in htmls]

    print("Analsysing...")
    seen.update(unseen)
    unseen.clear()

    for title, page_urls, url in results:
        print(count,title,url)
        count += 1
        unseen.update(page_urls - seen)

