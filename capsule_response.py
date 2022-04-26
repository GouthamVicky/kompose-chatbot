import json
import requests
import pprint
import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

def lead_form_creation(userId,serviceid):
    message="Our experts are ready to assist you. To begin speaking with one of our expert, please fill out the form below" 
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
                                    "formAction": os.getenv('form_action_url'),
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


def lead_form_creation_textarea(userId,serviceid):
    message="Our experts are ready to assist you. To begin speaking with one of our expert, please fill out the form below" 
    json=[
        {
                            "message": 
                            message,
                            
                            },
        {
            "metadata": {
                "contentType": "300",
                "payload": [
                    {
                        "type": "textarea",
                        "data": {
                            "cols": 10,
                            "validation": {
                                "regex": "^[^*|\\\":<>[\\]{}`\\\\()';@&$]+$",
                                "errorText": "To assist you effectively, please submit the query in detail with no special characters in it"
                            },
                            "title": "Please Type in your Query",
                            "name": "textarea",
                            "rows": 4,
                            "placeholder": "Type here ..",
                            "label":"textarea"
                        }
                    },
                    {
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
                            "name": "PhoneNumber",
                            "validation": {
                                "errorText": "Please Enter Valid 10 Digit Mobile Number",
                                "regex": "\\b^[0][0-9]{10}\\b|\\b[0-9]{10}\\b"
                            },
                            "label": "PhoneNumber"
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
                        "data": {
                            "name": "Submit",
                            "action": {
                                "message": "Submit",
                                "formAction": os.getenv('form_action_text_url')
                            },
                            "type": "submit"
                        },
                        "type": "submit"
                    }
                ],
                "templateId": "12"
            },
            "platform": "kommunicate"
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
    


def demoform(userId):
    message="If you'd like to book a demo to see Smart i in action, please fill in your details to schedule a call" 
    json=[
        {
                            "message": 
                            message,
                            
                            },
        {
            "metadata": {
                "contentType": "300",
                "payload": [
                    {
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
                            "name": "PhoneNumber",
                            "validation": {
                                "errorText": "Please Enter Valid 10 Digit Mobile Number",
                                "regex": "\\b^[0][0-9]{10}\\b|\\b[0-9]{10}\\b"
                            },
                            "label": "Mobile Number"
                        },
                        "type": "text"
                    },
                    {
                "type": "datetime-local",
                "data": {
                    "label": "Date",
                    "name":"Scheduled Date"
                }
                },
                    {
                                "type": "hidden",
                                "data": {
                                "value": userId,
                                "name": "ConvoID"
                                }
                            },
                    {
                                "type": "hidden",
                                "data": {
                                "value": "Book a Demo Call",
                                "name": "CustomerMotive"
                                }
                            },
                         
                    {
                        "data": {
                            "name": "Submit",
                            "action": {
                                "message": "Submit",
                                "formAction": os.getenv("domainUrl")+"webhook/smarti/formdata"
                            },
                            "type": "submit"
                        },
                        "type": "submit"
                    }
                ],
                "templateId": "12"
            },
            "platform": "kommunicate"
        }]
    return json

def queryform(userId):
    message="Could you please share your Query along with your Email address so that we'll get in touch with you asap!" 
    json=[
        {
                            "message": 
                            message,
                            
                            },
        {
            "metadata": {
                "contentType": "300",
                "payload": [
            {
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
                "type": "textarea",
                "data": {
                    "cols": 10,
                    "validation": {
                        "regex": "^[^*|\\\":<>[\\]{}`\\\\()';@&$]+$",
                        "errorText": "special characters not allowed"
                    },
                    "title": "Please Type in your Query",
                    "name": "textarea",
                    "rows": 4,
                    "placeholder": "Type here ..",
                    "label": "textarea"
                }
            },
             {
                                "type": "hidden",
                                "data": {
                                "value": userId,
                                "name": "ConvoID"
                                }
                            },
             {
                                "type": "hidden",
                                "data": {
                                "value": "Query Request",
                                "name": "CustomerMotive"
                                }
                            },
            {
                "data": {
                    "name": "Submit",
                    "action": {
                        "message": "Submit",
                        "formAction": os.getenv("domainUrl")+"webhook/smarti/formdata"
                    },
                    "type": "submit"
                },
                "type": "submit"
            }
        ],
                "templateId": "12"
            },
            "platform": "kommunicate"
        }]
    return json

def handleUnknown(userId,question):
    message="Hmm 🤔... I don't have an easy answer to that questions, but if you'd like to share your E-mail, One of our representatives will look into that for you and follow up 😀" 
    json=[
        {
                            "message": 
                            message,
                            
                            },
        {
            "metadata": {
                "message":"Could I get your email address?",
                "contentType": "300",
                "payload": [
            {
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
                                "type": "hidden",
                                "data": {
                                "value": userId,
                                "name": "ConvoID"
                                }
                            },
             
             {
                                "type": "hidden",
                                "data": {
                                "value": "Out of scope Questions",
                                "name": "CustomerMotive"
                                }
                            },
             {
                                "type": "hidden",
                                "data": {
                                "value": question,
                                "name": "Requested Question"
                                }
                            },
            {
                "data": {
                    "name": "Submit",
                    "action": {
                        "message": "Submit",
                        "formAction": os.getenv("domainUrl")+"webhook/smarti/formdata"
                    },
                    "type": "submit"
                },
                "type": "submit"
            }
        ],
                "templateId": "12"
            },
            "platform": "kommunicate"
        }]
    return json