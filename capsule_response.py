import json
import requests
import pprint


def lead_form_collection(sessionId):
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
                                "placeholder": "Enter your email",
                                "validation": {
                                    "errorText": "Invalid Email",
                                    "regex": "^(([^<>()\\[\\]\\.;:\\s@\"]+(\\.[^<>()[\\]\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$"
                                },
                                "label": "Email"
                                },
                                "type": "text"
                            },
                            {
                                "data": {
                                "placeholder": "Enter your Phone Number",
                                
                                "name":"PhoneNumber",
                                "validation": {
                                    "errorText": "Please Enter Valid 10 Digit Mobile Number",
                                    "regex": "\\b^[0][0-9]{10}\\b|\\b[0-9]{10}\\b"
                                },
                                "label":"PhoneNumber"
                                },
                                
                                "type": "text"
                            },
                            {
                                "type": "hidden",
                                "data": {
                                "value": sessionId,
                                "name": "sessionId"
                                }
                            },
                            {
                                "type": "submit",
                                "data": {
                                "action": {
                                    "formAction": "https://dev-ml.vakilsearch.com/mlchatbot/store/user/details/incorp",
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
