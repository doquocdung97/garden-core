import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import validates
import urllib
from middleware.settings import DEBUG
from sqlalchemy.sql.expression import null, true
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()
def get_declarative_base():
	return BASE

Session = None
engine  = None
def create_db_engine(db_conn_string = None, debug_mode=False):
	global engine
	if not engine:
		engine = create_engine("sqlite:///data.db",
																echo=debug_mode,
																pool_size=100,
																max_overflow=100,
																pool_recycle=1,
																pool_pre_ping=True,
																pool_use_lifo=True
																)
	return engine

def my_before_commit(session):
    print("before commit!")

def create_db_session(engine):
	global Session
	if not Session:
		Session = sessionmaker(bind=engine,expire_on_commit=False)
	return Session()


def commit_db_session(data,callback = None, error = None):
	engine = create_db_engine()
	session = create_db_session(engine)
	try:
		session.add(data)
		session.commit()
		if callback:
			callback(data)
		return data
	except Exception as ex:
		if error:
			error(ex)
	finally:
		session.close()