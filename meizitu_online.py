#coding=utf-8

import os
import re
import time
import utils
import requests
from bs4 import BeautifulSoup

headers={'Referer':'http://jandan.net/ooxx/page-290',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

def jiandan(soup,pages):
    # soup, pages = jiandan_get_page_num()
    num = 0
    for page in range(11,int(pages))[::-1]:
        print page
        num += 1
        if num == 10:
            time.sleep(3)
        r = requests.get('http://jandan.net/ooxx/page-%s' % page, headers=headers)
        print r.url
        soup = BeautifulSoup(r.content, 'lxml')
        rows =soup.find_all('div',class_='row')
        for row in rows:
            # print row
            # 喜欢人数
            like = re.search(r'<span>(\d*)</span>',str(row.find_all('span',class_='tucao-like-container')[0])).group(1)
            # 吐槽人数
            unlike = re.search(r'<span>(\d*)</span>', str(row.find_all('span', class_='tucao-unlike-container')[0])).group(1)
            # print like,unlike
            if int(like)>int(unlike):
            # if int(like)>200:
                pictures = row.find_all('a',class_='view_img_link')
                for picture in pictures:
                    if picture['href'].endswith('jpg'):
                        jiandan_upload_picture('http:'+picture['href'])
                    else:
                        # print 'picture is not jpg'
                        pass
            else:
                # print 'unlike more than like people'
                pass

def jiandan_upload_picture(url):
    try:
        r = requests.get(url,headers=headers,timeout=10)
        # r = requests.get(url,headers=headers)
        print r.elapsed.microseconds
        time.sleep(0.1)
        pictrue_name = re.search(r'large/(.*)',url).group(1)
        with open('./meizitu/'+pictrue_name,'wb') as img:
            img.write(r.content)
    except:
        print 'time out'

def jiandan_get_page_num():
    r = requests.get('http://jandan.net/ooxx/',headers=headers)
    soup = BeautifulSoup(r.content,'lxml')
    # 页数
    page = soup.find_all(class_='current-comment-page',limit=1)[0].string.replace('[','').replace(']','')
    # print page
    return soup, page



if __name__=="__main__":
    if not os.path.exists('./meizitu'):
        os.mkdir('./meizitu')
    soup,pages = jiandan_get_page_num()
    jiandan(soup,pages)
