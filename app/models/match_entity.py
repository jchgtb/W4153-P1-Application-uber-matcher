from sqlalchemy import Column, Integer, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Match(Base):
    __tablename__ = "matches"

    match_id = Column(Integer, primary_key=True, autoincrement=True)
    user1_id = Column(Integer, nullable=False)
    user2_id = Column(Integer, nullable=False)
    user1_status = Column(Enum('PENDING', 'ACCEPTED', 'REJECTED', name='status_enum'), default='PENDING', nullable=False)
    user2_status = Column(Enum('PENDING', 'ACCEPTED', 'REJECTED', name='status_enum'), default='PENDING', nullable=False)

