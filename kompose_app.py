from requests.sessions import session
from capsule_response import lead_form_creation
from fastapi import FastAPI, Depends,Form,Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, BaseSettings
from json import dump, loads,dumps
from fastapi import FastAPI, Response, status
import uvicorn
from typing import Any, Dict, AnyStr, List, Union
from fastapi.middleware.cors import CORSMiddleware
from capsule_response import *
from datetime import datetime
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import datetime

load_dotenv()

app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000/online-trademark-registration",
    "https://qe.vakilsearch.com",
    "https://qe-helpdesk.vakilsearch.com/ml-nw/payment/url/",
    "https://qe.vakilsearch.com/online-trademark-registration",
    "https://www.google.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = MongoClient(os.getenv('mongo_client_url'))
db=client['kompose_lead_form']
db=db.myCollection


JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]



@app.post("/webhook/incorp/")
async def root(arbitrary_json: JSONStructure = None):
    input_json={}
    for key ,value in arbitrary_json.items():
        input_json[key.decode("utf-8")]=value
    

    print(input_json)

    input_name=input_json['matchedIntentName']
    print("User Message =========== >",input_name)
    session_id=str(input_json['groupId'])
    print("User Message =========== >",str(session_id))
    intent_number=input_json['matchedIntent']
    print("Intent Number ============>",intent_number)



    if input_name.lower()=="i have other questions" or str(intent_number)=="623094b838b63d0fcc232800":
        message=lead_form_creation(session_id,1)
        return message
    
    if input_name.lower()=="submit" or str(intent_number)=="62319adc38b63d0fcc2328c9":
        retrive=db.find_one({"SessionID":user_id})
        email=retrive['EmailId']
        phone=retrive['PhoneNumber']
        serviceid=retrive['serviceId']
        url=retrive['paymentUrl']
        print(email,phone,url)

        message=acknowldgement_message(email, phone,input_json,serviceid)
        return message
    

    


@app.post("/store/session")
async def session_predict(Email: str = Form(...),PhoneNumber: str = Form(...),sessionID: str = Form(...),serviceId: str = Form(...)):

    current_date_and_time = datetime.datetime.now()
    print(sessionID)
    hours = 5
    minutes =30
    hours_added = datetime.timedelta(hours = hours,minutes=minutes)

    future_date_and_time = current_date_and_time + hours_added

    
    current =str(future_date_and_time)
    print(current)
    
    json= {"EmailId":Email,"PhoneNumber": PhoneNumber,"timeStamp":current,"SessionID":sessionID,"serviceId":serviceId,"ticketID":result['ticketId'],"paymentUrl":result['url']}

    print("CREATING TICKET ID FOR CUSTOMER")
    result=idgeneration(Email, PhoneNumber,json,serviceId)
    print(result)
    print("STORING DATA IN MONGO DB ")
    store_data=db.insert_one({"EmailId":Email,"PhoneNumber": PhoneNumber,"timeStamp":current,"SessionID":sessionID,"serviceId":serviceId,"ticketID":result['ticketId'],"paymentUrl":result['url']})
    print(json)
    
    return json


if __name__ == "__main__":

    uvicorn.run("kompose_app:app", host="0.0.0.0", port=19025, log_level="info", workers = 2,debug=True)