from requests.sessions import session
from fastapi import FastAPI, Depends,Form,Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, BaseSettings
from json import dump, loads,dumps
from fastapi import FastAPI, Response, status
import uvicorn
from typing import Any, Dict, AnyStr, List, Union



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



@app.post("/webhook/")
async def root(arbitrary_json: JSONStructure = None):
    input_json={}
    for key ,value in arbitrary_json.items():
        input_json[key.decode("utf-8")]=value
    

    print(input_json)

    output=       [{
            "message": "A message can be simple as a plain text" 
        }, {
            "message": "A message can be a rich message containing metadata",
            "metadata": {
            "contentType": "300",
                "templateId": "6",
                "payload": [{
                    "title": "Suggested Reply button 1",
                    "message": "Suggested Reply button 1",
                }, {
                    "title": "Suggested Reply button 2",
                    "message": "Suggested Reply button 2" 
                }]
            }
        }]
    return output



if __name__ == "__main__":

    uvicorn.run("kompose_app:app", host="0.0.0.0", port=19025, log_level="info", workers = 2,debug=True)