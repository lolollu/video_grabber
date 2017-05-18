#!/usr/bin/env python
# encoding: utf-8

import bs_parser
import json

def get_course_list(root_content):

    course_items = root_content.find_all("a", class_="wh wh1")
    container = []
    for item in course_items:
        try:
            hrf = item["href"]
        except:
            hrf = None
        info = item.find_all("div")
        order = info[0].string
        try:
            name = info[1].string
        except:
            name = None

        if name == None:
            continue

        video_name = r'%s_%s.mp4'%(order.encode('utf8'),name.encode('utf8'))
        video_web_page = r'http://ptr.chaoxing.com%s'%hrf.encode('utf8')
        container.append((video_name,video_web_page))
    return container


if __name__ == '__main__':
    video_dst = './video_test/'
    root_url = r'http://ptr.chaoxing.com/course/2533204.html'
    html_txt = bs_parser.html_text(root_url)
    root_content = bs_parser.bs_obj(html_txt)

    video_pages = get_course_list(root_content)

    for i in video_pages:
        sub_html_txt = bs_parser.html_text(i[1])
        sub_content = bs_parser.bs_obj(sub_html_txt)
        it = sub_content.find("iframe")["data"]
        dict_content = json.loads(it.encode('utf8'))
        try:
            video_url = "http://ptr.chaoxing.com/ananas/status/" + dict_content['objectid']
        except:
            continue
        #print video_url
        video_dict = bs_parser.html_text(video_url)
        #print video_dict
        try:
            hd_video_url = json.loads(video_dict)["httphd"]
        except:
            hd_video_url = json.loads(video_dict)['http']

        bs_parser.downloader(hd_video_url,video_dst,i[0])

        #print hd_video
        #video_id = sub_content.find("iframe").string.encode('utf8').split(':')[1]




