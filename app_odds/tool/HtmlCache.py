# -*- coding: UTF8 -*-
import codecs
import hashlib
import os.path
import time
import urllib.request

class HtmlCache:
    def getContent(self,url,encoding = 'utf-8',cache = 1,timeout = 30*60):
        if cache:
            m = hashlib.md5()
            m.update(url.encode())
            md5value = m.hexdigest()

            fpath = './data/{0}.html'.format(md5value)
            if os.path.exists(fpath) and timeout != None and (time.time() - os.path.getmtime(fpath) < timeout):
                with codecs.open(fpath,'r',encoding) as f:
                    return f.read()
            else:
                html = urllib.request.urlopen(url).read().decode(encoding,errors = 'ignore')
                if not os.path.exists('./data/'):
                    os.makedirs('./data/')
                with codecs.open(fpath, 'w', encoding) as outfile:
                    outfile.write(html)
                return html
        else:
            html = urllib.request.urlopen(url).read().decode(encoding)
            return html

