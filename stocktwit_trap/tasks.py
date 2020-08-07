from time import sleep
from stocktwit_trap.services import StockTwitApiService, DatabaseService

def background_task(n):

    """ Function that returns len(n) and simulates a delay """

    delay = 2

    print("Task running")
    print(f"Simulating a {delay} second delay")

    sleep(delay)

    print(len(n))
    print("Task complete")

    return len(n)


def get_twit_messages(symbols):
    st_service = StockTwitApiService()
    db_service = DatabaseService()
    for symbol in symbols:
        print('Getting twits for ' + symbol)
        messages, incoming_symbols = st_service.get_messages_for_symbol(symbol)

        db_service.add_new_symbols(incoming_symbols)
        db_service.add_new_messages(messages)
