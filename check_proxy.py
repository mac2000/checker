#!/usr/bin/env python
import pycurl
import cStringIO
import sys
import re

if len(sys.argv) < 2:
    sys.exit('Usage example: python check_proxy.py ip3:ohzahnohdohnuyoseeph@174.122.73.120:3128')

match = re.search('(?P<user>[^:]+):(?P<pass>[^@]+)@(?P<host>[^:]+):(?P<port>\d+)', sys.argv[1])

if not match:
    sys.exit('First argument must be in form: user:pass@host:port')

proxy_user = match.group('user')
proxy_pass = match.group('pass')
proxy_host = match.group('host')
proxy_port = match.group('port')
'''
proxy_host = '174.122.73.120'
proxy_port = 3128
proxy_user = 'ip3'
proxy_pass = 'ohzahnohdohnuyoseeph'
'''
buf = cStringIO.StringIO()

c = pycurl.Curl()
c.setopt(c.URL, 'http://checker.mac-blog.org.ua/ip.php')
c.setopt(c.VERBOSE, 1)
c.setopt(c.FAILONERROR, 1)
# c.setopt(c.CONNECTTIMEOUT, 5)
# c.setopt(c.TIMEOUT, 5)
c.setopt(c.PROXY, proxy_host)
c.setopt(c.PROXYPORT, int(proxy_port))
c.setopt(c.PROXYUSERPWD, '%s:%s' % (proxy_user, proxy_pass))
c.setopt(c.WRITEFUNCTION, buf.write)

try:
    c.perform()
    ip = buf.getvalue()
    if ip == proxy_host:
        print "%s == %s" % (proxy_host, ip)
    else:
        print "%s != %s" % (proxy_host, ip)
except pycurl.error, error:
    errno, errstr = error
    print '%s : %s' % (errno, errstr)

buf.close()
