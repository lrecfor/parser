from bs4 import BeautifulSoup
import requests


class Parser:

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/116.0.0.0"
                          "Safari/537.36"
        }
        self.time = None
        self.title = None
        self.new_text = None

    def parse_news(self):
        session = requests.Session()
        response = session.get(f"https://hornews.com/news/", headers=self.headers)

        bs = BeautifulSoup(response.text, "html.parser")

        news_block = bs.find('div', 'row')
        news_links = [a_tag.attrs.get("href") for a_tag in news_block.find_all('a') if a_tag.attrs.get("href")
                      and a_tag.attrs.get("href") != ""]
        dict_keys = {}.fromkeys(news_links)
        news_links = list(dict_keys.keys())

        for link in news_links:
            session_ = requests.Session()
            response_ = session_.get(f"https://hornews.com" + link, headers=self.headers)

            bs = BeautifulSoup(response_.text, "html.parser")

            self.time = bs.find('time', 'heading-block__time').text
            print(self.time)

            self.title = bs.find('h1', 'heading-block__title').text
            print(self.title)

            ds = bs.find('div', 'news-item__text user-text')
            self.new_text = [_.text for _ in ds.find_all('p')]
            ds = bs.find('div', 'news')
            self.new_text = "".join(self.new_text[:-len([_.text for _ in ds.find_all('p')])])

            print(self.new_text)

    def get_news(self):
        self.parse_news()


p = Parser()
p.get_news()
