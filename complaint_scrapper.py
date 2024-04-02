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
from entity import Brand, ComplainedItem, Complaint, Reply, Member, ErrorLog
from dao import MemberDao, ReplyDao, ComplaintDao, ComplainedItemDao, ErrorLogDao

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

def scrape_complaints(complained_items=[]):
    complaints = []
    complained_item: Reply
    for complained_item in complained_items:
        url = BASE_URL + complained_item.href
        raw_html = simple_get(url)
        soup = BeautifulSoup(raw_html, 'html.parser')
        complaint_pages = []
        last_page_number = 1
        last_page = soup.find("ul", class_="pagination-list")
        if last_page:
            last_page = last_page.find_all("a", class_="page")[-1].text.strip()
            last_page_number = int(last_page)
        print(f"there are {last_page_number} pages about {complained_item.brand}")
        print()
        total_complaints = 0
        for i in range (1, 2): #@ last_page_number+1
            url_with_pagination = url + "?page=" + str(i)
            raw_html = simple_get(url_with_pagination)
            soup = BeautifulSoup(raw_html, 'html.parser')
            main_content = soup.find("main", attrs={"class":"content"})
            complaints_layer = main_content.find_all("a", attrs={"class":"complaint-layer"})
            total_complaints += len(complaints_layer)
            for complaint in complaints_layer:
                complaint_pages.append(complaint["href"])

   
        print(f"found {total_complaints} complaints about {complained_item.brand}")
        
        complaint_number = 0
        for complaint_page in complaint_pages:
            complaint_number += 1
            complaint_url = BASE_URL + complaint_page
            print(f"\nComplaint {complaint_number}:")
            raw_html = simple_get(complaint_url)
            soup = BeautifulSoup(raw_html, 'html.parser') 
        
            # title = soup.find("h1",{"class":"complaint-detail-title"}).text.strip()
            title = soup.find("title").text.strip()
            print(f"TITLE: {title}")
            description = soup.find("div", {"class":"complaint-detail-description"})
            if description is None:
                description = "No description for: " + complaint_url
            else:
                description = description.text.strip('\n')
            print(f"DESCRIPTION: {description}")
            date_str = soup.find("div", {"class": "js-tooltip time"})["title"].strip()
            print(f"DATE: {date_str}")
            view_count = soup.find("span",{"class":"js-view-count"}).text
            views = "0"
            if view_count != "-":
                views = view_count.replace(".","")
            print(f"VIEWS: {views}")
            complainer_url = soup.find("div", {"class": "profile-img"})["data-href"]
            member_href = complainer_url[4:]
            print(f"COMPLAINER: {member_href}")
            rating_div = soup.find("div", {"data-ga-element": "Result_Stars"})
            rating = None
            if rating_div:
                rating = int(rating_div.find("span", {"class": "rate-num"}).text.strip())
            date = string_to_date(date_str)
            complaint_detail_head_div = soup.find("div", {"class": "complaint-detail-head"})
            solved = False
            if complaint_detail_head_div:
                if complaint_detail_head_div.find("div", {"class": "solved-badge"}):
                    solved = True
            like_count = 0
            like_count_span = soup.find("span", {"class": "total-support"})
            if like_count_span:
                like_count_str = like_count_span.text.strip().replace(".","")
                like_count_str = like_count_str.split()[0]
                like_count = int(like_count_str)
            print("like count:", like_count)

            member = Member(member_href)
            member = MemberDao.add_or_update(member)
            complaint = Complaint(complaint_page, complained_item.id, title, description, date, int(views), like_count, member.id, rating, solved)
            print(f"solved: {solved}")
            print(f"solved: {complaint.solved}")

            complaint = ComplaintDao.add_or_update(complaint)

            answers_container = soup.find("div", {"class": "complaint-answer-container"})
            if answers_container:
                answer_divs = answers_container.find_all("div", recursive=False)
                print("Cevaplaar....")
                for answer_div in answer_divs:
                    is_from_brand = False 
                    tags = answer_div.get("class")
                    if "ga-c" in tags and "ga-v" in tags:
                        is_from_brand = True 
                    reply_date_str = answer_div.find("div", class_="post-time").text.strip()
                    message = answer_div.find("p", class_="message").text.strip().replace("\n","")
                    reply_date = convert_to_datetime(reply_date_str)
                    print("Mesaj:", message)
                    print("Gönderim Tarihi:", reply_date)
                    print("Gönderen marka mı:", is_from_brand)
                    reply = Reply(complaint.id, message, date, is_from_brand)
                    reply = ReplyDao.add(reply)
                    complaint.replies.append(reply)

            complaints.append(complaint)
    return complaints


# MAIN PROCESS

# required for convert string to datetime
locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')

# 5- tüm complained_items lar dan
# sayfalar gezilip şikayetler, üye ve cevaplarla birlikle oluşturulup
# veri tabanına kaydediliyor
items = ComplainedItemDao.get_all()
complaints = scrape_complaints(items)
