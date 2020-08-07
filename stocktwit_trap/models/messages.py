from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import relationship
from stocktwit_trap.database import Base
from stocktwit_trap.models.messages_symbols import messages_symbols_xref

class Messages(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    stocktwit_id = Column(Integer, unique=True, nullable=False)
    body = Column(String, nullable=False)
    sentiment = Column(String,  nullable=True)
    twitted_on = Column(Date, nullable=False)

    symbols = relationship(
        "Symbols",
        secondary=messages_symbols_xref,
        backref="messages"
    )

    def __init__(self, stocktwit_id=None, body=None, sentiment=None, twitted_on=None):
        self.stocktwit_id = stocktwit_id
        self.body = body
        self.sentiment = sentiment
        self.twitted_on = twitted_on
