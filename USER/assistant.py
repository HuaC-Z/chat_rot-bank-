# -*- coding: utf-8 -*-
"""
Created on 2020/4/29 10

@Author: Czh
"""
import random
import string
import pandas as pds
import os

PATH = os.path.dirname(__file__)


class Generator():

    def generate_bank_card(self):
        bank_card = '1708' + ''.join([random.choice(string.digits) for i in range(8)])

        return bank_card


class Check():
    def check_data(self):
        bank = pds.read_csv(PATH + r'/Information.csv')
        return bank

    def check_id_card(self):
        bank = pds.read_csv(PATH + r'/Information.csv')
        id_card_list = list(bank['id_card'])
        return id_card_list

    def check_bank_card(self):
        bank = pds.read_csv(PATH + r'/Information.csv')
        bank_card_list = list(bank['bank_card'])
        return bank_card_list

    def check_password(self, bank_card):
        bank = pds.read_csv(PATH + r'/Information.csv')
        password = list(bank.loc[bank['bank_card'] == bank_card, 'password'])[0]
        return password


class Store():
    def __init__(self, card, name, bank_card, id_card, email, password):
        self.card = card
        self.name = name
        self.bank_card = bank_card
        self.id_card = id_card
        self.email = email
        self.password = password

    def store(self):
        bank = pds.read_csv(PATH + r'/Information.csv')
        new = pds.Series(
            {'card': self.card, 'bank_card': self.bank_card, 'name': self.name, 'email': self.email,
             'id_card': self.id_card, 'password': str(self.password), 'balance': 0.0})
        bank = bank.append(new, ignore_index=True)
        bank.to_csv(PATH + r'/Information.csv', index=False)

        return '存储成功'


class Bank():

    def balance(self, bank_card):
        bank = pds.read_csv(PATH + r'/Information.csv')
        balance = list(bank.loc[bank['bank_card'] == bank_card, 'balance'])[0]
        name = list(bank.loc[bank['bank_card'] == bank_card, 'name'])[0]
        return [name, balance]

    def deposit(self, bank_card, money):  # 存钱
        bank = pds.read_csv(PATH + r'/Information.csv')
        name = list(bank.loc[bank['bank_card'] == bank_card, 'name'])[0]
        balance = list(bank.loc[bank['bank_card'] == bank_card, 'balance'])[0] + money
        bank.loc[bank['bank_card'] == bank_card, 'balance'] = balance
        bank.to_csv(PATH + r'/Information.csv', index=False)
        return '存钱成功,目前{}的账号余额为:{}元'.format(name, balance)

    def withdraw(self, bank_card, money):  # 取钱
        bank = pds.read_csv(PATH + r'/Information.csv')
        name = list(bank.loc[bank['bank_card'] == bank_card, 'name'])[0]
        balance = list(bank.loc[bank['bank_card'] == bank_card, 'balance'])[0] - money
        bank.loc[bank['bank_card'] == bank_card, 'balance'] = balance
        bank.to_csv(PATH + r'/Information.csv', index=False)
        return '取钱成功,目前{}的账号余额为:{}元'.format(name, balance)

    def transfer(self, bank_card, money, to_bank_card):
        bank = pds.read_csv(PATH + r'/Information.csv')
        name = list(bank.loc[bank['bank_card'] == bank_card, 'name'])[0]
        row_money = list(bank.loc[bank['bank_card'] == bank_card, 'balance'])[0]
        balance = row_money - money
        if balance < 0:
            return '对不起,{}账号的余额不足,现在的余额为{}元'.format(name, row_money)
        else:
            bank.loc[bank['bank_card'] == bank_card, 'balance'] = balance

            end_balance = list(bank.loc[bank['bank_card'] == to_bank_card, 'balance'])[0] + money
            bank.loc[bank['bank_card'] == to_bank_card, 'balance'] = end_balance
            bank.to_csv(PATH + r'/Information.csv', index=False)
            return '转账成功,目前{}的账号余额为:{}元'.format(name, balance)
