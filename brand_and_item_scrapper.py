# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 12:01:30 2018

@author: Mehmet Sonmez
"""

import locale
import requests
import time
import re
from datetime import datetime, timedelta
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from entity import Brand, ComplainedItem, Reply, ErrorLog
from dao import ComplainedItemDao, BrandDao, ErrorLogDao

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
        brand_divs = soup.find_all("div", attrs={"class":"brand-rate"})
        for brand_div in brand_divs:
            brand_name = brand_div.find("span", class_="brand-name").text
            brand_link = brand_div.find("a")["href"]
            rating = brand_div.find("div", class_="rate-num").span.text
            rating_count = brand_div.find("span", class_="without-brackets").text
            rating_count = rating_count.split(" ",1)[0]
            rating_count = rating_count.replace(".","")
            complained_item = ComplainedItem(brand_link, brand_name, int(rating), int(rating_count), None, None)
            brand_list.append(complained_item)  
    return brand_list

def scrape_brands(initial_complained_items = []):
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
        brand = BrandDao.add_or_update(brand)
        brand_list.append(brand)
    return brand_list

def print_brands(brands=[]):
    brand: Brand
    for brand in brands:
        print(f"href: {brand.href}\nname: {brand.name}\nrepiled complaint: {brand.replied_complaint}\ntotal complaint: {brand.total_complaint}\naverage reply sec: {brand.average_reply_sec}\nrating: {brand.rating}\nrating count: {brand.rating_count}\n")

def print_complained_item(item: ComplainedItem):
    print(f"id: {item.id}\nhref: {item.href}\nname: {item.name}\nrating: {item.rating}\nrating count: {item.rating_count}\nupper item id: {item.upper_item_id}\nbrand id: {item.brand_id}\nis leafe: {item.is_leaf}\n")

def print_complained_items(complained_items=[]):
    item: ComplainedItem
    for item in complained_items:
        print(f"id: {item.id}\nhref: {item.href}\nname: {item.name}\nrating: {item.rating}\nrating count: {item.rating_count}\nupper item id: {item.upper_item_id}\nbrand id: {item.brand_id}\nis leafe: {item.is_leaf}\n")

def print_complaints(complaints=[]):
    complaint: Reply
    for complaint in complaints:
        print(f"href: {complaint.href}\ncomplained item: {complaint.complained_item}\ntitle: {complaint.title}\ndate: {complaint.date}\nview count: {complaint.view_count}\ncomplain owner: {complaint.complain_owner}\nrating: {complaint.rating}\nsolved: {complaint.sovled}")
        print("replies:")
        reply: Reply
        for reply in complaint.replies:
            print(f"href: {reply.href}\nmessage: {reply.message}\ndate: {reply.date}\nis from brand: {reply.is_from_brand}")
        print()

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
                print_complained_item(complained_item) # @+ sonra sil
                complained_item = ComplainedItemDao.add_or_update(complained_item)
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
                    next_item = ComplainedItem(link["href"], name, rating, rating_count, complained_item.id, complained_item.brand_id)
                    next_generation_compained_items.append(next_item)
            else:
                ComplainedItemDao.add_or_update(complained_item)
        else:
            ComplainedItemDao.add_or_update(complained_item)
    return next_generation_compained_items

def string_to_date(date_string):
    # Şuanki yıl bilgisini alın
    parameters = len(date_string.split())
    try:
        if parameters == 2:
            date = datetime.strptime(date_string, "%B %d %H:%M").date()
        elif parameters == 3:
            date_string = f"{datetime.now().year} {date_string}"
            date = datetime.strptime(date_string, "%Y %d %B %H:%M").date()
        elif parameters == 4:
            date = datetime.strptime(date_string, "%d %B %Y %H:%M").date()
        else:
            print("[-] Date string has much parameters!")
        return date
    except ValueError:
        print("[-] Unexpected date format!")
        print(f"({date_string})")
        print(parameters)
        print(date_string.split())
        return None

def convert_to_datetime(time_str):
    if "saniye" in time_str:
        seconds = int(time_str.split()[0])
        return datetime.now() - timedelta(seconds=seconds)
    
    elif "dakika" in time_str:
        minutes = int(time_str.split()[0])
        return datetime.now() - timedelta(minutes=minutes)
    
    elif "saat" in time_str:
        hours = int(time_str.split()[0])
        return datetime.now() - timedelta(hours=hours)
    
    elif "gün" in time_str:
        days = int(time_str.split()[0])
        return datetime.now() - timedelta(days=days)
    
    elif "hafta" in time_str:
        weeks = int(time_str.split()[0])
        return datetime.now() - timedelta(weeks=weeks)
    
    else:
        try:
            # Eğer saniye, dakika, saat, gün veya hafta içermiyorsa
            # ve '%d %B %H:%M' formatına uyuyorsa bu formata göre çevir

            return string_to_date(time_str)
        except ValueError:
            print("Geçersiz tarih formatı:", time_str)
            return None


# MAIN PROCESS

# required for convert string to datetime
locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')

# 1- tüm markalara gidip initial_complained_items oluşturuluyor
initial_complained_items = get_initial_complained_items()    

# 2- initial_complained_items daki markaların karnelerine gidip 
# brandler oluşturulup veri tabanına kaydediliyor
scrape_brands(initial_complained_items)

# 3- initial_complained_items daki brand_id ler dolduruluyor
for item in initial_complained_items:
    item.brand_id = BrandDao.get_by_href(item.href).id
    item.upper_item_id = None

# 4- tüm alt dalları ile birlikte complained_items oluşturulup 
# veri tabanına kaydediliyor
father_items = initial_complained_items
generation = 0
while True: 
    child_items = scrape_complained_items(father_items)
    print(f"--- {generation}. Generation Items ---")
    generation +=1
    print_complained_items(father_items)
    if len(child_items) == 0:
        break
    father_items = child_items


