from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base


base = declarative_base()


class New(base):
    __tablename__ = "news"
    id = Column(Integer(), primary_key=True)
    time = Column(String(), nullable=False)
    title = Column(String(), nullable=False)
    text = Column(String(), nullable=False)


class Database:
    def __init__(self):
        self.url = f"postgresql://postgres:1@localhost:5432/news_database"
        self.engine = create_engine(self.url, echo=True)

    def create(self):
        if not database_exists(self.url):
            create_database(self.url)

        metadata = MetaData()
        news_table = Table('news', metadata,
                           Column('id', Integer(), primary_key=True),
                           Column('time', String(), nullable=False),
                           Column('title', String(), nullable=False),
                           Column('text', String(), nullable=False)
                           )
        metadata.create_all(self.engine)

    def add(self, news_list):
        self.create()
        Session = sessionmaker(bind=self.engine)
        session = Session()
        for new in news_list:
            session.add(new)
        session.commit()
