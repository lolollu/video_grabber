#!/usr/bin/env python
# encoding: utf-8

from bs4 import BeautifulSoup

import urllib2
import time
import random
import requests
import os, sys
from contextlib import closing


request_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                  'Accept': 'text/html;q=0.9,*/*;q=0.8',
                  'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                  'Accept-Encoding': 'gzip',
                  'Cookie':r'UM_distinctid=15bc715d39f800-0da9cd36b-4f4b012e-232800-15bc715d3a05ce; bdshare_firstime=1493694726699; OUTFOX_SEARCH_USER_ID_NCOO=1114402987.9810658; Hm_lvt_6d761014fc10be3a449858080fdd278a=1493693750,1493782878,1493979064,1494807336; JSESSIONID=BF208A6350A03B58C3B6E671C84160A3; memberId=ea3a9cb35bbb312c015bbd80b9e10059; loginDate=20170517111442; CNZZDATA1258749969=471695409-1493690447-http%253A%252F%252Fbbs.cfaspace.com%252F%7C1495174552',
                  'Connection': 'close',
                  'Referer': None,
                  }

class ProgressBar(object):
    def __init__(self, title, count=0.0, run_status=None, fin_status=None, total=100.0, unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.statue)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        _info = self.info % (
            self.title, self.status, self.count / self.chunk_size, self.unit, self.seq, self.total / self.chunk_size,
            self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print self.__get_info(), end_str


def html_text(url):

    if url == '' or url is None:
        return None
    try:
        time.sleep(random.random()*0.3)
        request = urllib2.Request(url = url, headers = request_header)
        html = urllib2.urlopen(request)
        return html.read()
    except urllib2.HTTPError as e:
        print 'Http error'
        print e
        return None
    except urllib2.URLError as e:
        print 'Url error'
        print e
        return None
    finally:
        print "html text of !!!%s!!! is done."%url


def bs_obj(text):
    if text == '' or text is None:
        return None
    try:
        bs_obj = BeautifulSoup(text, 'html.parser')
        return bs_obj
    except:
        print "BeautifulSoup parser failed and return None"
    finally:
        print "BeautifualSoup parser Done."

def downloader(url,dst,file_name):
    dst_path = os.path.join(dst,file_name)
    with closing(requests.get(url,stream= True, headers = request_header)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        if os.path.exists(dst_path) and os.path.getsize(dst_path) == content_size:
            print 'pass ', dst_path
        else:
            progress = ProgressBar(file_name,total = content_size, unit='KB', chunk_size = chunk_size, run_status='Downloading',fin_status="Finished")
            with open(dst_path,'wb') as f:
                for data in response.iter_content(chunk_size=chunk_size):
                    f.write(data)
                    f.flush()
                    progress.refresh(count = len(data))

















