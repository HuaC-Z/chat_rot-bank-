# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from typing import Text, Dict, Any, List
import json
import pandas as pds
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, UserUtteranceReverted, ConversationPaused, AllSlotsReset
import os
import pandas as pds
import requests
from USER.assistant import *

# tracker.current_state()
# tracker.latest_message["text"]
# tracker.get_latest_entity_values("entity")
# tracker.get_slot("shown_privacy")
# class rasa_sdf.events.Restarted(timestamp=None)

logger = logging.getLogger(__name__)


class CreateCreditCardFrom(FormAction):
    def name(self):
        return "create_credit_card_form"

    @staticmethod
    def required_slots(tracker):

        # 插槽名字和询问插槽的意图名字一致  utter_ask_name(动作) --->name(插槽)
        return [
            "name",
            "email",
            "id_card",
            "password",
            "password_confirm"
        ]

    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "name": [
                self.from_text(intent="enter_data"),
                self.from_entity(entity='name')
            ],
            "email": [
                self.from_entity(entity="email"),
                self.from_text(intent="enter_data"),
            ],
            "id_card": [
                self.from_text(intent="enter_data"),
            ],
            "password": [
                self.from_text(intent="enter_data"),
            ],
            "password_confirm": [
                self.from_text(intent="enter_data"),
            ],
        }

    def validate_email(self, value, dispatcher, tracker, domain):
        """Check to see if an id_card entity was actually picked up by duckling."""
        example = ['qq.com', '163.com', 'huohu.com', 'xinlang.com', '126.com']
        print('用户输入邮箱--->', tracker.latest_message["text"])
        if list(tracker.get_latest_entity_values("email")) != []:
            data = list(tracker.get_latest_entity_values("email"))[0].split("@")
            if len(data) == 2:
                if data[-1] in example:
                    return {"email": value}
                else:
                    dispatcher.utter_template('utter_no_email', tracker)
                    return {"email": None}
            else:
                dispatcher.utter_template('utter_no_email', tracker)
                return {"email": None}
        else:
            dispatcher.utter_template('utter_no_email', tracker)
            return {"email": None}

    def validate_id_card(self, value, dispatcher, tracker, domain):
        id_card = list(tracker.get_latest_entity_values('number'))
        """Check to see if an id_card entity was actually picked up by duckling."""
        print('用户输入证件号--->', id_card)
        if id_card != []:
            id_card = str(id_card[0])
            check = Check()
            id_card_list = check.check_id_card()
            if len(id_card) == 18:
                if id_card in id_card_list:
                    dispatcher.utter_message('此证件号已被使用,请确认后重新输入。')
                    return {"id_card": None}
                else:
                    return {"id_card": value}
            else:
                dispatcher.utter_template('utter_no_id_card', tracker)
                return {"id_card": None}
        else:
            dispatcher.utter_template('utter_no_id_card', tracker)
            return {"id_card": None}

    def validate_password(self, value, dispatcher, tracker, domain):
        password = list(tracker.get_latest_entity_values('number'))
        if password != []:
            print('用户输入密码--->', len(str(password[0])), password)
            if len(str(password[0])) == 6:
                return {"password": str(value)}
            else:
                dispatcher.utter_message('密码长度不对,请确认后重新输入。')
                return {"password": None}
        else:
            dispatcher.utter_message('密码长度不对,请确认后重新输入。')
            return {"password": None}

    def validate_password_confirm(self, value, dispatcher, tracker, domain):
        password_confirm = list(tracker.get_latest_entity_values('number'))
        if password_confirm != []:
            print('用户确认密码--->', len(str(password_confirm[0])), password_confirm)
            password = tracker.get_slot('password')
            if password == str(password_confirm[0]):
                return {"password_confirm": str(value)}
            else:
                dispatcher.utter_message('两次密码不一致,请确认后重新输入。')
                return {"password_confirm": None}
        else:
            dispatcher.utter_message('两次密码不一致,请确认后重新输入。')
            return {"password_confirm": None}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:

        card = tracker.get_slot('credit_card_value')
        name = tracker.get_slot('name')
        gene = Generator()
        check = Check()
        bank_card_list = check.check_bank_card()
        flag = True
        while flag:
            bank_card = gene.generate_bank_card()
            if bank_card in bank_card_list:
                flag = True
            else:
                flag = False
        id_card = tracker.get_slot('id_card')
        email = tracker.get_slot('email')
        password = tracker.get_slot('password')
        dispatcher.utter_message('恭喜您,办卡成功!请记住您的银行卡号【{}】'.format(bank_card))
        dispatcher.utter_message('开始存储用户信息...')
        print('存储用户信息')
        sto = Store(card, name, bank_card, id_card, email, password)

        dispatcher.utter_message(sto.store())
        return []


