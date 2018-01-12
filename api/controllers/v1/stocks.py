#!/usr/bin/env python
#-*- coding: utf-8 -*-
import pecan
from pecan import rest
from wsme import types as wtypes
import logging
from webdemo.api import expose
from pecan import request
import tushare as ts
from pandas import DataFrame
import json
from collections import OrderedDict

logger = logging.getLogger(__name__)


class StockDetail(wtypes.Base):
    date = wtypes.text
    open = float
    high = float
    close = float
    low = float
    volume = float

class Stock(wtypes.Base):
    id = wtypes.text
    name = wtypes.text
    industry = wtypes.text
    area = wtypes.text
    pe = float
    outstanding = float
    totals = float
    totalAssets = float
    detail = [StockDetail]

class Stocks(wtypes.Base):
    stocks = [Stock]

class StocksController(rest.RestController):

    '''
       None 表示这个方法没有返回值
       status_code 表示这个API的响应状态码是201
       test eg:
       curl -X POST http://localhost:8080/v1/stocks -H "Content-Type: application/json" -d '{"phone": ["1000860","100876"], "age": 24, "user_id": "133", "name": "kile", "email": "111@163.com"}' -v

    '''
    # @expose.expose(None, body=Person, status_code=201)
    # def post(self, user):
    #     db_conn = request.db_conn
    #     db_conn.add_user(user)

    @expose.expose(Stocks)
    def get(self):
        logger.info("Get all users Method is called ...")
        """

        user_info_list = [
            {
                'name': 'Alice',
                'age': 30,
            },
            {
                'name': 'Bob',
                'age': 40,
            }
        ]
        users_list = [User(**user_info) for user_info in user_info_list]
        """
        df = ts.get_stock_basics()
        ss = json.loads(
            DataFrame(df, columns=['name', 'industry', 'area', 'pe', 'outstanding', 'totals', 'totalAssets']).to_json(
                orient='index'),
            object_pairs_hook=OrderedDict)
        print ss
        if len(ss) == 0:
            return Stocks()
        ss_list = []
        for stock_id, stock_body in ss.items():
            u = Stock()
            u.id = stock_id
            u.name = stock_body['name']
            u.industry = stock_body['industry']
            u.area = stock_body['area']
            u.pe = stock_body['pe']
            u.outstanding = stock_body['outstanding']
            u.totals = stock_body['totals']
            u.totalAssets = stock_body['totalAssets']
            u.detail = []
            ss_list.append(u)
        return Stocks(stocks=ss_list)

    @pecan.expose()
    def _lookup(self, id, *remainder):
        return StockController(id), remainder

class StockController(rest.RestController):

    def __init__(self, id):
        self.stock_id = id

    """
    test eg:
         http://127.0.0.1:8080/v1/stock/abc
    """
    @expose.expose(Stock)
    def get(self):
        """
         logger.info("v1 UserController Get Method is called ...")
        user_info = {
            'id': self.user_id,
            'name': 'Alice',
            'age': 30,
        }
        """
        logger.info("stock_id %s" % self.stock_id)
        self.stock_id = id
        df = ts.get_hist_data('600848', start='2017-01-05', end='2018-01-09')
        s_detail = json.loads(DataFrame(df, columns=['open', 'high', 'close', 'low', 'volume']).to_json(orient='index'), object_pairs_hook=OrderedDict)
        print s_detail

        if s_detail is None:
            logger.info("user by user_id is not found...")
            return Stock()
        else:
            logger.info(
                "user by user_id is found ...")
            stock = Stock()
            stock.id = self.stock_id
            stock.name = '美丽动人'
            stock_detail = []
            for date, detail in s_detail.items():
                sd = StockDetail()
                sd.date = date
                sd.open = detail['open']
                sd.high = detail['high']
                sd.close = detail['close']
                sd.low = detail['low']
                sd.volume = detail['volume']
                stock_detail.append(sd)
            stock.detail = stock_detail
            return stock

    # """
    # test eg:
    #      curl -X PUT http://localhost:8080/v1/users/12 -H "Content-Type: application/json" -d '{"user_id": "12","name": "Cook", "age":50}'
    # """
    # @expose.expose(Person, body=Person)
    # def put(self, user):
    #     logger.info("v1 UserController Put Method is called ...")
    #     """
    #             user_info = {
    #         'user_id': user.user_id,
    #         'name': user.name,
    #         'age': user.age + 1
    #     }
    #     return Person(**user_info)
    #     """
    #     db_conn = request.db_conn
    #     person = db_conn.update_user(user)
    #     return person
    #
    # """
    # test eg:
    #      curl -X DELETE http://localhost:8080/v1/users/123
    # """
    #
    # @expose.expose()
    # def delete(self):
    #     logger.info("v1 UserController Delete Method is called ...")
    #     print('Delete user_id: %s' % self.user_id)
    #     db_conn = request.db_conn
    #     db_conn.delete_user(self.user_id)

# class UsersController(rest.RestController):
#
#     '''
#        None 表示这个方法没有返回值
#        status_code 表示这个API的响应状态码是201
#        test eg:
#        curl -X POST http://localhost:8080/v1/users -H "Content-Type: application/json" -d '{"phone": ["1000860","100876"], "age": 24, "user_id": "133", "name": "kile", "email": "111@163.com"}' -v
#
#     '''
#     @expose.expose(None, body=Person, status_code=201)
#     def post(self, user):
#         db_conn = request.db_conn
#         db_conn.add_user(user)
#
#     @expose.expose(Users)
#     def get(self):
#         logger.info("Get all users Method is called ...")
#         """
#
#         user_info_list = [
#             {
#                 'name': 'Alice',
#                 'age': 30,
#             },
#             {
#                 'name': 'Bob',
#                 'age': 40,
#             }
#         ]
#         users_list = [User(**user_info) for user_info in user_info_list]
#         """
#         db_conn = request.db_conn
#         users = db_conn.list_users()
#         if len(users) == 0:
#             return Users()
#         users_list = []
#         for user in users:
#             u = Person()
#             u.user_id = user.user_id
#             u.age = user.age
#             u.email = user.email
#             u.name = user.name
#             phones = []
#             for tel in user.telephone:
#                 logger.info(
#                     "user.id %s ... tel.user_id %s" %
#                     (user.id, tel.user_id))
#                 if user.id == tel.user_id:
#                     phones.append(tel.telnumber)
#             u.phone = phones
#             users_list.append(u)
#         return Users(users=users_list)
#
#     @pecan.expose()
#     def _lookup(self, user_id, *remainder):
#         return UserController(user_id), remainder



