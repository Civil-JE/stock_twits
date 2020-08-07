from datetime import datetime
from sqlalchemy import exists

from stocktwit_trap.models import Symbols, Messages
from stocktwit_trap.database import db_session


class DatabaseService:

    def commit(self):
        db_session.commit()


    def add_new_symbols(self, symbols):
        new_symbols = []
        for symbol in symbols:
            if not self._symbol_exists(symbol['id']):
                new_symbols.append(Symbols(
                    stocktwit_id=symbol['id'],
                    symbol=symbol['name']
                ))

        db_session.add_all(new_symbols)
        db_session.commit()


    def add_new_messages(self, messages):
        new_messages = []
        for message in messages:
            if not self._message_exists(message['stocktwit_id']):
                new_message = Messages(
                    stocktwit_id=message['stocktwit_id'],
                    body=message['body'],
                    sentiment=message['sentiment'],
                    twitted_on=self._format_timestamp(message['created_at'])
                )
                new_messages.append(self._add_symbols_to_message(message['symbols'], new_message))

        db_session.add_all(new_messages)
        db_session.commit()


    def get_message_count(self):
        return len(Messages.query.all())


    def get_symbol_count(self):
        return len(Symbols.query.all())


    def get_list_of_all_messages(self):
        return [message.body for message in Messages.query.all()]


    def get_list_of_all_symbols(self):
        return [symbol.symbol for symbol in Symbols.query.all()]


    def get_list_of_all_symbols_filter_active(self, active=True):
        return [symbol.symbol for symbol in Symbols.query.filter_by(active=active)]


    def get_symbols_by_symbol(self, symbol):
        symbol_query = Symbols.query.filter_by(symbol=symbol)
        if symbol_query.count() == 1:
            return symbol_query.one()
        else:
            raise Exception


    def _add_symbols_to_message(self, symbols, message):
        for symbol in symbols:
            msg_symbol = db_session.query(Symbols).filter_by(stocktwit_id=symbol['id']).one()
            message.symbols.append(msg_symbol)

        return message


    def _message_exists(self, message_id):
        return db_session.query(exists().where(Messages.stocktwit_id==message_id)).scalar()


    def _symbol_exists(self, symbol_id):
        return db_session.query(exists().where(Symbols.stocktwit_id==symbol_id)).scalar()


    def _format_timestamp(self, timestamp):
        return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%Sz")
