# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 12:01:30 2018

@author: Mehmet Sonmez
"""

import csv
import requests
import time
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from complaint import Complaint
from reply import Reply

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
def get_brands_href():
    url = "https://www.sikayetvar.com/tum-markalar"
    raw_htlm = simple_get(url)
    soup = BeautifulSoup(raw_htlm, 'html.parser')
    last_page = soup.find("ul", class_="pagination ga-v ga-c").find_all("a")[-2].text
    last_page_number = int(last_page)
    brands_href_list = []
    for i in range(1, 3+1):
        url_with_pagination = url + "?page=" + str(i)
        raw_html = simple_get(url_with_pagination)
        soup = BeautifulSoup(raw_html, 'html.parser')
        complaints = soup.find_all("div", attrs={"class":"card-brand"})
        for complaint in complaints:
            brands_href = complaint.find("a", attrs={"class": "brand-logo"})["href"]
            brands_href_list.append(brands_href)
    return brands_href_list


# tüm markaların karnelerine gitsin
# markalar veri tabanına kayededilsin
def scrape_brands(brands_href_list = [], base_url = "http://www.sikayetvar.com"):
    for brands_href in brands_href_list:
        brand_report_link = base_url + brands_href + brands_href + "-marka-karnesi"
        print(brand_report_link)



BASE_URL = "http://www.sikayetvar.com"
brand_names = ["vena","w-collection","qnet-promosyon"] #The brand names are to be filled in

complaint_list = []

# complaint = Complaint("title", "description", "date", "view_count", "complainer")
# print(complaint.title)
# answer = Reply("date", "message", "score", "replier")
# complaint.set_reply(answer)
# print(complaint.reply.message)


brands_href_list = get_brands_href()
print(f"Found {len(brands_href_list)} brands.")
scrape_brands(brands_href_list, BASE_URL)
# for brand_href in brands_href_list:
#     print(brand_href)

brand_names = []  #bi dursun sonra silersin
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
        complaint_list.append(complaint)

 
    