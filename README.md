crawl_zhihu_collections
=======================

Zhihu.com is well-known Chinese Answer-Question website just like Quora.
Many people create collections to save good answers or questions.
However, Zhihu doesn't support ways to export one's collection, 
so I write a python spider to crawl one's zhihu collection and save it to local space. 

This is also my learning project for web crawling/spider.
This project needs BeautifulSoup lib support,
Try "easy_install BeautifulSoup4" if it is not installed.


Command Usage
=======================

python crawl_zhihu.py http://www.zhihu.com/collection/31085150



Future todo list
=======================

More robust, able to process different errors;
Multi threads to speed up crawling;
Database support;
Save collections to PDFs not just HTMLs;