class CheckBalace(FormAction):
    def name(self):
        return "check_balance_form"

    @staticmethod
    def required_slots(tracker):

        # 插槽名字和询问插槽的意图名字一致  utter_ask_name(动作) --->name(插槽)
        return [
            "bank_card",
            "password",
        ]

    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "bank_card": [
                self.from_text(intent="enter_data"),
            ],
            "password": [
                self.from_text(intent="enter_data"),
            ]
        }

    def validate_bank_card(self, value, dispatcher, tracker, domain):
        bank_card = list(tracker.get_latest_entity_values('number'))
        bank_card_list = list(Check().check_bank_card())
        print('用户输入银行卡--->', bank_card)
        if bank_card != []:
            if bank_card[0] in bank_card_list:
                return {"bank_card": value}
            else:
                dispatcher.utter_message('对不起，此卡未注册')
                return {"bank_card": None}
        else:
            dispatcher.utter_message('此卡未注册')
            return {"bank_card": None}

    def validate_password(self, value, dispatcher, tracker, domain):
        bank_card = tracker.get_slot('bank_card')
        pwd = Check().check_password(int(bank_card))
        password = list(tracker.get_latest_entity_values('number'))
        print('用户输入密码--->', password, str(password[0]))
        if password != []:
            print(str(pwd))
            print(str(password[0]) == str(pwd))
            if str(password[0]) == str(pwd):
                return {"password": value}
            else:
                dispatcher.utter_message('密码不正确')
                return {"password": None}
        else:
            dispatcher.utter_message('密码不正确')
            return {"password": None}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:

        bank_card = tracker.get_slot("bank_card")
        info = Bank().balance(int(bank_card))
        if info == []:
            return []
        else:
            dispatcher.utter_message('{}账号的余额还有{}元'.format(info[0], info[1]))
            return []


class DepositMoneyForm(FormAction):
    def name(self):
        return "deposit_money_form"

    @staticmethod
    def required_slots(tracker):
        return [
            "bank_card",
            "password",
            "save_money",
        ]

    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "bank_card": [
                self.from_text(intent="enter_data"),
            ],
            "password": [
                self.from_text(intent="enter_data"),
            ],
            "save_money": [
                self.from_text(intent="enter_data"),
            ],

        }

    def validate_bank_card(self, value, dispatcher, tracker, domain):
        bank_card = list(tracker.get_latest_entity_values('number'))
        bank_card_list = list(Check().check_bank_card())
        print('用户输入银行卡--->', bank_card)
        if bank_card != []:
            if bank_card[0] in bank_card_list:
                return {"bank_card": value}
            else:
                dispatcher.utter_message('对不起，此卡未注册')
                return {"bank_card": None}
        else:
            dispatcher.utter_message('此卡未注册')
            return {"bank_card": None}

    def validate_password(self, value, dispatcher, tracker, domain):
        bank_card = tracker.get_slot('bank_card')
        pwd = Check().check_password(int(bank_card))
        password = list(tracker.get_latest_entity_values('number'))
        print('用户输入密码--->', password, str(password[0]))
        if password != []:
            print(str(pwd))
            print(str(password[0]) == str(pwd))
            if str(password[0]) == str(pwd):
                return {"password": value}
            else:
                dispatcher.utter_message('密码不正确')
                return {"password": None}
        else:
            dispatcher.utter_message('密码不正确')
            return {"password": None}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Once we have all the information, attempt to add it to the
        Google Drive database"""

        money = float(tracker.get_slot('save_money'))
        bank_card = int(tracker.get_slot("bank_card"))
        dispatcher.utter_message(Bank().deposit(bank_card, money))
        return []


class WithdrawMoneyForm(FormAction):
    def name(self):
        return "withdraw_money_form"

    @staticmethod
    def required_slots(tracker):
        return [
            "bank_card",
            "password",
            "withdraw_money",
        ]

    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "bank_card": [
                self.from_text(intent="enter_data"),
            ],
            "password": [
                self.from_text(intent="enter_data"),
            ],
            "withdraw_money": [
                self.from_text(intent="enter_data"),
            ],
        }

    def validate_bank_card(self, value, dispatcher, tracker, domain):
        bank_card = list(tracker.get_latest_entity_values('number'))
        bank_card_list = list(Check().check_bank_card())
        print('用户输入银行卡--->', bank_card)
        if bank_card != []:
            if bank_card[0] in bank_card_list:
                return {"bank_card": value}
            else:
                dispatcher.utter_message('对不起，此卡未注册')
                return {"bank_card": None}
        else:
            dispatcher.utter_message('此卡未注册')
            return {"bank_card": None}

    def validate_password(self, value, dispatcher, tracker, domain):
        bank_card = tracker.get_slot('bank_card')
        pwd = Check().check_password(int(bank_card))
        password = list(tracker.get_latest_entity_values('number'))
        print('用户输入密码--->', password, str(password[0]))
        if password != []:
            print(str(pwd))
            print(str(password[0]) == str(pwd))
            if str(password[0]) == str(pwd):
                return {"password": value}
            else:
                dispatcher.utter_message('密码不正确')
                return {"password": None}
        else:
            dispatcher.utter_message('密码不正确')
            return {"password": None}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Once we have all the information, attempt to add it to the
        Google Drive database"""

        money = float(tracker.get_slot('withdraw_money'))
        bank_card = int(tracker.get_slot("bank_card"))
        dispatcher.utter_message(Bank().withdraw(bank_card, money))
        return []


