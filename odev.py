import requests
import json
from datetime import datetime, timedelta

API_KEY = "4e944ae2ca6e416b93cb8fcb6ea4f795"
BASE_URL = "https://newsapi.org/v2/everything"
DATA_FILE = "news_data.json"

def fetch_news(query="technology", date_range="weekly"):
    """ Belirtilen sorgu ve tarih aralığına göre haberleri getirir. """
    date_from, date_to = get_date_range(date_range)
    params = {
        "q": query,
        "from": date_from,
        "to": date_to,
        "sortBy": "publishedAt",
        "apiKey": API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        
        if not articles:
            print("Uygun haber bulunamadı.")
            return []
        
        return articles
    except requests.exceptions.RequestException as e:
        print("Hata oluştu:", e)
        return []

def get_date_range(range_type):
    """ Seçilen zaman aralığına göre başlangıç ve bitiş tarihlerini belirler. """
    today = datetime.today()
    if range_type == "daily":
        start_date = today - timedelta(days=1)
    elif range_type == "weekly":
        start_date = today - timedelta(weeks=1)
    elif range_type == "monthly":
        start_date = today - timedelta(days=30)
    else:
        start_date = today - timedelta(weeks=1)  # Varsayılan haftalık
    
    return start_date.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")

def save_news(news_list):
    """ Haberleri JSON dosyasına kaydeder. """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(news_list, f, ensure_ascii=False, indent=4)

def load_news():
    """ JSON dosyasından haberleri yükler. """
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def add_news(new_article):
    """ Yeni bir haber ekler. """
    news_list = load_news()
    news_list.append(new_article)
    save_news(news_list)
    print("Yeni haber eklendi!")

def update_news(index, updated_article):
    """ Belirtilen indeksteki haberi günceller. """
    news_list = load_news()
    if 0 <= index < len(news_list):
        news_list[index] = updated_article
        save_news(news_list)
        print("Haber güncellendi!")
    else:
        print("Geçersiz indeks!")

def delete_news(index):
    """ Belirtilen indeksteki haberi siler. """
    news_list = load_news()
    if 0 <= index < len(news_list):
        del news_list[index]
        save_news(news_list)
        print("Haber silindi!")
    else:
        print("Geçersiz indeks!")

def main():
    query = input("Hangi konudaki haberleri görmek istersin? (örn: technology, sports): ")
    date_range = input("Zaman aralığı seç (daily, weekly, monthly): ")
    news_list = fetch_news(query, date_range)
    
    if news_list:
        save_news(news_list)
        print("\n📢 En Son Haberler:")
        for i, news in enumerate(news_list[:5], start=1):
            print(f"{i}. {news['title']}")
    
    while True:
        print("\n[1] Haber Ekle [2] Haber Güncelle [3] Haber Sil [4] Çıkış")
        choice = input("Ne yapmak istiyorsun?: ")
        if choice == "1":
            title = input("Haber başlığı: ")
            content = input("Haber içeriği: ")
            add_news({"title": title, "content": content})
        elif choice == "2":
            index = int(input("Güncellenecek haberin indeksini gir: "))
            title = input("Yeni başlık: ")
            content = input("Yeni içerik: ")
            update_news(index, {"title": title, "content": content})
        elif choice == "3":
            index = int(input("Silinecek haberin indeksini gir: "))
            delete_news(index)
        elif choice == "4":
            break
        else:
            print("Geçersiz seçenek!")

if _name_ == "_main_":
    main()
