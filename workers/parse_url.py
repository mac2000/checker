#!/usr/bin/env python
#-*- conding: utf-8 -*-
import re
from urlparse import urlparse

def parse_url(url):
    regex = re.compile('((?P<user>\w+):(?P<pass>\w+)@)?(?P<host>[^:$]+)(:(?P<port>\d{2,5}))?', re.IGNORECASE);
    parts = urlparse(url)
    m = regex.match(parts.netloc)
    return {
        'scheme': parts.scheme or None,
        'netloc': parts.netloc or None,
        'path': parts.path or None,
        'params': parts.params or None,
        'query': parts.query or None,
        'fragment': parts.fragment or None,
        'user': m.group('user'),
        'pass': m.group('pass'),
        'host': m.group('host'),
        'domain': m.group('host').replace('www.', '') or None,
        'port': m.group('port') or None
    }

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description = 'Parse URL')
    parser.add_argument('url', help = 'URL to parse')
    args = parser.parse_args()

    if not args.url.startswith('http'):
        parser.error('Wrong url given')

    result = parse_url(args.url)
    for k, v in result.items():
        print "%10s: %s" % (k, v)
