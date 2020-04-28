# -*- coding: utf-8 -*-
"""
Created on 2020/4/27 23

@Author: Czh
"""
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

PATH = os.path.dirname(__file__)
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
            "credit_card"
        ]

    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "name": [self.from_entity(entity="name"),
                     self.from_text(intent="enter_data"),
                     ],
            "email": [
                self.from_entity(entity="email"),
                self.from_text(intent="enter_data"),
            ],

            "id_card": [
                self.from_entity(entity="id_card"),
                self.from_text(intent="enter_data"),
            ],
            "password": [
                self.from_entity(entity="password"),
                self.from_text(intent="enter_data"),
            ],
            "credit_card": [
                self.from_entity(entity="credit_card"),
                self.from_text(intent="enter_data"),
            ]
        }

    # 验证插槽，如果该插槽有值则直接跳过此故事线
    #     def validate_email(
    #         self,
    #         slot_dict: Dict[Text, Any],
    #         dispatcher: "CollectingDispatcher",
    #         tracker: "Tracker",
    #         domain: Dict[Text, Any],
    #     ) -> List[EventType]:
    def validate_email(self, value, dispatcher, tracker, domain):
        """Check to see if an id_card entity was actually picked up by duckling."""
        example = ['qq.com', '163.com', 'huohu.com', 'xinlang.com', '126.com']
        data = tracker.get_slot("email").split('@')
        if len(data) == 2 and data[-1] in example:
            # entity was picked up, validate slot
            return {"email": value}
        else:
            # no entity was picked up, we want to ask again
            dispatcher.utter_template("utter_no_email", tracker)
            return {"email": None}

    def validate_password(self, value, dispatcher, tracker, domain):
        password = str(tracker.get_slot('password'))
        """Check to see if an id_card entity was actually picked up by duckling."""
        if len(password) == 6:
            # entity was picked up, validate slot
            return {"password": value}
        else:
            # no entity was picked up, we want to ask again
            dispatcher.utter_template("utter_no_password", tracker)
            return {"password": None}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Once we have all the information, attempt to add it to the
        Google Drive database"""

        import datetime
        print(tracker.slots)

        bank = pds.read_csv(PATH + r'\USER\Information.csv')
        name = tracker.get_slot("name")
        id_card = tracker.get_slot("id_card")
        email = tracker.get_slot("email")
        password = tracker.get_slot('password')
        credit_card = tracker.get_slot('credit_card')
        new = pds.Series({'user_name': name, 'id_card': id_card, 'password': password,'credit_card':credit_card, 'balance': 0})
        bank = bank.append(new, ignore_index=True)
        bank.iloc[:, 1:].to_csv(PATH + r'\USER\Information.csv')

        date = datetime.datetime.now().strftime("%d/%m/%Y")

        sales_info = [name, id_card, password, date, email]

        # gdrive = GDriveService()
        try:
            # gdrive.store_data(sales_info)
            print("User info store success!")
            dispatcher.utter_template("utter_confirm_store", tracker)
            return []
        except Exception as e:
            logger.error(
                "Failed to write data to gdocs. Error: {}" "".format(e.message),
                exc_info=True,
            )
            dispatcher.utter_template("utter_store_failed", tracker)
            return []


class ResetSlots(Action):

    def name(self):
        return 'reset_slots'

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]
'''
,user_name,email,id_card,password,credit_card,balance
0,陈政华,fourgroup1@163.com,100001,123456,41708001,8888888888
1,胡林冲,fourgroup2@163.com,100002,123456,41708002,8888888888
2,马登州,fourgroup3@163.com,100003,123456,41708003,8888888888
3,孙少博,fourgroup4@163.com,100004,123456,41708004,8888888882
'''