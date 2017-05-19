#!/usr/bin/env python
# encoding: utf-8

import bs_parser

main_url = r'http://www.cfaspace.com'

def get_title(content):
    s =  content.find("h3", class_="heading-title").contents[0].replace('\r\n','').strip(' ').replace(' ','_')
    print s
    return s

def get_doc_url(content):
    s= content.find_all('span', class_='pull-right')[0].find('a')['href']
    print s
    return s

def get_video_url(content):
    s = content.find('video').find('source')['src']
    print s
    return s

def get_course_list(content):
    course_list = content.find("div", class_="list_video").find_all('a')
    list_container = []
    for i in course_list:
        list_container.append(main_url+i['href'])
    return list_container

if __name__ == "__main__":
    src = r'http://www.cfaspace.com/course/detail/ea3a92dd409c51ff0140d7888abe1ac1'
    text = bs_parser.html_text(src)
    #with open('html_test','w') as f:
    #    f.write(text)
    with open('html_test','r') as f:
        content = f.read()
    bs_content = bs_parser.bs_obj(content)

    course_list = get_course_list(bs_content)
    for one_class in course_list[:2]:
        class_text = bs_parser.html_text(one_class)
        class_content = bs_parser.bs_obj(class_text)

        title = get_title(class_content)
        doc_link = main_url + get_doc_url(class_content)
        video_link = main_url + get_video_url(class_content)



