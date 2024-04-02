import requests
import time
import re
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from entity import Brand, ComplainedItem, Complaint, Reply, Member

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
    time.sleep(10)
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
    url = BASE_URL + "/tum-markalar"
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

def print_brands(brands=[]):
    brand: Brand
    for brand in brands:
        print(f"href: {brand.href}\nname: {brand.name}\nrepiled complaint: {brand.replied_complaint}\ntotal complaint: {brand.total_complaint}\naverage reply sec: {brand.average_reply_sec}\nrating: {brand.rating}\nrating count: {brand.rating_count}\n")


# MAIN PROCESS

items = get_initial_complained_items()
brands = get_brands(items)
print_brands(brands)