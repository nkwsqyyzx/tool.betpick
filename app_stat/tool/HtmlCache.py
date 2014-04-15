# -*- coding: UTF8 -*-
import codecs
import hashlib
import os.path
import time
import urllib.request

class HtmlCache:
    def __init__(self,basepath):
        self.basepath = basepath

    def getContent(self,url,encoding = 'utf-8',cache = 1,timeout = 30*60):
        if cache:
            m = hashlib.md5()
            m.update(url.encode())
            md5value = m.hexdigest()

            fpath = '{0}{1}.html'.format(self.basepath,md5value)
            if os.path.exists(fpath) and ((time.time() - os.path.getmtime(fpath) < timeout) and timeout or True):
                with codecs.open(fpath,'r',encoding) as f:
                    return f.read()
            else:
                html = urllib.request.urlopen(url).read().decode(encoding,errors = 'ignore')
                if not os.path.exists(self.basepath):
                    os.makedirs(self.basepath)
                with codecs.open(fpath, 'w', encoding) as outfile:
                    outfile.write(html)
                return html
        else:
            html = urllib.request.urlopen(url).read().decode(encoding)
            return html

