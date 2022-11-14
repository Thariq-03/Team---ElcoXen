
from fastapi import FastAPI , Response
from pydantic import BaseModel
import pandas as pd
# import requests

STATE = [{"state_code":"S01","state_name":"Andhra Pradesh"},{"state_code":"S02","state_name":"Arunachal Pradesh"},{"state_code":"S03","state_name":"Assam"},{"state_code":"S04","state_name":"Bihar"},{"state_code":"S05","state_name":"Goa"},{"state_code":"S06","state_name":"Gujarat"},{"state_code":"S07","state_name":"Haryana"},{"state_code":"S08","state_name":"Himachal Pradesh"},{"state_code":"U08","state_name":"Jammu and Kashmir"},{"state_code":"S10","state_name":"Karnataka"},{"state_code":"S11","state_name":"Kerala"},{"state_code":"S12","state_name":"Madhya Pradesh"},{"state_code":"S13","state_name":"Maharashtra"},{"state_code":"S14","state_name":"Manipur"},{"state_code":"S15","state_name":"Meghalaya"},{"state_code":"S16","state_name":"Mizoram"},{"state_code":"S17","state_name":"Nagaland"},{"state_code":"S18","state_name":"Odisha"},{"state_code":"S19","state_name":"Punjab"},{"state_code":"S20","state_name":"Rajasthan"},{"state_code":"S21","state_name":"Sikkim"},{"state_code":"S22","state_name":"Tamil Nadu"},{"state_code":"S23","state_name":"Tripura"},{"state_code":"S24","state_name":"Uttar Pradesh"},{"state_code":"S25","state_name":"West Bengal"},{"state_code":"S26","state_name":"Chattisgarh"},{"state_code":"S27","state_name":"Jharkhand"},{"state_code":"S28","state_name":"Uttarakhand"},{"state_code":"S29","state_name":"Telangana"},{"state_code":"U01","state_name":"Andaman \u0026 Nicobar Islands"},{"state_code":"U02","state_name":"Chandigarh"},{"state_code":"U03","state_name":"Dadra \u0026 Nagar Haveli and Daman \u0026 Diu"},{"state_code":"U05","state_name":"NCT OF Delhi"},{"state_code":"U06","state_name":"Lakshadweep"},{"state_code":"U07","state_name":"Puducherry"},{"state_code":"U09","state_name":"Ladakh"}]

# state_code = {"Andhra"}


class char(BaseModel):
    epic : str
    state : str

class Address(BaseModel):
    city: str
    state :str
    area : str

class Voter(BaseModel):
    name : str
    epic : str
    fhm : str
    fhmname : str
    dob : str
    address : Address
    gender : str
    part_no : int
    ac_no : int
    serial_no :int


app = FastAPI()



@app.post('/create')
def create(data:Voter):
    # df = pd.read_csv("data.csv")
    data = {
        "name": data.name,
        "epic": data.epic,
        "fhm":data.fhm,
        "f-h-m-name":data.fhmname,
        "dob" : data.dob,
        "city" : data.address.city,
        "state" : data.address.state,
        "area" : data.address.area,
        "gender" : data.gender,
        "part_no": data.part_no,
        "ac_no" : data.ac_no,
        "serial_no" : data.serial_no
    }

    df = pd.DataFrame(data, index=[0])
    df.to_csv('data.csv', mode='a',index=False,header=False)
    return data


@app.post("/get-family")
def get_tree(EPIC:str,state):
    df = pd.read_csv("data.csv")
    print(df[df['epic']==EPIC])
    return "done"

def get_voter(epic,state_no):
    import requests as r
    data = {
    "txtCaptcha": "VnV5N1",
    "search_type": "epic",
    "reureureired": "ca3ac2c8-4676-48eb-9129-4cdce3adf6ea",
    "epic_no": epic,
    "state": state_no,
    "page_no": 1,
    "results_per_page": 10
    }
    header = { "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Content-Length": "169",
    "Content-Type": "application/json;charset=UTF-8",
    "Cookie": "Electoral=456c656374726f6c7365617263682d73657276657233; runOnce=true; electoralSearchId=ozgndy3etc2xmarbyt3nkdoy; cookiesession1=678B28670E2CCAF5477957CDA6A4F22F; Electoral=456c656374726f6c7365617263682d73657276657233; __RequestVerificationToken=e-VeqqbFfVJSxZ5Bzm_Q1ceGxgj6fOUzGN0ochzJEsKxNELmQarXcJF6yC6ScW0kwbet491UcKgOAtPnmnC5ZMqG6UDdT80pJTFRQhPbZp41",
    "Host": "electoralsearch.in",
    "Origin": "https://electoralsearch.in",
    "Referer": "https://electoralsearch.in/",
    "sec-ch-ua": "Chromium;v=106, Google Chrome;v=10, Not;A=Brand;v=99",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Linux",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }
    r = r.post(url = "https://electoralsearch.in/Home/searchVoter" ,json= data,headers=header)

    # print(r.json())
    return r.json()

def get_state_code(state):
    global STATE
    for i in STATE:
        if i["state_name"] == state:
            return ["state_code"]


@app.post("/proxy")
def proxy(data:char):
    state_code = get_state_code(data.state)
    print(state_code)
    return get_voter(data.epic,state_code)


# get_voter("WJB4082111","22")