class TransferMoney(FormAction):
    def name(self):
        return "transfer_money_form"

    @staticmethod
    def required_slots(tracker):
        return [
            "bank_card",
            "to_bank_card",
            "transfer_money",
            "password",
        ]

    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "bank_card": [
                self.from_text(intent="enter_data"),
            ],
            "password": [
                self.from_text(intent="enter_data"),
            ],
            "to_bank_card": [
                self.from_text(intent="enter_data")
            ],
            "transfer_money": [
                self.from_text(intent="enter_data"),
            ],
        }

    def validate_bank_card(self, value, dispatcher, tracker, domain):
        bank_card = list(tracker.get_latest_entity_values('number'))
        bank_card_list = list(Check().check_bank_card())
        print('用户输入银行卡--->', bank_card)
        if bank_card != []:
            if bank_card[0] in bank_card_list:
                return {"bank_card": value}
            else:
                dispatcher.utter_message('对不起，此卡未注册')
                return {"bank_card": None}
        else:
            dispatcher.utter_message('此卡未注册')
            return {"bank_card": None}

    def validate_password(self, value, dispatcher, tracker, domain):
        bank_card = tracker.get_slot('bank_card')
        pwd = Check().check_password(int(bank_card))
        password = list(tracker.get_latest_entity_values('number'))
        print('用户输入密码--->', password, str(password[0]))
        if password != []:
            if str(password[0]) == str(pwd):
                dispatcher.utter_message('密码验证成功!')
                return {"password": value}
            else:
                dispatcher.utter_message('密码不正确!')
                return {"password": None}
        else:
            dispatcher.utter_message('密码不正确!')
            return {"password": None}

    def validate_to_bank_card(self, value, dispatcher, tracker, domain):
        pre_bank_card = int(tracker.get_slot('bank_card'))
        bank_card = list(tracker.get_latest_entity_values('number'))
        bank_card_list = list(Check().check_bank_card())
        print('之前的银行卡--->', pre_bank_card)
        print('用户输入银行卡--->', bank_card)
        if bank_card != []:
            if bank_card[0] in bank_card_list and bank_card[0] != pre_bank_card:
                return {"to_bank_card": value}
            else:
                dispatcher.utter_message('对不起，此卡未注册或此卡为已输卡号!')
                return {"to_bank_card": None}
        else:
            dispatcher.utter_message('此卡未注册!')
            return {"to_bank_card": None}

    def submit(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ) -> List[Dict]:

        money = float(tracker.get_slot('transfer_money'))
        bank_card = int(tracker.get_slot("bank_card"))
        to_bank_card = int(tracker.get_slot("to_bank_card"))
        dispatcher.utter_message(Bank().transfer(bank_card, money, to_bank_card))
        return []


class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
            self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain,  # type:  Dict[Text, Any]
    ) -> List["Event"]:
        intent = tracker.latest_message["text"]
        print(intent)
        print(tracker.latest_message)
        chatbot = ChatRobotAPI(intent)
        dispatcher.utter_message(
            chatbot.chat()
        )
        return [UserUtteranceReverted()]


class ChatRobotAPI(object):

    def __init__(self, content):
        self.content = content

    def chat(self):
        sess = requests.get('https://api.ownthink.com/bot?spoken=' + self.content)
        print(sess)
        answer = sess.text
        print(answer)
        answer = json.loads(answer)
        print(answer)
        # {'data': {'info': {'text': '让我给你一个大大的拥抱，纪念我们每一次的问好！'}, 'type': 5000}, 'message': 'success'}
        return answer['data']['info']['text']
