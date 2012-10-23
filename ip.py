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


# http://www.angryobjects.com/2011/10/15/http-with-python-pycurl-by-example/

'''

c = pycurl.Curl()
c.setopt(c.URL, 'http://myappserver.com/ses1')
c.setopt(c.CONNECTTIMEOUT, 5)
c.setopt(c.TIMEOUT, 8)
c.setopt(c.COOKIEFILE, '')
c.setopt(c.FAILONERROR, True) # <-------------------------------------------
c.setopt(c.HTTPHEADER, ['Accept: text/html', 'Accept-Charset: UTF-8'])
try:
    c.perform()

    c.setopt(c.URL, 'http://myappserver.com/ses2')
    c.setopt(c.POSTFIELDS, 'foo=bar&bar=foo')
    c.perform()
except pycurl.error, error:
    errno, errstr = error
    print 'An error occurred: ', errstr

'''

#  cookies = tempfile.mkstemp()

'''

#!/usr/bin/env python
import pycurl
import tempfile
import cStringIO

tmp = tempfile.NamedTemporaryFile()
buf = cStringIO.StringIO()

c = pycurl.Curl()
c.setopt(c.URL, 'http://google.com/')
c.setopt(c.FOLLOWLOCATION, 1)
c.setopt(c.COOKIEFILE, tmp.name)
c.setopt(c.COOKIEJAR, tmp.name)
c.setopt(c.WRITEFUNCTION, buf.write)
c.perform()

html = buf.getvalue()
buf.close()
tmp.close()
print "done"
