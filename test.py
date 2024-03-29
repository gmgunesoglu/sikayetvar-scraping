# from complained_item import ComplainedItem

# def get_next_generation(item_list = []):
#     next_items = []
#     item: ComplainedItem
#     for item in item_list:
#         new_item = ComplainedItem(item.href + "/child", item.name + " child", item.rating, item.rating_count, item.href, item.brand)
#         new_item.is_leaf = True
#         next_items.append(new_item)
#         item.brand = item.name
#     return next_items

# def print_item(item: ComplainedItem):
#     print(f"href: {item.href}\nname: {item.name}\nrating: {item.rating}\nrating count: {item.rating_count}\nupper item: {item.upper_item}\nbrand: {item.brand}\nis leafe: {item.is_leaf}\n")


# item = ComplainedItem("/tes","test",5,222,None,"/test")

# item_list = []
# item_list.append(item)
# print_item(item_list[0])
# next_item_list = get_next_generation(item_list)
# print_item(item_list[0])
# print_item(next_item_list[0])

# import locale
# from datetime import datetime

# def string_to_date(date_string):
#     # Şuanki yıl bilgisini alın    
#     try:
#         if len(date_string.split()) == 2:
#             date = datetime.strptime(date_string, "%B %d %H:%M").date()
#         elif len(date_string.split()) == 3:
#             date_string = f"{datetime.now().year} {date_string}"
#             date = datetime.strptime(date_string, "%Y %d %B %H:%M").date()
#         elif len(date_string.split()) == 4:
#             date = datetime.strptime(date_string, "%d %B %Y %H:%M").date()
#         else:
#             print("[-] Date string has much parameters!")
#         return date
#     except ValueError:
#         print("[-] Unexpected date format!")
#         print(f"({date_string})")
#         print(len(date_string.split()))
#         return None


# # tarih 
# import locale
# from datetime import datetime, timedelta

# def string_to_date(date_string):
#     # Şuanki yıl bilgisini alın
#     parameters = len(date_string.split())
#     try:
#         if parameters == 2:
#             date = datetime.strptime(date_string, "%B %d %H:%M").date()
#         elif parameters == 3:
#             date_string = f"{datetime.now().year} {date_string}"
#             date = datetime.strptime(date_string, "%Y %d %B %H:%M").date()
#         elif parameters == 4:
#             date = datetime.strptime(date_string, "%d %B %Y %H:%M").date()
#         else:
#             print("[-] Date string has much parameters!")
#         return date
#     except ValueError:
#         print("[-] Unexpected date format!")
#         print(f"({date_string})")
#         print(parameters)
#         print(date_string.split())
#         return None

# def convert_to_datetime(time_str):
#     if "saniye" in time_str:
#         seconds = int(time_str.split()[0])
#         return datetime.now() - timedelta(seconds=seconds)
    
#     elif "dakika" in time_str:
#         minutes = int(time_str.split()[0])
#         return datetime.now() - timedelta(minutes=minutes)
    
#     elif "saat" in time_str:
#         hours = int(time_str.split()[0])
#         return datetime.now() - timedelta(hours=hours)
    
#     elif "gün" in time_str:
#         days = int(time_str.split()[0])
#         return datetime.now() - timedelta(days=days)
    
#     elif "hafta" in time_str:
#         weeks = int(time_str.split()[0])
#         return datetime.now() - timedelta(weeks=weeks)
    
#     else:
#         try:
#             # Eğer saniye, dakika, saat, gün veya hafta içermiyorsa
#             # ve '%d %B %H:%M' formatına uyuyorsa bu formata göre çevir

#             return string_to_date(time_str)
#         except ValueError:
#             print("Geçersiz tarih formatı:", time_str)
#             return None

# # string i date e çevirmek için
# locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')

# # Örnek stringler
# strings = [
#     "1 hafta önce",
#     "3 gün önce",
#     elif "hafta" in time_str:
#         weeks = int(time_str.split()[0])
#         return datetime.now() - timedelta(weeks=weeks)
    
#     else:
#         try:
#             # Eğer saniye, dakika, saat, gün veya hafta içermiyorsa
#             # ve '%d %B %H:%M' formatına uyuyorsa bu formata göre çevir

#             return string_to_date(time_str)
#         except ValueError:
#             print("Geçersiz tarih formatı:", time_str)
#             return None

# # string i date e çevirmek için
# locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')

# # Örnek stringler
# strings = [
#     "1 hafta önce",
#     "3 gün önce",
#     "32 dakika önce",
#     "20 saniye önce",
#     "29 Ocak 01:02",
#     "28 Ocak 22:43",
#     "21 Aralık 2023 20:57"
# ]

# # # Her bir string için dönüşümü gerçekleştir
# # for string in strings:
# #     print(convert_to_datetime(string))


# strings2 = [
#     "29 Ocak 01:02",
#     "28 Aralık 22:43",
#     "21 Aralık 2023 20:57"
# ]
# for string in strings2:
#     print(string_to_date(string))
#     "32 dakika önce",
#     "20 saniye önce",
#     "29 Ocak 01:02",
#     "28 Ocak 22:43",
#     "21 Aralık 2023 20:57"
# ]

# # Her bir string için dönüşümü gerçekleştir
# for string in strings:
#     print(convert_to_datetime(string))


# strings2 = [
#     "29 Ocak 01:02",
#     "28 Aralık 22:43",
#     "21 Aralık 2023 20:57"
# ]
# for string in strings2:
#     print(string_to_date(string))
# # tarih 
# import locale
# from datetime import datetime, timedelta

