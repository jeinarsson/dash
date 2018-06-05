from sqlalchemy.engine import reflection
from sqlalchemy import create_engine
from sqlalchemy.schema import (
    MetaData,
    Table,
    DropTable,
    ForeignKeyConstraint,
    DropConstraint,
    )
import project.db as db
import os
from datetime import datetime

from project.db.models import *

def drop_everything(engine):

    conn = engine.connect()

    # the transaction only applies if the DB supports
    # transactional DDL, i.e. Postgresql, MS SQL Server
    trans = conn.begin()

    inspector = reflection.Inspector.from_engine(engine)

    # gather all data first before dropping anything.
    # some DBs lock after things have been dropped in 
    # a transaction.

    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(
                ForeignKeyConstraint((),(),name=fk['name'])
                )
        t = Table(table_name,metadata,*fks)
        tbs.append(t)
        all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))

    trans.commit()   

def create_from_empty(database_url = None):
    import project.db.models

    if database_url is None:
        database_url = os.environ['DATABASE_URL']
    
    

    engine = create_engine(database_url)

    # create schema
    print('Initializing DB in\n{}'.format(database_url))
    #db.Base.metadata.drop_all(bind=engine)
    drop_everything(engine)
    db.Base.metadata.create_all(bind=engine, checkfirst=True)
    
    print('Adding some initial data.')
    # add any initial data
    s = db.make_session(database_url)

    e = EventsCache()
    e.timestamp = datetime.min
    e.data = None
    s.add(e)
    
    s.commit()


    print('Done.')


if __name__ == '__main__':
    create_from_empty()
    