from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def make_www_session(app):

    engine = create_engine(app.config['DATABASE_URL'])
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    Base.query = db_session.query_property()

    return db_session

def make_session(database_url = None):

    if database_url is None:
        from os import environ
        database_url = environ['DATABASE_URL']
    
    engine = create_engine(database_url)
    sm = sessionmaker(bind=engine)
    return sm()


