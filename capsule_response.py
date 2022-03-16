import json
import requests
import pprint
import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

def lead_form_creation(userId,serviceid):
    message="Our experts are on standby to answer any other questions you have. Please provide your details so that we can reach you within 24hrs" 
    json= [
                        {
                            "message": 
                            message,
                            
                            },
                        
                {
                    
                    "metadata": {
                        "contentType": "300",
                        "templateId": "12",
                         "payload":[ {
                                "data": {
                                "placeholder": "Your email please",
                                "validation": {
                                    "errorText": "Please provide a valid email",
                                    "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$"
                                },
                                "label": "Email"
                                },
                                "type": "text"
                            },
                            {
                                "data": {
                                "placeholder": "Your mobile number please (10 digits)",
                                
                                "name":"PhoneNumber",
                                "validation": {
                                    "errorText": "Please provide a valid 10 digit mobile number",
                                    "regex": "\\b^[0][0-9]{10}\\b|\\b[0-9]{10}\\b"
                                },
                                "label":"PhoneNumber"
                                },
                                
                                "type": "text"
                            },
                            {
                                "type": "hidden",
                                "data": {
                                "value": userId,
                                "name": "sessionID"
                                }
                            },
                            {
                                "type": "hidden",
                                "data": {
                                "value": serviceid,
                                "name": "serviceId"
                                }
                            },
                            {
                                "type": "submit",
                                "data": {
                                "action": {
                                    "formAction": os.getenv('form_action_Url'),
                                    "requestType": "application/x-www-form-urlencoded",
                                    "message": "Submit",
				    "replyText":"hide form template"
                                },
                                "type": "submit",
                                "name": "Submit"
                                }
                            }]
                    }
                }]          
    return json

def acknowldgement_message(url):
    try:
        
        now = datetime.now().hour
        now=int(now)+6
        if (int(now) < 19) and (int(now) >= 9):
            message="Thank you for your enquiry! One of our experts will get back to you within 2 hours.\nPlease click the following URL to proceed for Payment"
        else:
            message="Thank you for your enquiry! We are currently offline. Our experts will reach out to you during regular business hours (Monday to Saturday 9am - 7pm).\nPlease click the following URL to proceed for Payment"
        print(message)
        json= [
                        {
                            "message": 
                            message,
                            
                            },
                        
                {
                    "metadata": {
                        "contentType": "300",
                        "templateId": "3",
                        "payload": [
                            {
                            "name": "Pay Now",
                            "title": "Do you have More Questions?",
                            "url":"https://"+url,
                            "openLinkInNewTab":True,
                            "type": "link"
                            }
                        ]
                    }
                }]          
        return json
    except Exception as e:
        print("Error ====================>"+str(e))
        json= [
                        {
                            "message": 
                            "If you want to connect with one of our Experts, Please click the below capsule",
                            
                            },
                        
                {
                    
                    "metadata": {
                        "contentType": "300",
                        "templateId": "11",
                        "payload": [
                            {
                            "name": "Chat with Experts",
                            "action": {
                            "title": "Chat with Experts",
                            "message":  "Chat with Experts",
                            "type": "quickReply"
                            }
                            }
                        ]
                    }
                }]          
        return json