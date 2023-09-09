from bs4 import BeautifulSoup
import requests
import schedule
import datetime
from database import New, Database


class Parser:

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/116.0.0.0"
                          "Safari/537.36"
        }
        self.news = []

    def parse_news(self):
        session = requests.Session()
        response = session.get(f"https://hornews.com/news/", headers=self.headers)

        bs = BeautifulSoup(response.text, "html.parser")

        news_block = bs.find('main', 'col-md-9 js-height-donor')
        news_links = [a_tag.attrs.get("href") for a_tag in news_block.find_all('a') if a_tag.attrs.get("href")
                      and a_tag.attrs.get("href") != ""]
        dict_keys = {}.fromkeys(news_links)
        news_links = list(dict_keys.keys())

        for link in news_links:
            session_ = requests.Session()
            response_ = session_.get(f"https://hornews.com" + link, headers=self.headers)

            bs = BeautifulSoup(response_.text, "html.parser")

            new_time = bs.find('time', 'heading-block__time').text

            new_title = bs.find('h1', 'heading-block__title').text

            ds = bs.find('div', 'news-item__text user-text')
            new_text = [_.text for _ in ds.find_all('p')]
            ds = bs.find('div', 'news')
            new_text = "".join(new_text[:-len([_.text for _ in ds.find_all('p')])])

            self.news.append(New(time=new_time,
                                 title=new_title,
                                 text=new_text))

    def add_to_database(self):
        d = Database()
        d.add(news_list=self.news)

    def update_database(self):
        print("update_database(): ", datetime.datetime.now())
        self.parse_news()
        self.add_to_database()


if __name__ == "__main__":
    p = Parser()
    schedule.every().hour.do(p.update_database)
    while True:
        schedule.run_pending()
