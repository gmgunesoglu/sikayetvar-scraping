# sikayetvar-scraping 

Proje sikayetvar.com daki markalar/modeller/ürünlerhakkında bilgi toplar ve bu bilgileri güncel tutar. Bunlara ek olarak marka/model/ürün hakkında yapılan şikayetlerle ilgili bilgi toplar.


## Teknolojiler
  - Python (v3.10.12)
    - requests
    - bs4 (BeautifulSoup)
    - psycopg2
    - sqlalchemy
  - Postgresql (v14.11)
  - VS Code


## Kurulum
Proje için bir klasör oluşturup projeyi o klasöre kurun:
> mkdir proje_klasoru

> cd proje_klasoru

> git clone https://github.com/gmgunesoglu/sikayetvar-scraping


## Veri Tabanı Yapılandırması
Projeyi vs code da açın:
> code sikayetvar-scraping/

"dao.py" dosyasında create_engine fonksiyonunun parametresini kendi veri tabanınıza göre ayarlarlayın.
![image](https://github.com/gmgunesoglu/sikayetvar-scraping/assets/76867018/b100b45c-4f19-4855-9725-27c25d201f2a)

Terminale dönüp postgresql de bir veri tabanı oluşturun:
> psql -U <kullanıcı_adı>

> <kullanıcı_şifresi>

> CREATE DATABASE <veri_tabanı_adı>  

> \q

Tabloları oluşturacak script i çalıştırın (terminalin konumu proje klasöründe olmalı):
> PGPASSWORD=<kullanıcı_şifresi> psql -U <kullanıcı_adı> -d <veri_tabanı_adı>   -a -f sikayetvar-scraping/create_tables.sql


## Projeyi Çalıştırma
terminalin konumu proje klasörünüzdeyken ilk önce brand_and_item_scrapper.py dosyasını çalıştırın:
> ./sikayetvar-scraping/myenv/bin/python ./sikayetvar-scraping/brand_and_item_scrapper.py

Bu işlem brand ve complained_item tablolarınıza satırlar ekleyecek ve güncel tutacaktır. Delay 10 saniye olarak ayarlanmıştır,
"brand_and_item_scrapper.py" dosyasında DELAY değişkenini duruma göre değiştirilebilir.
complained_item tablosuna bir satır eklendikten sonra (yaklaşık 10 dakikasonra) complaint_scrapper.py dosyasını çalıştırabilirsiniz. Terminal proje klasöründeyken:
> ./sikayetvar-scraping/myenv/bin/python ./sikayetvar-scraping/complaint_scrapper.py

Bu işlem complaint, member ve reply tablolarına satırlar ekleyecektir.

## Varlık İlişyi Diyagramı
![image](https://github.com/gmgunesoglu/sikayetvar-scraping/assets/76867018/68c6b1fd-d1d3-4599-8d08-f7b2b7ac1708)
