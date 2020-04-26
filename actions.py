# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from typing import Text, Dict, Any, List
import json

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, UserUtteranceReverted, ConversationPaused


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
                "id_card"]


    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "email": [
                self.from_entity(entity="email"),
                self.from_text(intent="enter_data"),
            ],
            "name": [self.from_entity(entity="name"),
                     self.from_text(intent="enter_data"),
                     ],
            "id_card": [
                self.from_entity(entity="number"),
                self.from_text(intent="enter_data"),
            ]
        }
# 验证插槽，如果该插槽有值则直接跳过此故事线
#     def validate_slots(
#         self,
#         slot_dict: Dict[Text, Any],
#         dispatcher: "CollectingDispatcher",
#         tracker: "Tracker",
#         domain: Dict[Text, Any],
#     ) -> List[EventType]:
#     def validate_id_card(self, value, dispatcher, tracker, domain):
#
#         """Check to see if an id_card entity was actually picked up by duckling."""
#         if any(tracker.get_slot("id_card")):
#             # entity was picked up, validate slot
#             return {"id_card": value}
#         else:
#             # no entity was picked up, we want to ask again
#             dispatcher.utter_template("utter_no_id_card", tracker)
#             return {"id_card": None}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Once we have all the information, attempt to add it to the
        Google Drive database"""

        import datetime

        name = tracker.get_slot("name")
        id_card = tracker.get_slot("id_card")
        email = tracker.get_slot("email")
        credit_card_value = tracker.get_slot("credit_card_value")

        date = datetime.datetime.now().strftime("%d/%m/%Y")

        sales_info = [name, id_card, credit_card_value, date, email]

        #gdrive = GDriveService()
        try:
            #gdrive.store_data(sales_info)
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
