from sqlalchemy import Table, Column, Integer, ForeignKey
from stocktwit_trap.database import Base


messages_symbols_xref = Table('messages_symbols_xref', Base.metadata,
                            Column('message_id', Integer, ForeignKey('messages.id')),
                            Column('symbol_id', Integer, ForeignKey('symbols.id'))
                        )
