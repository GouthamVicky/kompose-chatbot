import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

url = os.getenv('lead_creation_url')
print(url)

def idgeneration(email,phone,obj,service_id):

  
  payload = json.dumps({
    "name": "",
    "email":email,
    "contact_number": phone,
    "city_id": "1",
    "service_id": str(service_id),
    "source_data": {
      "utmz_data": "",
      "utmb_data": "",
      "utma_data": ""
    },
    "ticket_source_id": 110,
    "selfserve_source": "Inkorporate",
    "source_name": obj.get("utm_source",""),
    "medium_name": obj.get("utm_medium",""),
    "campaign_name": obj.get("utm_campaign",""),
    "content_name": obj.get("utm_content",""),
    "campaign_id": obj.get("Campaignid",""),
    "adgroupid": obj.get("Adgroupid",""),
    "utm_term": obj.get("utm_term",""),
    "device": obj.get("device",""),
    "adposition": obj.get("Adposition",""),
    "physical": obj.get("physical",""),
    "match_type": obj.get("match_type",""),
    "gclid": obj.get("gclid",""),
    "network": obj.get("network",""),
    "target_name": obj.get("target_name",""),
    "placement": obj.get("placement",""),
    "keyword_id": obj.get("keyword_id",""),
    "referrer_url": obj.get("referrer_url",""),
    "consult_form": False,
    "freeconsultation": False,
    "googleAdwords": "",
    "is_prime": False,
    "business_calculator": "",
    "business_loan": ""
  })
  headers = {
    'X-Requested-With': 'XMLHttpRequest\'',
    'Content-Type': 'application/json',
    'key': 'e7e7a52397d57a5cd126328db7793009',
    'token': 'tPiz9vb0vGxATzEEsNciEsPf9GRNcNp6'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  result=json.loads(response.text)
  print(result)

  try:

    if result['data']['ticket']['id']:
      print("=========>NEW TICKET ID GENERATED<============")
      ticketId=result['data']['ticket']['id']
      magickey=result['data']['ticket_magic_key']
  except Exception as e:
    print(str(e))
    pass
  try:

    if result['data']['ticket']['ticket_details']['ticketId']:
      print("========>DUPLICATE TICKET ID <=========")
      ticketId=result['data']['ticket']['ticket_details']['ticketId']
      magickey=result['data']['ticket']['ticket_details']['magickey']
  except Exception as e:
    print(str(e))
    pass

  print(ticketId)
  print(magickey)
  paymentlandingpage=os.getenv('Paymenturl')+str(magickey)
  print(paymentlandingpage)
  result={"ticketId":ticketId,"url":paymentlandingpage}
  return result



