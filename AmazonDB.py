# import os
# import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
Base = declarative_base()
class AmazonProduct(Base):
    __tablename__='amazon-product'
    #  Title,ID,Price,Aval,URL,Date
    id = Column(Integer, primary_key=True)
    product_id = Column(String(250),nullable=False)
    title = Column(String(250), nullable=False)
    price = Column(Float)
    availability = Column(String(250))
    link = Column(String(250))
    date = Column(Date)

    def create_table(self):
        engine = create_engine('sqlite:///amazon_items.db')
        Base.metadata.create_all(engine)

class ProductData:
    engine = create_engine('sqlite:///amazon_items.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    def insert_data(self,Title,ID,Price,Aval,url_link,Date):
        new_item = AmazonProduct(title=Title,product_id=ID,price=Price,availability=Aval,link=url_link,date=Date)
        self.session.add(new_item)
        self.session.commit()

    def view_all(self):
        return self.session.query(AmazonProduct).all()

