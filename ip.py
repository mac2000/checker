#!/usr/bin/env python
import pycurl
import cStringIO
from pyquery import PyQuery as pq
from lxml import etree

buf = cStringIO.StringIO()

c = pycurl.Curl()
c.setopt(c.URL, 'http://myip.ru/')
c.setopt(c.FOLLOWLOCATION, 1)
c.setopt(c.WRITEFUNCTION, buf.write)
c.perform()

html = buf.getvalue()
buf.close()

#print html

d = pq(html)
#d = pq(etree.fromstring(html))

el = d('table table table tr:last-child td')

print el.text()
#print el.html()
