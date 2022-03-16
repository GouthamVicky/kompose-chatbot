from requests.sessions import session
from capsule_response import lead_form_collection
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



    if intent_name.lower()=="i have other questions" or str(intent_number)=="623094b838b63d0fcc232800":
        message=lead_form_collection(session_id)
        return output

    


@app.post("/store/user/details/incorp")
async def session_predict(Email: str = Form(...),PhoneNumber: str = Form(...),sessionID: str = Form(...)):
    current_date_and_time = datetime.datetime.now()
    print(sessionID)
    hours = 5
    minutes =30
    hours_added = datetime.timedelta(hours = hours,minutes=minutes)

    future_date_and_time = current_date_and_time + hours_added

    
    current =str(future_date_and_time)
    print(current)
    print("STORING DATA IN MONGO DB ")
    json= {"EmailId":Email,"PhoneNumber": PhoneNumber,"timeStamp":current,"SessionID":sessionID,"serviceId":1}
    store_data=db.insert_one({"EmailId":Email,"PhoneNumber": PhoneNumber,"timeStamp":current,"SessionID":sessionID,"serviceId":serviceId})
    print(json)
    
    return json



if __name__ == "__main__":

    uvicorn.run("kompose_app:app", host="0.0.0.0", port=19025, log_level="info", workers = 2,debug=True)