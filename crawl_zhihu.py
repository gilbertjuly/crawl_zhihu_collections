#! /usr/bin/python
#coding = utf-8
import urllib, urllib2
import random
import re
import sys, os, shutil

from bs4 import BeautifulSoup #for BS4
#from BeautifulSoup import BeautifulSoup #for BS3


##################################################################
### Someone's Favorite -> Collections -> Pages -> Hrefs(Questions)
### the point is to get question links on each page

collection_name = None
user_name = None
#tags_list = []

user_agents = [ 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
                'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
                'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ (KHTML, like Gecko) Element Browser 5.0', \
                'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
                'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
                'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
                'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25', \
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36', \
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']


http_handler = urllib2.HTTPHandler(debuglevel=1)
opener = urllib2.build_opener(http_handler)
urllib2.install_opener(opener)


def crawl_zhihu(url):
    ### Crawling for one Collection in someone's Favorite ###
    url_one_folder = url
    page_idx = 1
    url_page_in_folder = url_one_folder + "?page=%s"%page_idx
    hrefs_list = []
    
    
    ### Crawling for one Page in one Collection ###
    while url_page_in_folder != None:
        user_agent_index = random.randint(0, 9)
        user_agent = user_agents[user_agent_index]

        #print url_page_in_folder
        next_page_idx = page_idx + 1
        request = urllib2.Request(url_page_in_folder, data=None, headers={'User-Agent': user_agent})
        #request.add_header('User-agent', user_agent)
    
        try:
            response = urllib2.urlopen(request)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
            exit()

        html_page_in_folder = response.read()
     
        soup = BeautifulSoup(html_page_in_folder)

        if page_idx == 1:
            collection_tag = soup.find('h2', attrs={
                            'id':r'zh-fav-head-title', 
                            'class':r'zm-item-title zm-editable-content'})
            #m = re.search(r'[\S]', collection_tag.text)
            #print m.span()
            collection_name = collection_tag.text[2:-1]
            #print collection_name
            user_tag = soup.find('h2', attrs={
                            'class':r'zm-list-content-title'})
            user_name = user_tag.a.text
            dst_path = os.path.join(user_name, collection_name)
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)
            #print dst_path 
            #exit()

        #itemlist = soup.findAll('h2', attrs={'class':'zm-item-title'})
        tags_list = soup.findAll('a', attrs={ 
                            'class':None, 
                            'href':re.compile(r'question'), 
                            'target':r'_blank'})

        ### Crawling for one question in one Page ###
        for tag in tags_list:
            #print tag['href']
            #print tag.text
            tag_href = 'http://www.zhihu.com' + tag['href']
            #print tag_href
            #hrefs_list.append(tag_href)
            new_file = '%s.html'%tag.text
            open(new_file, 'w').write((urllib2.urlopen(tag_href)).read())
            try:
                dst_file = os.path.join(dst_path, new_file)
                if not os.path.exists(dst_file):
                    shutil.move(new_file, dst_path)
            except (OSError, IOError), e:
                pass
    
        reg_next_page = 'page=%s' % next_page_idx
        next_page = soup.find('a', attrs={'href':re.compile(reg_next_page)})
    
        if next_page == None:
            url_page_in_folder = None
        else:
            url_page_in_folder = url_one_folder + next_page['href']
            page_idx = next_page_idx
    

if __name__ == '__main__':
    if(len(sys.argv)==2) and (sys.argv[1].startswith(r'http://www.zhihu.com/collection/')):
        crawl_zhihu(sys.argv[1])
    else:
        print '''
        Command Paramters Error!
        Command Usage:
            python crawl_zhihu.py [someone's collection url]
        COmmand example:
            python crawl_zhihu.py http://www.zhihu.com/collection/31085150
        '''




