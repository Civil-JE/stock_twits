from sqlalchemy import Column, Integer, String, Boolean
from stocktwit_trap.database import Base


class Symbols(Base):
    __tablename__ = 'symbols'

    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True, nullable=False)
    stocktwit_id = Column(Integer, unique=True, nullable=False)
    active = Column(Boolean,  nullable=False)


    def __init__(self, stocktwit_id=None, symbol=None, active=0):
        self.stocktwit_id = stocktwit_id
        self.symbol = symbol
        self.active = active
