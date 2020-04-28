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

# tracker.current_state()
# tracker.get_latest_entity_values("entity")
# tracker.get_slot("shown_privacy")
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

    # 验证插槽，如果该插槽有值则直接跳过此故事线
    #     def validate_email(
    #         self,
    #         slot_dict: Dict[Text, Any],
    #         dispatcher: "CollectingDispatcher",
    #         tracker: "Tracker",
    #         domain: Dict[Text, Any],
    #     ) -> List[EventType]:
    def validate_name(self, value, dispatcher, tracker, domain):
        name = list(tracker.get_latest_entity_values('name'))
        """Check to see if an id_card entity was actually picked up by duckling."""
        print('name--->',len(name[0]), name, value, tracker.get_slot('name'))
        bank = pds.read_csv(PATH + r'\USER\Information.csv')
        name_list = list(bank['user_name'])
        if name[0] in name_list:
            # entity was picked up, validate slot
            return {"name": None}
        else:
            # no entity was picked up, we want to ask again
            return {"name": value}


    def validate_email(self, value, dispatcher, tracker, domain):
        """Check to see if an id_card entity was actually picked up by duckling."""
        example = ['qq.com', '163.com', 'huohu.com', 'xinlang.com', '126.com']
        data = list(tracker.get_latest_entity_values("email"))
        print('email--->', data)
        if tracker.get_slot('email') != None:
            return {"email": tracker.get_slot('email')}
        else:
            if len(data) == 2:
                if data[-1] in example:
                # entity was picked up, validate slot
                    return {"email": value}
                else:
                    return {"email": None}
            else:
                # no entity was picked up, we want to ask again
                return {"email": None}

        # 每次调用表单后输入数据都会验证
    def validate_password(self, value, dispatcher, tracker, domain):
        password = list(tracker.get_latest_entity_values('number'))
        """Check to see if an id_card entity was actually picked up by duckling."""
        print('password--->', len(str(password[0])), password, value, tracker.get_slot('password'))
        if len(str(password[0])) == 6:
            # entity was picked up, validate slot
            return {"password": value}
        else:
            # no entity was picked up, we want to ask again
            return {"password": None}
    # 每次调用表单后输入数据都会验证
    def validate_id_card(self, value, dispatcher, tracker, domain):
        id_card = list(tracker.get_latest_entity_values('number'))
        """Check to see if an id_card entity was actually picked up by duckling."""
        print('id_card--->',len(str(id_card[0])), id_card, value, tracker.get_slot('password'))
        if len(str(id_card[0])) == 9:
            # entity was picked up, validate slot
            return {"id_card": value}
        else:
            # no entity was picked up, we want to ask again
            return {"id_card": None}

    def validate_password_confirm(self, value, dispatcher, tracker, domain):
        password_confirm = list(tracker.get_latest_entity_values('number'))
        """Check to see if an id_card entity was actually picked up by duckling."""
        password = tracker.get_slot('password')
        if password == password_confirm[0]:
            # entity was picked up, validate slot
            return {"password_confirm": value}
        else:
            # no entity was picked up, we want to ask again
            return {"password": None}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Once we have all the information, attempt to add it to the
        Google Drive database"""

        name = tracker.get_slot("name")
        id_card = tracker.get_slot("id_card")
        email = tracker.get_slot("email")
        password = tracker.get_slot('password')

        import datetime
        print('开始存储用户信息...')
        bank = pds.read_csv(PATH + r'\USER\Information.csv')

        new = pds.Series({'user_name': name, 'email':email,'id_card': id_card, 'password': password, 'balance': 0})
        bank = bank.append(new, ignore_index=True)
        bank.iloc[:, 1:].to_csv(PATH + r'\USER\Information.csv')

        date = datetime.datetime.now().strftime("%d/%m/%Y")

        sales_info = [name, id_card, password, date, email]

        # gdrive = GDriveService()
        # try:
        #     # gdrive.store_data(sales_info)
        #     print("User info store success!")
        #     dispatcher.utter_template("utter_confirm_store", tracker)
        #     return []
        # except Exception as e:
        #     logger.error(
        #         "Failed to write data to gdocs. Error: {}" "".format(e.message),
        #         exc_info=True,
        #     )
        #     dispatcher.utter_template("utter_store_failed", tracker)
        #     return []

        print("User info store success!")
        dispatcher.utter_template("utter_confirm_store", tracker)
        return []
class ResetSlots(Action):

    def name(self):
        return 'reset_slots'

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]
