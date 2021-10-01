#-*- coding: utf-8 -*-

import urllib2
import codecs
import os.path
from retry import retry
from Paper3_Methods import *


pagenum=1617121

#True value
maxpage=9999999

#Test value
#maxpage=2

filename=str(pagenum).zfill(7)+'.html'
path='/1-1000'

url = 'http://hotels.ctrip.com/international/'+str(pagenum)+'.html'

##Proxy and encoding settings
proxy = urllib2.ProxyHandler({
    'http': 'REDACTED',
    'https':'REDACTED'
})
opener = urllib2.build_opener(proxy)
opener.addheaders = [('Accept-Charset', 'utf-8')]
urllib2.install_opener(opener)
##

#Retry, URLError Timeout handling
@retry(urllib2.URLError, tries=10, delay=5, backoff=3)
def urlopen_with_retry(url):
    return urllib2.urlopen(url)

def make_path(pagenum):
    foldernum=(pagenum//1000)+1
    minw=((foldernum-1)*1000)
    maxw=minw+999
    path=str(minw)+' - '+str(maxw)
    filename=str(pagenum).zfill(7)+'.html'
    halfpath = make_data_path("ctrip/HTML_extracts/{}".format(path))
    if not os.path.isdir(halfpath): os.makedirs(halfpath)
    fullpath = os.path.join(halfpath, filename)
    return fullpath

def extract_HTML(url, fullpath):
    site = urlopen_with_retry(url)
    data = site.read().decode('utf-8')
    with codecs.open(fullpath, "w", 'utf-8') as html:
        html.write(data)

def main():
    for i in range(pagenum,maxpage):
        pagenum=i
        fullpath=make_path(pagenum)
        url = 'http://hotels.ctrip.com/international/'+str(pagenum)+'.html'
        extract_HTML(url, fullpath)
        #current_time = str(datetime.datetime.now())
        print 'URL request: ' +url + ' extracted to file: ' + fullpath
        #+ ' at DateTime: ' + current_time

if __name__ == '__main__':
    main()
    

