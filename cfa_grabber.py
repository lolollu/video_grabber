#!/usr/bin/env python
# encoding: utf-8

import bs_parser
import os,sys

main_url = r'http://www.cfaspace.com'

def get_title(content):
    s =  content.find("h3", class_="heading-title").contents[0].replace('\r\n','').strip(' ').replace(' ','_')
    s = s.replace("?",'').replace(":",'').replace("|",'')
    print s
    return s

def get_doc_url(content):
    s= content.find_all('span', class_='pull-right')[0].find('a')['href']
    if s is not None and len(s.split('.')) > 1:
        print s
        return main_url + s
    else:
        print None
        return None

def get_video_url(content):
    s = content.find('video').find('source')['src']
    print s
    return main_url + s

def get_course_list(content):
    course_list = content.find("div", class_="list_video").find_all('a')
    list_container = []
    for i in course_list:
        list_container.append(main_url+i['href'])
    return list_container

if __name__ == "__main__":
    video_root_name  = sys.argv[1]
    video_root_path = r'./{}'.format(video_root_name)
    if not os.path.exists(video_root_path):
        os.mkdir(video_root_path)
    doc_path = os.path.join(video_root_path,'material')
    if not os.path.exists(doc_path):
        os.mkdir(doc_path)

    src = r'http://www.cfaspace.com/course/detail/ea3af1b449915333014992be42290081'
    text = bs_parser.html_text(src)
    #with open('html_test','w') as f:
    #    f.write(text)
    #with open('html_test','r') as f:
    #    content = f.read()
    bs_content = bs_parser.bs_obj(text)

    course_list = get_course_list(bs_content)
    for one_class in course_list:
        class_text = bs_parser.html_text(one_class)
        class_content = bs_parser.bs_obj(class_text)

        title = get_title(class_content)
        video_name = '%s.mp4'%title
        doc_link = get_doc_url(class_content)
        if doc_link is not None:
            print doc_link
            doc_name = '%s.%s'%(title,doc_link.split('.')[-1])
            bs_parser.downloader(doc_link,doc_path,doc_name)

        video_link = get_video_url(class_content)
        bs_parser.downloader(video_link,video_root_path,video_name)