# def string_to_date(date_string):
#     # Şuanki yıl bilgisini alın
#     parameters = len(date_string.split())
#     try:
#         if parameters == 2:
#             date = datetime.strptime(date_string, "%B %d %H:%M").date()
#         elif parameters == 3:
#             date_string = f"{datetime.now().year} {date_string}"
#             date = datetime.strptime(date_string, "%Y %d %B %H:%M").date()
#         elif parameters == 4:
#             date = datetime.strptime(date_string, "%d %B %Y %H:%M").date()
#         else:
#             print("[-] Date string has much parameters!")
#         return date
#     except ValueError:
#         print("[-] Unexpected date format!")
#         print(f"({date_string})")
#         print(parameters)
#         print(date_string.split())
#         return None

# def convert_to_datetime(time_str):
#     if "saniye" in time_str:
#         seconds = int(time_str.split()[0])
#         return datetime.now() - timedelta(seconds=seconds)
    
#     elif "dakika" in time_str:
#         minutes = int(time_str.split()[0])
#         return datetime.now() - timedelta(minutes=minutes)
    
#     elif "saat" in time_str:
#         hours = int(time_str.split()[0])
#         return datetime.now() - timedelta(hours=hours)
    
#     elif "gün" in time_str:
#         days = int(time_str.split()[0])
#         return datetime.now() - timedelta(days=days)
    
#     elif "hafta" in time_str:
#         weeks = int(time_str.split()[0])
#         return datetime.now() - timedelta(weeks=weeks)
    
#     else:
#         try:
#             # Eğer saniye, dakika, saat, gün veya hafta içermiyorsa
#             # ve '%d %B %H:%M' formatına uyuyorsa bu formata göre çevir

#             return string_to_date(time_str)
#         except ValueError:
#             print("Geçersiz tarih formatı:", time_str)
#             return None

# # string i date e çevirmek için
# locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')

# # Örnek stringler
# strings = [
#     "1 hafta önce",
#     "3 gün önce",
#     elif "hafta" in time_str:
#         weeks = int(time_str.split()[0])
#         return datetime.now() - timedelta(weeks=weeks)
    
#     else:
#         try:
#             # Eğer saniye, dakika, saat, gün veya hafta içermiyorsa
#             # ve '%d %B %H:%M' formatına uyuyorsa bu formata göre çevir

#             return string_to_date(time_str)
#         except ValueError:
#             print("Geçersiz tarih formatı:", time_str)
#             return None

# # string i date e çevirmek için
# locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')

# # Örnek stringler
# strings = [
#     "1 hafta önce",
#     "3 gün önce",
#     "32 dakika önce",
#     "20 saniye önce",
#     "29 Ocak 01:02",
#     "28 Ocak 22:43",
#     "21 Aralık 2023 20:57"
# ]

# # # Her bir string için dönüşümü gerçekleştir
# # for string in strings:
# #     print(convert_to_datetime(string))


# strings2 = [
#     "29 Ocak 01:02",
#     "28 Aralık 22:43",
#     "21 Aralık 2023 20:57"
# ]
# for string in strings2:
#     print(string_to_date(string))
    

# # sql  psycopg2
# import psycopg2
# import brand_dao
# import brand

# # Veritabanına bağlan
# conn = psycopg2.connect(
#     dbname="sikayetvar", 
#     user="postgres", 
#     password="postgres", 
#     host="localhost",
#     port="5432"
# )

# # Bağlantı üzerinden bir cursor oluştur
# cur = conn.cursor()
# print("hmm")


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from brand import Brand

def create_brand(href, name, replied_complaint, total_complaint, average_reply_sec, rating_count, rating):
    """
    Yeni bir marka oluşturur ve veritabanına ekler.
    """
    new_brand = Brand(href=href, name=name, replied_complaint=replied_complaint, total_complaint=total_complaint,
                      average_reply_sec=average_reply_sec, rating_count=rating_count, rating=rating)
    session.add(new_brand)
    session.commit()

def get_brand_by_id(brand_id):
    """
    Belirli bir markanın bilgilerini brand_id'ye göre getirir.
    """
    return session.query(Brand).filter_by(id=brand_id).first()

def update_brand(brand_id, href=None, name=None, replied_complaint=None, total_complaint=None,
                 average_reply_sec=None, rating_count=None, rating=None):
    """
    Belirli bir markanın bilgilerini günceller.
    """
    brand = session.query(Brand).filter_by(id=brand_id).first()
    if href:
        brand.href = href
    if name:
        brand.name = name
    if replied_complaint:
        brand.replied_complaint = replied_complaint
    if total_complaint:
        brand.total_complaint = total_complaintsqlalchemy.orm
    if average_reply_sec:
        brand.average_reply_sec = average_reply_sec
    if rating_count:
        brand.rating_count = rating_count
    if rating:
        brand.rating = rating
    session.commit()

def delete_brand(brand_id):
    """
    Belirli bir markayı veritabanından siler.
    """
    brand = session.query(Brand).filter_by(id=brand_id).first()
    session.delete(brand)
    session.commit()

# Veritabanı bağlantısını oluştur
engine = create_engine('postgresql://postgres:postgres@localhost:5432/sikayetvar')
Session = sessionmaker(bind=engine)
session = Session()

create_brand("/migros", "Migros", 5000, 5200, 300, 600, 60)
