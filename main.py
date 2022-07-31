from gazpacho import get, Soup
from fastapi import FastAPI
import numpy as np 
import pandas as pd
import requests
import json

app = FastAPI()

@app.get("/pnrcheck")
def pnrCheck(pnr:int):
    url = f"https://paytm.com/train-tickets/pnr-enquiry/{pnr}/-"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    ping = requests.get(url=url,headers=headers)
    soup = Soup(str(ping.content)[2:])
    search = soup.find('div',attrs={'class':'col-xs-7'})
    list_data = search.find('div',attrs={'class':'col-xs-3'})
    text = []
    for item in list_data[4:]:
        text.append(item.text)
    np_array = np.array(text)
    arr_split = np.array_split(np_array,len(text)/4)
    output = []
    for element in arr_split:
        dict_val = {}
        dict_val['Name'] = element[0]
        dict_val['Seat No'] = element[1]
        dict_val['Coach'] = element[2]
        dict_val['Status'] = element[3]
        output.append(dict_val)
    return output