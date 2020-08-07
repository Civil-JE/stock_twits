import requests
import json

from stocktwit_trap import config


class AlphaVantageApiService:

    def get_stock_data_for_symbol(self, symbol):
        params = [
            ('outputsize', 'compact'),
            ('datatype', 'json')
        ]
        url = self._build_url(symbol, 'TIME_SERIES_DAILY', )
        result = requests.get(url)

        return result

    def _build_url(self, symbol, function, additional_params=None):
        base_url = config.ALPHA_VANTAGE_BASE_URL
        api_key = config.ALPHA_VANTAGE_KEY
        additional_params = self._build_param_strings(additional_params)

        return f'{base_url}{function}&symbol={symbol}{additional_params}&apikey={api_key}'

    def _build_param_strings(self, params):
        param_string = ''
        if params:
            for param in params:
                param_string += f'&{param[0]}={param[1]}'

        return param_string

    def write_results_to_file(self, results):
        with open('test_stock.json', 'w') as file:
            file.write(json.dumps(results))
            file.close()
