#!/usr/bin/env python
import pycurl
import cStringIO

proxy_host = '174.122.73.120'
proxy_port = 3128
proxy_user = 'ip3'
proxy_pass = 'ohzahnohdohnuyoseeph'

buf = cStringIO.StringIO()

c = pycurl.Curl()
c.setopt(c.URL, 'http://checker.mac-blog.org.ua/ip.php')
c.setopt(c.FAILONERROR, 1)
c.setopt(c.PROXY, proxy_host)
c.setopt(c.PROXYPORT, proxy_port)
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
    print 'Erorr: ', errstr

buf.close()
