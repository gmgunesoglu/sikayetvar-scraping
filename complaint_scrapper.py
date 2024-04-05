import locale
import requests
import time
from datetime import datetime, timedelta
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from entity import Complaint, Reply, Member, ComplainedItem
from dao import MemberDao, ReplyDao, ComplaintDao, ComplainedItemDao, save_error

# GLOBAL VERIABLES

# user agent
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'
}

BASE_URL = "http://www.sikayetvar.com"

DELAY = 1

# FUNCTIONS

def second_get(url: str, delay: int, count: int):
    time.sleep(delay)
    print(f"SECOND GET: {url}")
    try:
        with closing(requests.get(url, headers=HEADERS, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                print(f"None url: {url}")   
                save_error(RuntimeError("Bad response for GET: " + url))
                if count == 1:
                    return None
                return second_get(url, delay*1.5, count-1)
    except RequestException as e:
        save_error(RuntimeError('Error during requests to {0} : {1}'.format(url, str(e))))
        return None

def simple_get(url: str):
    time.sleep(DELAY)
    print(f"GET: {url}")
    try:
        with closing(requests.get(url, headers=HEADERS, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                print(f"None url: {url}")   
                save_error(RuntimeError("Bad response for GET: " + url))
                return second_get(url, DELAY*1.5, 2)
    except RequestException as e:
        save_error(err = RuntimeError('Error during requests to {0} : {1}'.format(url, str(e))))
        return None

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)
   
def print_complaints(complaints=[]):
    complaint: Reply
    for complaint in complaints:
        print(f"href: {complaint.href}\ncomplained item: {complaint.complained_item}\ntitle: {complaint.title}\ndate: {complaint.date}\nview count: {complaint.view_count}\ncomplain owner: {complaint.complain_owner}\nrating: {complaint.rating}\nsolved: {complaint.sovled}")
        print("replies:")
        reply: Reply
        for reply in complaint.replies:
            print(f"href: {reply.href}\nmessage: {reply.message}\ndate: {reply.date}\nis from brand: {reply.is_from_brand}")
        print()

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
        if not raw_html:
            continue
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
        for i in range (1, last_page_number+1):
            url_with_pagination = url + "?page=" + str(i)
            raw_html = simple_get(url_with_pagination)
            if not raw_html:
                continue
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
            if not raw_html:
                continue
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

def print_complained_items(complained_items=[]):
    item: ComplainedItem
    for item in complained_items:
        print(f"id: {item.id}\nhref: {item.href}\nname: {item.name}\nrating: {item.rating}\nrating count: {item.rating_count}\nupper item id: {item.upper_item_id}\nbrand id: {item.brand_id}\nis leafe: {item.is_leaf}\n")


# MAIN PROCESS

# required for convert string to datetime
locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')

# 5- tüm complained_items lar dan
# sayfalar gezilip şikayetler, üye ve cevaplarla birlikle oluşturulup
# veri tabanına kaydediliyor
# items = ComplainedItemDao.get_all()
# scrape_complaints(items)



start_id = 1
end_id = 1
period = 10
complained_item_count = ComplainedItemDao.get_count()
while complained_item_count >= start_id:
    end_id += period
    if end_id > complained_item_count:
        end_id = complained_item_count + 1
    start_date = datetime.now()
    items = ComplainedItemDao.get_all_in_id_range(start_id, end_id)
    # print(f"start id: {start_id}\tend_id: {end_id}\n")
    # print_complained_items(items)
    scrape_complaints(items)
    end_date = datetime.now()
    start_id = end_id
    complained_item_count = ComplainedItemDao.get_count()
    print(f"START DATE: {start_date} END DATE: {end_date}")
    print(f"START_ID: {start_id} END_ID: {end_id}")
