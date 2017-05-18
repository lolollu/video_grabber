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
    with closing(requests.get(url,stream= True)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        if os.path.exists(dst_path) and os.path.getsize(dst_path) == content_size:
            print 'pass ', dst_path
        else:
            progress = ProgressBar(file_name,total = content_size, unit='KB', chunk_size = chunk_size, run_status='Downloading',fin_status="Finished")
            with open(dst_path,'wb') as f:
                for data in response.iter_content(chunk_size=chunk_size):
                    f.write(data)
                    progress.refresh(count = len(data))

















