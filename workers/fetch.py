#!/usr/bin/env python
#-*- conding: utf-8 -*-

def fetch(url, proxy = None, ua = None, cookie = None, verbose = True):
    from parse_url import parse_url
    import pycurl
    import cStringIO

    buf = cStringIO.StringIO()
    c = pycurl.Curl()

    c.setopt(c.URL, url)

    if cookie:
        c.setopt(c.COOKIEFILE, cookie)
        c.setopt(c.COOKIEJAR, cookie)

    if ua:
        c.setopt(c.USERAGENT, ua)

    if proxy:
        proxy = parse_url(proxy)
        c.setopt(c.PROXY, proxy['host'])
        c.setopt(c.PROXYPORT, int(proxy['port']))
        c.setopt(c.PROXYUSERPWD, "%s:%s" % (proxy['user'], proxy['pass']))

    # c.setopt(c.CONNECTTIMEOUT, 10)
    # c.setopt(c.TIMEOUT, 20)
    c.setopt(c.FAILONERROR, True)
    c.setopt(c.VERBOSE, verbose)
    c.setopt(c.FOLLOWLOCATION, 1)
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.setopt(c.HTTPHEADER, ['Accept: text/html', 'Accept-Charset: UTF-8'])
    try:
        c.perform()
        status = c.getinfo(c.HTTP_CODE)
        body = buf.getvalue()
        buf.close()
        return {'status': status, 'response': body}
    except pycurl.error, error:
        errno, errstr = error
        return {'status': errno, 'response': errstr}

if __name__ == "__main__":
    import argparse
    import re
    parser = argparse.ArgumentParser(description = 'Fetch URL')
    parser.add_argument('url', help = 'URL to fetch')
    parser.add_argument('-q', '--quiet', dest = 'verbose', action = 'store_false', help = 'Toggle output verbose')
    parser.add_argument('-a', '--useragent', dest = 'ua', action = 'store', help = 'User agent to use')
    parser.add_argument('-c', '--cookie', dest = 'cookie', action = 'store', help = 'Cookies file path to use')
    parser.add_argument('-p', '--proxy', dest = 'proxy', action = 'store', help = 'Proxy to use')
    args = parser.parse_args()
    if not args.url.startswith('http'):
        parser.error('Wrong url given')
    if args.proxy and not args.proxy.startswith('http'):
        parser.error('Wrong proxy given. Must be: http://<user>:<pass>@<host>:<port>')

    response = fetch(args.url, args.proxy, args.ua, args.cookie, args.verbose)

    if response['status'] is 200:
        print response['response']
    else:
        print response
