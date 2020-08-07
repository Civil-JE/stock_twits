import requests
import json

from stocktwit_trap import config


class StockTwitApiService:

    def get_access_token(self):
         response = requests.post(f'{config.BASE_STOCKTWIT_URL}streams/all.json', data={
         'client_id': config.CONSUMER_KEY,
         'response_type': 'code',
         'scope': 'read',
         'prompt': 0
         })
         return response

    def get_stock_twits_from_symbol(self, symbol):
        response = requests.get(f'{config.BASE_STOCKTWIT_URL}streams/symbol/{symbol}.json')

        return response

    def get_messages_symbols_from_response(self, response):
        raw_messages = response.json()['messages']
        messages = []
        all_symbols = []
        for message in raw_messages:
            # Get all unique symbols in the messages
            msg_symbols = [{'id': symbol['id'], 'name': symbol['symbol']} for symbol in message['symbols']]
            for symbol in msg_symbols:
                if symbol not in all_symbols: all_symbols.append(symbol)
            # Get all messages and format them for our use
            messages.append({
                'symbols': [{'id': symbol['id'], 'name': symbol['symbol']} for symbol in message['symbols']],
                'stocktwit_id': message['id'],
                'body': message['body'],
                'created_at': message['created_at'],
                'sentiment': message['entities']['sentiment']['basic'] if message['entities']['sentiment'] else None
            })

        return messages, all_symbols

    def get_messages_for_symbol(self, symbol):
        stock_twits = self.get_stock_twits_from_symbol(symbol)

        return self.get_messages_symbols_from_response(stock_twits)

    def write_results(self, results):
        with open('test_twit.json', 'w') as file:
            file.write(json.dumps(results))
            file.close()
