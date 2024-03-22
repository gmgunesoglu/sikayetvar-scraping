# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 12:01:30 2018

@author: Mehmet Sonmez
"""

import csv
import requests
import time
import re
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from complaint import Complaint
from reply import Reply
from complained_item import ComplainedItem
from brand import Brand

# user agent... 
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'
}

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    time.sleep(1)
    print(f"GET: {url}")
    try:
        with closing(requests.get(url, headers=headers, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                print(f"None url: {url}")
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)
    

# tüm markaların linklerini getirsin    
def get_initial_complained_items():
    url = "https://www.sikayetvar.com/tum-markalar"
    raw_htlm = simple_get(url)
    soup = BeautifulSoup(raw_htlm, 'html.parser')
    last_page = soup.find("ul", class_="pagination ga-v ga-c").find_all("a")[-2].text
    last_page_number = int(last_page)
    brand_list = []
    for i in range(1, 2):
        url_with_pagination = url + "?page=" + str(i)
        raw_html = simple_get(url_with_pagination)
        soup = BeautifulSoup(raw_html, 'html.parser')
        complaints = soup.find_all("div", attrs={"class":"brand-rate"})
        for complaint in complaints:
            brand_name = complaint.find("span", class_="brand-name").text
            brand_link = complaint.find("a")["href"]
            rating = complaint.find("div", class_="rate-num").text.split()[0]
            rating_count = complaint.find("span", class_="without-brackets").text
            rating_count = rating_count.split(" ",1)[0]
            rating_count = rating_count.replace(".","")
            complained_item = ComplainedItem(brand_link, brand_name, int(rating), int(rating_count), None, brand_link)
            brand_list.append(complained_item)  
    return brand_list

def get_brands(initial_complained_items = []):
    base_url = "https://www.sikayetvar.com"
    brand_list = []
    for complained_item in initial_complained_items:
        report_url = base_url + complained_item.href + complained_item.href + "-marka-karnesi"
        raw_html = simple_get(report_url)
        soup = BeautifulSoup(raw_html, 'html.parser')
        brand_report = soup.find_all("div", attrs={"class":"data-count"})
        complaint_count = brand_report[1].find("p").get_text().strip().replace(".","")
        reply_count = 0
        reply_sec = 0
        reply_text = brand_report[0].find("p").get_text().strip()
        if reply_text != "-":
            reply_count = int(reply_text.replace(".",""))
        reply_time_text = brand_report[3].find("p").get_text()
        if reply_time_text != "-":
            match = re.match(r'(?:(\d+)\s*sa)?\s*(?:(\d+)\s*dk)?\s*(?:(\d+)\s*sn)?', reply_time_text)
            hours = int(match.group(1) or 0)
            minutes = int(match.group(2) or 0)
            seconds = int(match.group(3) or 0)
            reply_sec = hours*3600 + minutes*60 + seconds
        brand = Brand(complained_item.href, complained_item.name, reply_count, complaint_count, reply_sec, complained_item.rating_count, complained_item.rating)
        brand_list.append(brand)
    return brand_list

# şikayet edilen nesne için alt/üst sınıf bilgilerini girer ve kaydeder
# tek sorumluluk prensibineuymuyor ama işlemleri hızlandıracak
def expend_and_save_complained_item(complained_items=[]):
    complained_item: ComplainedItem
    for complained_item in complained_items:
        url = "https://www.sikayetvar.com" + complained_item.href
        raw_html = simple_get(url)
        soup = BeautifulSoup(raw_html, 'html.parser')
        complaint_div = soup.find("div", attrs={"class":"brand-detail-grid__main"})
        print("----" + complained_item.href + "----")
        if complaint_div.find("section", recursive=False):
            print("var...")
        else: 
            print()




BASE_URL = "http://www.sikayetvar.com"
initial_complained_items = get_initial_complained_items()
# brands = get_brands(initial_complained_items)
# brand: Brand
# for brand in brands:
#     print(f"href: {brand.href}\nname: {brand.name}\nreplied complaint: {brand.replied_complaint}\ntotal complaint: {brand.total_complaint}\naverage reply sec: {brand.average_reply_sec}\nrating count: {brand.rating_count}\nrating: {brand.rating}")
# print(f"total brand count: {len(brands)}")
expend_and_save_complained_item(initial_complained_items)

# print(f"Found {len(brands_href_list)} brands.")
# scrape_brands(brands_href_list, BASE_URL)
# for brand_href in brands_href_list:
#     print(brand_href)

brand_names = []  #bi dursun sonra silersin şimdi aşağısı çalışmasın
for brand in brand_names:
    BRAND_URL = BASE_URL + "/" + brand
    raw_html = simple_get(BRAND_URL)
    soup = BeautifulSoup(raw_html, 'html.parser')
    item_pages = []
    last_page = soup.find("ul", class_="pagination-list").find_all("a", class_="page")[-1].text.strip()
    last_page_number = int(last_page)
    print(f"there are {last_page_number} pages about {brand}")
    print()

    
    total_complaints = 0
    # complaints = soup.find_all("a", attrs={"class":"complaint-layer"})
    # total_complaints += len(complaints)
    # for complaint in complaints:
    #     item_pages.append(complaint["href"])

    for i in range (1, last_page_number+1):
        BRAND_PAGE_URL = BRAND_URL + "?page=" + str(i)
        raw_html = simple_get(BRAND_PAGE_URL)
        soup = BeautifulSoup(raw_html, 'html.parser')
        complaints = soup.find_all("a", attrs={"class":"complaint-layer"})
        total_complaints += len(complaints)
        for complaint in complaints:
            item_pages.append(complaint["href"])

    print(f"found {total_complaints} complaints about {brand}")
    
    complaint_number = 0
    for page in item_pages:
        complaint_number += 1
        my_url = BASE_URL + page
        print(f"\nComplaint {complaint_number}:")
        raw_html = simple_get(my_url)
        soup = BeautifulSoup(raw_html, 'html.parser') 
    
        title = soup.find("h1",{"class":"complaint-detail-title"}).text.strip('\n')
        print(f"TITLE: {title}")
        description = soup.find("div", {"class":"complaint-detail-description"}).text.strip('\n')
        print(f"DESCRIPTION: {description}")
        date = soup.find("div", {"class": "js-tooltip time"})["title"]
        print(f"DATE: {date}")
        view_count = soup.find("span",{"class":"js-view-count"}).text
        views = "0"
        if view_count != "-":
            views = view_count
        print(f"VIEWS: {views}")
        complainer_url = soup.find("div", {"class": "profile-img"})["data-href"]
        complainer = complainer_url[5:]
        print(f"COMPLAINER: {complainer}")

        complaint = Complaint(title, description, date, view_count, complainer)
        # complaint_list.append(complaint)

 
    