## human
* human_handoff
    - utter_human_handoff
## builder
* ask_builder
    - utter_ask_builder
## weather
* ask_weather
    - utter_ask_weather
## howdoing    
* ask_howdoing
    - utter_ask_howdoing
## whatspossible  
* ask_whatspossible
    - utter_ask_whatspossible
## isbot
* ask_isbot
    - utter_isbot
## whatisrasa
* ask_whatisrasa
    - utter_great
## howold
* ask_howold
    - utter_out_of_scope
## languagesbot
* ask_languagesbot
    - utter_languagesbot
## howbuilt
* ask_howbuilt
    - utter_howbuilt
## whoisit
* ask_whoisit
    - utter_not_sure
## restaurant
* ask_restaurant
    - utter_ask_restaurant
## time
* ask_time
    - utter_ask_time
## wherefrom
* ask_wherefrom
    - utter_ask_wherefrom
    
## greet
* greet
    - utter_greet
    
    
    
    
    
    
    
    
    
    
    

## Building card
* apply_for_credit_card
    - utter_apply_for_credit_card
* feedback{"credit_card_value":"黑卡"}
    - slot{"credit_card_value":"黑卡"}
    - utter_heika
    - create_credit_card_form
    - form{"name": "create_credit_card_form"}
    - form{"name": null}
    - utter_evaluate
* feedback{"credit_card_value":"金卡"}
    - slot{"credit_card_value":"金卡"}
    - utter_jinka
    - create_credit_card_form
    - form{"name": "create_credit_card_form"}
    - form{"name": null}
    - utter_evaluate
* feedback{"credit_card_value":"银卡"}
    - slot{"credit_card_value":"银卡"}
    - utter_yinka      
    - create_credit_card_form
    - form{"name": "create_credit_card_form"}
    - form{"name": null}
    - utter_evaluate
* feedback{"evaluate_value":"满意"}
    - slot{"evaluate_value":"满意"}
    - utter_awesome
    - action_restart
* feedback{"evaluate_value":"不满意"}
    - slot{"evaluate_value":"不满意"}
    - utter_nomanyi
    - action_restart

    

