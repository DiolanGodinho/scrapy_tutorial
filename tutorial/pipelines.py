# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

import psycopg2
from .db_config import config

class TutorialPipeline:
    def __init__(self) -> None:
        self.curr = None

    def open_spider(self, spider):
        self.connect()
        self.create_table()

    def connect(self):
        try:
            params = config()

            self.conn = psycopg2.connect(**params)

            self.curr = self.conn.cursor()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_table(self):
        self.curr.execute('DROP TABLE IF EXISTS tb_quotes;')

        self.curr.execute('''
            CREATE TABLE tb_quotes(id SERIAL PRIMARY KEY, 
                                   quote_text TEXT, 
                                   author VARCHAR(50), 
                                   tags VARCHAR(100));''')

    def process_item(self, item, spider):
        self.store_data(item)
        return item

    def store_data(self, item):
        tags = '/'.join(item['tags'])

        self.curr.execute('''
            INSERT INTO tb_quotes(quote_text, author, tags) 
            VALUES (%s, %s, %s) 
            RETURNING id;''', 
            (item['quote_text'], item['author'], tags))
        
        id = self.curr.fetchone()[0]

        self.conn.commit()

        return id

    def close_spider(self, spider):
        self.curr.close()
        self.conn.close()
