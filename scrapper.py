# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 12:01:30 2018

@author: Mehmet Sonmez
"""

import csv
import requests
import time
import re
from datetime import datetime
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from complaint import Complaint
from reply import Reply
from complained_item import ComplainedItem
from brand import Brand
from commit import Commit

# GLOBAL VERIABLES

# user agent
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'
}

BASE_URL = "http://www.sikayetvar.com"


# FUNCTIONS

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    time.sleep(1)
    print(f"GET: {url}")
    try:
        with closing(requests.get(url, headers=HEADERS, stream=True)) as resp:
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
    
def get_initial_complained_items():
    url = "https://www.sikayetvar.com/tum-markalar"
    raw_htlm = simple_get(url)
    soup = BeautifulSoup(raw_htlm, 'html.parser')
    last_page = soup.find("ul", class_="pagination ga-v ga-c").find_all("a")[-2].text
    last_page_number = int(last_page)
    brand_list = []
    for i in range(1, 2): #@ last_page_number + 1
        url_with_pagination = url + "?page=" + str(i)
        raw_html = simple_get(url_with_pagination)
        soup = BeautifulSoup(raw_html, 'html.parser')
        complaints = soup.find_all("div", attrs={"class":"brand-rate"})
        for complaint in complaints:
            brand_name = complaint.find("span", class_="brand-name").text
            brand_link = complaint.find("a")["href"]
            rating = complaint.find("div", class_="rate-num").span.text
            rating_count = complaint.find("span", class_="without-brackets").text
            rating_count = rating_count.split(" ",1)[0]
            rating_count = rating_count.replace(".","")
            complained_item = ComplainedItem(brand_link, brand_name, int(rating), int(rating_count), None, brand_link)
            brand_list.append(complained_item)  
    return brand_list

def get_brands(initial_complained_items = []):
    base_url = "https://www.sikayetvar.com"
    brand_list = []
    for complained_item in initial_complained_commit_owneritems:
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

def print_complained_item(item: ComplainedItem):
    print(f"href: {item.href}\nname: {item.name}\nrating: {item.rating}\nrating count: {item.rating_count}\nupper item: {item.upper_item}\nbrand: {item.brand}\nis leafe: {item.is_leaf}\n")

def print_complained_items(complained_items=[]):
    item: ComplainedItem
    for item in complained_items:
        print(f"href: {item.href}\nname: {item.name}\nrating: {item.rating}\nrating count: {item.rating_count}\nupper item: {item.upper_item}\nbrand: {item.brand}\nis leafe: {item.is_leaf}\n")

def print_complaints(complaints=[]):
    complaint: Complaint
    for complaint in complaints:
        print(f"href: {complaint.href}\ncomplained item: {complaint.complained_item}\ntitle: {complaint.title}\ndate: {complaint.date}\nview count: {complaint.view_count}\ncomplain owner: {complaint.complain_owner}\nrating: {complaint.rating}\nsolved: {complaint.sovled}" )

def scrape_complained_items(complained_items=[]):
    next_generation_compained_items = []
    complained_item: ComplainedItem
    for complained_item in complained_items:
        url = BASE_URL + complained_item.href
        raw_html = simple_get(url)
        soup = BeautifulSoup(raw_html, 'html.parser')
        complaint_div = soup.find("div", attrs={"class":"brand-detail-grid__main"})
        children_section = complaint_div.find("section", recursive=False)
        if children_section:
            swiper_wrapper_div = children_section.find('div', class_='swiper-wrapper')
            if swiper_wrapper_div:
                # cocukları var
                complained_item.is_leaf = False
                links = swiper_wrapper_div.find_all("a", recursive=False)
                for link in links:
                    url = BASE_URL + (link["href"])
                    raw_html = simple_get(url)
                    next_item_soup = BeautifulSoup(raw_html, 'html.parser')
                    item_info_div = next_item_soup.find('div', class_='brand-rate')
                    name = item_info_div.find("h1", class_="model-name ga-v ga-c").contents[-1].strip()
                    ratings_div = item_info_div.find("div", class_="rating-wrap")
                    rating = 0
                    rating_count = 0
                    if ratings_div:
                        rating_nums = ratings_div.find("div", class_="rate-num").find("span").text.strip()
                        rating = int(rating_nums)
                        rating_count_str = ratings_div.find("span",class_="without-brackets").text.strip()
                        rating_count_str = rating_count_str.replace(".", "")
                        rating_count_str = rating_count_str.split()[0]
                        rating_count = int(rating_count_str)
                    next_item = ComplainedItem(link["href"], name, rating, rating_count, complained_item.href, complained_item.brand)
                    next_generation_compained_items.append(next_item)
    return next_generation_compained_items

def string_to_date(date_string):
    # Şuanki yıl bilgisini alın    
    try:
        if len(date_string.split()) == 2:
            date = datetime.strptime(date_string, "%B %d %H:%M").date()
        elif len(date_string.split()) == 3:
            date_string = f"{datetime.now().year} {date_string}"
            date = datetime.strptime(date_string, "%Y %d %B %H:%M").date()
        elif len(date_string.split()) == 4:
            date = datetime.strptime(date_string, "%d %B %Y %H:%M").date()
        else:
            print("[-] Date string has much parameters!")
        return date
    except ValueError:
        print("[-] Unexpected date format!")
        print(f"({date_string})")
        print(len(date_string.split()))
        return None


def scrape_complaints(complained_items=[]):
    complaints = []
    complained_item: ComplainedItem
    for complained_item in complained_items:
        url = BASE_URL + complained_item.href
        raw_html = simple_get(url)
        soup = BeautifulSoup(raw_html, 'html.parser')
        complaint_pages = []
        last_page = soup.find("ul", class_="pagination-list").find_all("a", class_="page")[-1].text.strip()
        last_page_number = int(last_page)
        print(f"there are {last_page_number} pages about {complained_item.brand}")
        print()
        total_complaints = 0
        for i in range (1, 2): #@ last_page_number+1
            url_with_pagination = url + "?page=" + str(i)
            raw_html = simple_get(url_with_pagination)
            soup = BeautifulSoup(raw_html, 'html.parser')
            complaints = soup.find_all("a", attrs={"class":"complaint-layer"})
            total_complaints += len(complaints)
            for complaint in complaints:
                complaint_pages.append(complaint["href"])
   
        print(f"found {total_complaints} complaints about {complained_item.brand}")
        
        complaint_number = 0
        for complaint_page in complaint_pages:
            complaint_number += 1
            complaint_url = BASE_URL + complaint_page
            print(f"\nComplaint {complaint_number}:")
            raw_html = simple_get(complaint_url)
            soup = BeautifulSoup(raw_html, 'html.parser') 
        
            title = soup.find("h1",{"class":"complaint-detail-title"}).text.strip('\n')
            print(f"TITLE: {title}")
            description = soup.find("div", {"class":"complaint-detail-description"}).text.strip('\n')
            print(f"DESCRIPTION: {description}")
            date_str = soup.find("div", {"class": "js-tooltip time"})["title"].strip()
            print(f"DATE: {date_str}")
            view_count = soup.find("span",{"class":"js-view-count"}).text
            views = "0"
            if view_count != "-":
                views = view_count
            print(f"VIEWS: {views}")
            complainer_url = soup.find("div", {"class": "profile-img"})["data-href"]
            complain_owner = complainer_url[5:]
            print(f"COMPLAINER: {complain_owner}")
            
            date = string_to_date(date_str)
            like_count = 0
            complaint = Complaint(complaint_page, complained_item.href, title, date, view_count, like_count, complain_owner)
            complaints.append(complaint)
    return complaint


# MAIN PROCESS

# gets topl lvl complained items and they are also brand
initial_complained_items = get_initial_complained_items()

# creates brand list with complained items, dont send lower levels complained item lists as parameter!
# brands = get_brands(initial_complained_items)
# brand: Brand
# for brand in brands:
#     print(f"href: {brand.href}\nname: {brand.name}\nreplied complaint: {brand.replied_complaint}\ntotal complaint: {brand.total_complaint}\naverage reply sec: {brand.average_reply_sec}\nrating count: {brand.rating_count}\nrating: {brand.rating}")
# print(f"total brand count: {len(brands)}")

# Hem parametre olarak gönderilen listedeki şikayet edilen nesnede eksik olan alanları doldurur ()
# tek sorumluluk prensibine uymuyor ama işlemleri hızlandıracak

print("--- first gereration after scrape ---")
father_items = initial_complained_items
complaints = scrape_complaints(father_items)
print_complaints(complaints)

# while True: 
#     child_items = scrape_complained_items(father_items)
#     print("--- items ---")
#     print_complained_items(father_items)
#     if len(child_items) == 0:
#         break
#     father_items = child_items

# bu noktada 1. aşama bitiyor (veri tabanı kayıtları yapılmalı)
# en alt seviyedeki(is_leaf = True) complained_item listesini bir sql sorgusu ile oluşturup
# fonksiyona parametre olarak gönder, o da tüm şikayetleri işleyip kayıt etsin (2. aşama)

scrape_complaints(father_items)
 