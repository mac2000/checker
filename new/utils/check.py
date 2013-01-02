#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import time
import tempfile
import random
import urllib
from fetch import fetch
from parse_url import parse_url
from pyquery import PyQuery as pq

def check(keyword, domain, proxy=None, verbose=False):
    query = 'h3.r a.l'#open('./query.txt').read().strip()
    keyword = urllib.quote_plus(keyword)
    cookies_file = tempfile.NamedTemporaryFile()

    ua = random.choice([
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11',
        'Opera/9.80 (Windows NT 5.1) Presto/2.12.388 Version/12.12',
        'Mozilla/5.0 (Windows NT 5.1; rv:17.0) Gecko/20100101 Firefox/17.0',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11',
        'Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.12',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/17.0',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11',
        'Opera/9.80 (Windows NT 6.2; WOW64) Presto/2.12.388 Version/12.12',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:17.0) Gecko/20100101 Firefox/17.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:17.0) Gecko/20100101 Firefox/17.0',
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11',
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 (KHTML, like Gecko) Ubuntu/12.10 Chromium/22.0.1229.94 Chrome/22.0.1229.94 Safari/537.4',
        'Opera/9.80 (X11; Linux i686) Presto/2.12.388 Version/12.12'
    ])

    fetch('http://google.com/ncr', proxy, ua, cookies_file.name, verbose)
    time.sleep(2)

    for page in range(1, 11):
        start = 10 * (page - 1)
        position = 1 + start

        url = "http://www.google.com/search?q=%s&hl=en" % keyword

        if page > 1:
            url = "%s&start=%d" % (url, start)

        response = fetch(url, proxy, ua, cookies_file.name, verbose)

        dom = pq(response)
        anchors = dom(query)

        for anchor in anchors:
            url = pq(anchor).attr('href')
            parsed = parse_url(url)
            if domain == parsed['domain']:
                return position
            position += 1
        time.sleep(3)

if __name__ == "__main__":
    import argparse
    import re
    parser = argparse.ArgumentParser(description = 'Get keyword domain position')
    parser.add_argument('keyword', help = 'Keyword to search')
    parser.add_argument('domain', help = 'Domain to search')
    parser.add_argument('-q', '--quiet', dest = 'verbose', action = 'store_false', help = 'Toggle output verbose')
    parser.add_argument('-p', '--proxy', dest = 'proxy', action = 'store', help = 'Proxy to use')
    args = parser.parse_args()
    if args.domain.startswith('http') or args.domain.startswith('www.'):
        parser.error('Wrong domain given. Do not use http:// or www.')
    if args.proxy and not args.proxy.startswith('http'):
        parser.error('Wrong proxy given. Must be: http://<user>:<pass>@<host>:<port>')

    try:
        print check(args.keyword, args.domain, args.proxy, args.verbose)
    except Exception as err:
        print err.args[-1]

