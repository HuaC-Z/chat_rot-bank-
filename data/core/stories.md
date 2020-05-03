## builder
* ask_builder
    - utter_ask_builder
## greet
* greet
    - utter_greet
## outofscrop
* out_of_scope
    - utter_out_of_scope
## bye
* bye
    - utter_bye     

## withdraw_money
* withdraw_money
    - withdraw_money_form
    - form{"name": "withdraw_money_form"}
    - form{"name": null}
    - action_restart
    

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
* feedback{"credit_card_value":"退出"}   
    - action_restart
* feedback{"evaluate_value":"满意"}
    - slot{"evaluate_value":"满意"}
    - utter_awesome
    - action_restart
* feedback{"evaluate_value":"不满意"}
    - slot{"evaluate_value":"不满意"}
    - utter_nomanyi
    - action_restart
    
## check blance
* show_accounts
    - check_balance_form
    - form{"name": "check_balance_form"}
    - form{"name": null}
    - action_restart

## Deposit money
* deposit_money
    - deposit_money_form
    - form{"name": "deposit_money_form"}
    - form{"name": null}
    - action_restart 
  
## transfer money
* transfer_money
    - transfer_money_form
    - form{"name": "transfer_money_form"}
    - form{"name": null}
    - action_restart