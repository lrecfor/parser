from parser import Parser
from database import Database

p = Parser()
d = Database()


def update_database():
    fresh_news = p.parse_news()
    d.add(news_list=fresh_news)
