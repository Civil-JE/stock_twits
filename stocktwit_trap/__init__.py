import os
from datetime import datetime, timedelta

from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from flask import Flask, request

from stocktwit_trap import config, tasks, database
from stocktwit_trap.services import StockTwitApiService, SchedulerService, DatabaseService, AlphaVantageApiService


def create_app(test_config=None):
    # Setup the Flask App
    app=Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'stock_twit_trap.sqlite')
    )
    # Setup the queue and scheduler
    redis_connection = Redis(host='localhost', port=6379)
    queue = Queue(connection=redis_connection)
    scheduler = Scheduler(connection=redis_connection)

    # Initialize_db & db_service
    database.init_db()
    db_service = DatabaseService()

    scheduler_service = SchedulerService(scheduler)
    scheduler_service.delete_queue(queue)
    # scheduler_service.schedule_twit_rip(db_service.get_list_of_all_symbols_filter_active())

    alpha_service = AlphaVantageApiService()
    results = alpha_service.get_stock_data_for_symbol('AAPL')
    alpha_service.write_results_to_file(results.json())

    @app.route('/counts/')
    def db_count():
        messages = db_service.get_message_count()
        symbols = db_service.get_symbol_count()
        return f"Messages: {messages} ||  Symbols: {symbols}"


    @app.route('/messages/')
    def message_list():
        messages = db_service.get_list_of_all_messages()
        return f"{messages}"


    @app.route('/symbols/')
    def symbol_list():
        symbols = db_service.get_list_of_all_symbols()
        return f"{symbols}"


    @app.route('/symbols/info/<symbol>/')
    def symbol_info(symbol):
        symbol = db_service.get_symbols_by_symbol(symbol)
        return f"Symbol: {symbol.symbol}, Active: {symbol.active}, ID: {symbol.stocktwit_id}"


    @app.route('/symbols/set_active/<symbol>/')
    def symbol_set_active(symbol):
        symbol = db_service.get_symbols_by_symbol(symbol)
        symbol.active = 1
        db_service.commit()
        return f"{symbol.symbol} set to active!"


    @app.route('/symbols/set_inactive/<symbol>/')
    def symbol_set_inactive(symbol):
        symbol = db_service.get_symbols_by_symbol(symbol)
        symbol.active = 0
        db_service.commit()
        return f"{symbol.symbol} set to inactive!"


    @app.teardown_appcontext
    def shutdown_session(exception=None):
        database.db_session.remove()

    return app
