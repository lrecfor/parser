from bs4 import BeautifulSoup
import requests
from threading import Timer
import time
import datetime

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class New(Base):
    __tablename__ = 'new'
    id = Column(Integer(), primary_key=True)
    time = Column(String(100), nullable=False)
    title = Column(String(100), nullable=False)
    text = Column(String(100), nullable=False)


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

            self.news.append([new_time, new_title, new_text])

    def add_to_database(self):
        url = f"postgresql://postgres:1@localhost:5432/news_database"
        if not database_exists(url):
            create_database(url)
        metadata = MetaData()
        engine = create_engine(url, echo=True)
        new = Table('new', metadata,
                    Column('id', Integer(), primary_key=True),
                    Column('time', String(100), nullable=False),
                    Column('title', String(100), nullable=False),
                    Column('text', String(100), nullable=False)
                    )
        metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        n1 = New(
            time='05:24',
            title='inili mashinu',
            text='karl u klary ukral koraly klara ukrala u karla klarnet',
        )
        session.add(n1)
        session.commit()

    def get_news(self):
        # print("news", datetime.datetime.now())
        self.parse_news()
        # Timer(10.0, self.get_news).start()


p = Parser()
# p.get_news()
p.add_to_database()
