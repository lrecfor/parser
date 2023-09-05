from bs4 import BeautifulSoup
import requests


class Parser:

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 "
                          "Safari/537.36"
        }
        self.time = None
        self.title = None
        self.new_text = None

    def parse_news(self):
        session = requests.Session()
        response = session.get(f"https://hornews.com/news/", headers=self.headers)

        bs = BeautifulSoup(response.text, "html.parser")
        self.time = bs.find_all('span', 'news__category')
        # for _ in self.time:
        #     print(_.text)

        self.title = bs.find_all('p', 'news__title')
        # for _ in self.title:
        #     print(_.text)

        news_links = []
        for a_tag in bs.find_all('a'):
            href = a_tag.attrs.get("href")
            if href == "" or href is None or href[:6] != "/news/" or len(href) == 6:
                continue
            news_links.append(href)

        for link in news_links:
            session_ = requests.Session()
            response_ = session_.get(f"https://hornews.com" + link, headers=self.headers)

            bs = BeautifulSoup(response_.text, "html.parser")

            ds = bs.find('div', 'news-item__text user-text')
            result = []
            for p_ in ds.find_all('p'):
                result.append(p_.text)
            ds = bs.find('div', 'news')
            result_ = []
            for p_ in ds.find_all('p'):
                result_.append(p_.text)
            print("".join(result[:-len(result_)]))

    def get_news(self):
        self.parse_news()


p = Parser()
p.get_news()
