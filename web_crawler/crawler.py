import urlparse
import urllib
import time
import httplib2
import logging
from collections import defaultdict
from bs4 import BeautifulSoup
from robotparser import RobotFileParser


DEFAULT_AGENTNAME = 'Bot'
DEFAULT_LIMIT_WIDTH = 10
DEFAULT_LIMIT_DEPTH = 5
BAD_CODES = (301, 303, 307, 404, 410, 500, 501, 502, 503, 504)

def benchmark(func):
    
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print time.clock() - t
        return res

    return wrapper


class WebCrawler(object):
    
    def __init__(self, agent_name=DEFAULT_AGENTNAME,
                limit_width=DEFAULT_LIMIT_WIDTH,
                limit_depth=DEFAULT_LIMIT_DEPTH):
        self._limit_width = limit_width
        self._limit_depth = limit_depth
        self._agent_name = agent_name

    def _allowed_to_open(self, url):
        host = urlparse.urlsplit(url)[1]
        robots_url = urlparse.urlunsplit(('http', host, '/robots.txt', '', ''))
        rp = RobotFileParser(robots_url)
        try:
            rp.read()
        except:
            return False
        return rp.can_fetch(self._agent_name, url)

    def _request_head(self, url):
        h = httplib2.Http()
        resp = h.request(url, "HEAD")[0]
        return resp['status']

    def _check_url(self, url):
        status = self._request_head(url)
        if not status or status in BAD_CODES:
            return False
        return self._allowed_to_open(url)

    def traverse(self, start_url):
        # import pdb; pdb.set_trace()
        if not self._check_url(start_url):
            return []
        level = 0
        temp = defaultdict(list)
        temp[level].append(start_url)
        urls = [start_url]
        while True:
            if temp[level] == []:
                temp.pop(level)
                level += 1
                if temp[level] == [] or level + 1 > self._limit_depth:
                    return urls
            cur_url = temp[level][0]
            temp[level].pop(0)
            try:
                htmltext = urllib.urlopen(cur_url).read()
            except:
                continue
            soup = BeautifulSoup(htmltext)
            width = 0
            for tag in soup.findAll('a', href=True):
                tag['href'] = urlparse.urljoin(start_url, tag['href'])
                if url in tag['href'] and tag['href'] not in urls:
                    if not self._check_url(tag['href']):
                        continue
                    width += 1
                    if width > self._limit_width:
                        break
                    temp[level + 1].append(tag['href'])
                    urls.append(tag['href'])
        return urls


if __name__ == "__main__":
    crawler = WebCrawler()
    url = "http://habrahabr.ru"
    print crawler.traverse(url)
