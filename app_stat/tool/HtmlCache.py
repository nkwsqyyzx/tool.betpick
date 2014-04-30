# -*- coding: UTF8 -*-
import codecs
import hashlib
import os.path
import time
import urllib.request

class HtmlCache:
    def __init__(self, basepath):
        self.basepath = basepath


    def getCachedHtml(self, url, encoding, timeout):
        m = hashlib.md5()
        m.update(url.encode())
        md5value = m.hexdigest()
        html = None
        fpath = '{0}{1}.html'.format(self.basepath, md5value)
        if os.path.exists(fpath) and ((time.time() - os.path.getmtime(fpath) < timeout) and timeout or True):
            with codecs.open(fpath, 'r', encoding) as f:
                html = f.read()
        return html, fpath

    def getContent(self, url, encoding='utf-8', cache=1, timeout=30 * 60):
        if cache:
            html, fpath = self.getCachedHtml(url, encoding, timeout)

            if html:
                return html
            else:
                html = urllib.request.urlopen(url).read().decode(encoding, errors='ignore')
                if not os.path.exists(self.basepath):
                    os.makedirs(self.basepath)
                with codecs.open(fpath, 'w', encoding) as outfile:
                    outfile.write(html)
                return html
        else:
            html = urllib.request.urlopen(url).read().decode(encoding)
            return html

    def getContentWithAgent(self, url, encoding='utf-8', cache=1, timeout=30 * 60, userAgent='Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'):
        if cache:
            html, fpath = self.getCachedHtml(url, encoding, timeout)

            if html:
                return html
            else:
                request = urllib.request.Request(url)
                request.add_header('User-Agent', userAgent)
                r = urllib.request.urlopen(request)
                html = r.read().decode(encoding, errors='ignore')
                if not os.path.exists(self.basepath):
                    os.makedirs(self.basepath)
                with codecs.open(fpath, 'w', encoding) as outfile:
                    outfile.write(html)
                return html
        else:
            request = urllib.request.Request(url)
            request.add_header('User-Agent', userAgent)
            r = urllib.request.urlopen(request)
            html = r.read().decode(encoding, errors='ignore')
            return html
