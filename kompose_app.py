from requests.sessions import session
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
from lead_creation import idgeneration
from fastapi.responses import HTMLResponse
from gsheetmongodb import gsheet_upload

load_dotenv()

app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:3000",
    "http://localhost:3000/online-trademark-registration",
    "https://qe.vakilsearch.com",
    "https://qe-helpdesk.vakilsearch.com/ml-nw/payment/url/",
    "https://qe.vakilsearch.com/online-trademark-registration",
    "https://www.google.com",
    "https://vakilsearch.com",
    "https://vakilsearch.com/online-company-registration"
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
smarti=client['smartichatbot']
smartiDb=smarti.myCollection


JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]



@app.post("/webhook/incorp/")
async def root_incorp(arbitrary_json: JSONStructure = None):
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



    if input_name.lower()=="i have other questions" or str(intent_number)=="623094b838b63d0fcc232800" or input_name=="Free Consultation" or str(intent_number)=="6230a49138b63d0fcc23280a":
        message=lead_form_creation(session_id,1)
        return message
    
    if input_name.lower()=="submit" or str(intent_number)=="62319adc38b63d0fcc2328c9":
        retrive=db.find_one({"SessionID":session_id})
        email=retrive['EmailId']
        phone=retrive['PhoneNumber']
        serviceid=retrive['serviceId']
        url=retrive['paymentUrl']
        print(email,phone,url)

        message=acknowldgement_message(url)
        return message
    if input_name=="I have a Query" or str(intent_number)=="6230a41739e8290fc89845c1":
        message=lead_form_creation(session_id,1)
        return message

@app.post("/webhook/smarti/")
async def root_smarti(arbitrary_json: JSONStructure = None):
    input_json={}
    for key ,value in arbitrary_json.items():
        input_json[key.decode("utf-8")]=value
    
    print(input_json)
    if "matchedIntentName" in input_json.keys():
        input_name=input_json['matchedIntentName']
        print("User Message =========== >",input_name) 
    
    session_id=str(input_json['groupId'])
    print("User Message =========== >",str(session_id))
    intent_number=input_json['matchedIntent']
    print("Intent Number ============>",intent_number)
    
    if str(intent_number)=="623a9c2939e8290fc8985098":
        question=input_json['message']
        message=handleUnknown(session_id,question)
        return message
    elif input_name=="Book a demo" or str(intent_number)=="623aa1d839e8290fc89850a8":
        message=demoform(session_id)
        return message
    elif input_name=="asking for Question" or str(intent_number)=="623aa59739e8290fc89850ae":
        message=queryform(session_id)
        return message
    

@app.post("/kompose/store/session")
async def session_predict(request:Request):
    form_data=await request.form()
    
    form_data_keys=list(form_data.keys())
    form_data_values=list(form_data.values())
    output_json=dict(zip(form_data_keys, form_data_values))
    current_date_and_time = datetime.datetime.now()
    
    hours = 5
    minutes =30
    hours_added = datetime.timedelta(hours = hours,minutes=minutes)

    future_date_and_time = current_date_and_time + hours_added

    
    current =str(future_date_and_time)
    print(current)
    output_json['timeStamp']=current
    
    output_json['PhoneNumber']=output_json['Mobile Number']
    #output_json['Mobile Number']
    print(output_json)
    #json= {"EmailId":Email,"PhoneNumber": PhoneNumber,"timeStamp":current,"SessionID":sessionID,"serviceId":serviceId}
    print("CREATING TICKET ID FOR CUSTOMER")
    result=idgeneration(output_json['Email'], output_json['PhoneNumber'],output_json,output_json['serviceId'])
    print(result)
    print("STORING DATA IN MONGO DB ")
    output_json['']
    store_data=db.insert_one({"EmailId":output_json['Email']})
    print(store_data)
    
    return json



@app.post("/kompose/store/textarea")
async def session_textarea(textarea: str= Form(...),Email: str = Form(...),PhoneNumber: str = Form(...),sessionID: str = Form(...),serviceId: str = Form(...)):

    current_date_and_time = datetime.datetime.now()
    print(sessionID)
    hours = 5
    minutes =30
    hours_added = datetime.timedelta(hours = hours,minutes=minutes)

    future_date_and_time = current_date_and_time + hours_added

    
    current =str(future_date_and_time)
    print(current)
    
    json= {"TextArea":textarea,"EmailId":Email,"PhoneNumber": PhoneNumber,"timeStamp":current,"SessionID":sessionID,"serviceId":serviceId}
    print(json)
    print("CREATING TICKET ID FOR CUSTOMER")
    result=idgeneration(Email, PhoneNumber,json,serviceId)
    print(result)
    print("STORING DATA IN MONGO DB ")
    store_data=db.insert_one({"EmailId":Email,"PhoneNumber": PhoneNumber,"QueryText":textarea,"timeStamp":current,"SessionID":sessionID,"serviceId":serviceId,"ticketID":result['ticketId'],"paymentUrl":result['url']})
    print(store_data)
    
    return json




@app.post("/webhook/smarti/formdata")
async def humanagentformdata(request:Request):
    form_data=await request.form()
    
    form_data_keys=list(form_data.keys())
    form_data_values=list(form_data.values())
    output_json=dict(zip(form_data_keys, form_data_values))
    current_date_and_time = datetime.datetime.now()
    hours = 5
    minutes =30
    hours_added = datetime.timedelta(hours = hours,minutes=minutes)

    future_date_and_time = current_date_and_time + hours_added

    output_json['Timestamp']=str(future_date_and_time)
    if "Date" in output_json.keys():
        output_json['Scheduled Date']=output_json['Date']
        del output_json['Date']
    current =str(future_date_and_time)
    print(current)
    print("STORING DATA IN MONGO DB ")
    store_data=smartiDb.insert_one(output_json)
    gsheet_upload("1hEBL29S5_VN4ExxyG_bTDz98QUhmBOWw7p1IUX6JMvk","CustomerQuerySheet","smartichatbot")
    return "Done"
    
    
    
    
    
@app.get("/payment/url/{obj}",response_class=HTMLResponse)
async def payment_page(obj:str):
    user_id=obj
    print(obj)
        
    try:
        print(db)
        retrive=db.find_one({"SessionID":str(user_id)})
        print(retrive)
        email=retrive['EmailId']
        phone=retrive['PhoneNumber']
        serviceid=retrive['serviceId']
        print(email,phone,serviceid)
        ticketId=retrive['ticketID']
        paymenturl=retrive["paymentUrl"]
        url= "https://"+paymenturl
        print(url)
        output={"url":url,"email":email,"phoneNumber":phone,"ticketId":ticketId,"serviceId":serviceid}
        print(output)
        
        return dumps(output)
        
    except Exception as e:
        print(str(e))
        url ="https://vakilsearch.com/online-gst-registration"
        json={"url":url} 
        return json





if __name__ == "__main__":

    uvicorn.run("kompose_app:app", host="0.0.0.0", port=int(os.getenv("port")), log_level="info", workers = 2,debug=True)
