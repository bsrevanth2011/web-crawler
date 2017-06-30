from domain import *
from urllib.request import urlopen
from link_finder import LinkFinder
from general import *

import threading

class Spider:
    # class variables
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    crawled = set()
    queue = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = project_name + "/queue.txt"
        Spider.crawled_file = project_name + "/crawled.txt"
        self.boot()
        self.crawl_page('Thread-0', base_url)

    @staticmethod
    def boot():
        create_project_directory(Spider.project_name)
        create_project_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + " now crawling " + page_url)
            print(" Queue: " + str(len(Spider.queue)) + " | Crawled: " + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html':
                html_bytes = response.read()
                html_string = html_bytes.decode('utf-8')
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except:
            print('page cannot be crawled')
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        for link in links:
            if link in Spider.queue:
                continue
            if link in Spider.crawled:
                continue
            if Spider.domain_name != get_domain_name(link):
                continue
            Spider.queue.add(link)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue_file, Spider.queue)
        set_to_file(Spider.crawled_file, Spider.crawled)
