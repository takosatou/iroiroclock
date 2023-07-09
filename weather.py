import datetime
import json
from pprint import pprint
import requests

AREA = 140000
AREA_SUB = 0
URL = f'https://www.jma.go.jp/bosai/forecast/data/forecast/{AREA}.json'

# type
CLEAR = 1
CLOUDY = 2
RAIN = 3
SNOW = 4

# conj
NONE = 0
PARTLY = 1
LATER = 2

# code -> icontype
CODEMAP = {
    100: (CLEAR, NONE, CLEAR),
    101: (CLEAR, PARTLY, CLOUDY),
    102: (CLEAR, PARTLY, RAIN),
    103: (CLEAR, PARTLY, RAIN),
    104: (CLEAR, PARTLY, SNOW),
    105: (CLEAR, PARTLY, SNOW),
    106: (CLEAR, PARTLY, RAIN),
    107: (CLEAR, PARTLY, RAIN),
    108: (CLEAR, PARTLY, RAIN),
    110: (CLEAR, LATER, CLOUDY),
    111: (CLEAR, LATER, CLOUDY),
    112: (CLEAR, LATER, RAIN),
    113: (CLEAR, LATER, RAIN),
    114: (CLEAR, LATER, RAIN),
    115: (CLEAR, LATER, SNOW),
    116: (CLEAR, LATER, SNOW),
    117: (CLEAR, LATER, SNOW),
    118: (CLEAR, LATER, RAIN),
    119: (CLEAR, LATER, RAIN),
    120: (CLEAR, PARTLY, RAIN),
    121: (CLEAR, PARTLY, RAIN),
    122: (CLEAR, LATER, RAIN),
    123: (CLEAR, NONE, CLEAR),
    124: (CLEAR, NONE, CLEAR),
    125: (CLEAR, LATER, RAIN),
    126: (CLEAR, LATER, RAIN),
    127: (CLEAR, LATER, RAIN),
    128: (CLEAR, LATER, RAIN),
    130: (CLEAR, NONE, CLEAR),
    131: (CLEAR, NONE, CLEAR),
    132: (CLEAR, PARTLY, CLOUDY),
    140: (CLEAR, PARTLY, RAIN),
    160: (CLEAR, PARTLY, SNOW),
    170: (CLEAR, PARTLY, SNOW),
    181: (CLEAR, LATER, SNOW),
    200: (CLOUDY, NONE, CLOUDY),
    201: (CLOUDY, PARTLY, CLEAR),
    202: (CLOUDY, PARTLY, RAIN),
    203: (CLOUDY, PARTLY, RAIN),
    204: (CLOUDY, PARTLY, SNOW),
    205: (CLOUDY, PARTLY, SNOW),
    206: (CLOUDY, PARTLY, SNOW),
    207: (CLOUDY, PARTLY, RAIN),
    208: (CLOUDY, PARTLY, RAIN),
    209: (CLOUDY, NONE, CLOUDY),
    210: (CLOUDY, LATER, CLEAR),
    211: (CLOUDY, LATER, CLEAR),
    212: (CLOUDY, LATER, RAIN),
    213: (CLOUDY, LATER, RAIN),
    214: (CLOUDY, LATER, RAIN),
    215: (CLOUDY, LATER, SNOW),
    216: (CLOUDY, LATER, SNOW),
    217: (CLOUDY, LATER, SNOW),
    218: (CLOUDY, LATER, RAIN),
    219: (CLOUDY, LATER, RAIN),
    220: (CLOUDY, PARTLY, RAIN),
    221: (CLOUDY, PARTLY, RAIN),
    222: (CLOUDY, LATER, RAIN),
    223: (CLOUDY, PARTLY, CLEAR),
    224: (CLOUDY, LATER, RAIN),
    225: (CLOUDY, LATER, RAIN),
    226: (CLOUDY, LATER, RAIN),
    228: (CLOUDY, LATER, SNOW),
    229: (CLOUDY, LATER, SNOW),
    230: (CLOUDY, LATER, SNOW),
    231: (CLOUDY, NONE, CLOUDY),
    240: (CLOUDY, PARTLY, RAIN),
    250: (CLOUDY, PARTLY, SNOW),
    260: (CLOUDY, PARTLY, SNOW),
    270: (CLOUDY, PARTLY, SNOW),
    281: (CLOUDY, LATER, SNOW),
    300: (RAIN, NONE, RAIN),
    301: (RAIN, PARTLY, CLEAR),
    302: (RAIN, PARTLY, CLOUDY),
    303: (RAIN, PARTLY, SNOW),
    304: (RAIN, NONE, RAIN),
    306: (RAIN, NONE, RAIN),
    308: (RAIN, NONE, RAIN),
    309: (RAIN, PARTLY, SNOW),
    311: (RAIN, LATER, CLEAR),
    313: (RAIN, LATER, CLOUDY),
    314: (RAIN, LATER, SNOW),
    315: (RAIN, LATER, SNOW),
    316: (RAIN, LATER, CLEAR),
    317: (RAIN, LATER, CLOUDY),
    320: (RAIN, LATER, CLEAR),
    321: (RAIN, LATER, CLOUDY),
    322: (RAIN, PARTLY, SNOW),
    323: (RAIN, LATER, CLEAR),
    324: (RAIN, LATER, CLEAR),
    325: (RAIN, LATER, CLEAR),
    326: (RAIN, LATER, SNOW),
    327: (RAIN, LATER, SNOW),
    328: (RAIN, NONE, RAIN),
    329: (RAIN, NONE, RAIN),
    340: (SNOW, NONE, SNOW),
    350: (RAIN, NONE, RAIN),
    361: (SNOW, LATER, CLEAR),
    371: (SNOW, LATER, CLOUDY),
    400: (SNOW, NONE, SNOW),
    401: (SNOW, PARTLY, CLEAR),
    402: (SNOW, PARTLY, CLOUDY),
    403: (SNOW, PARTLY, RAIN),
    405: (SNOW, NONE, SNOW),
    406: (SNOW, NONE, SNOW),
    407: (SNOW, NONE, SNOW),
    409: (SNOW, PARTLY, RAIN),
    411: (SNOW, LATER, CLEAR),
    413: (SNOW, LATER, CLOUDY),
    414: (SNOW, LATER, RAIN),
    420: (SNOW, LATER, CLEAR),
    421: (SNOW, LATER, CLOUDY),
    422: (SNOW, LATER, RAIN),
    423: (SNOW, LATER, RAIN),
    425: (SNOW, NONE, SNOW),
    426: (SNOW, NONE, SNOW),
    427: (SNOW, NONE, SNOW),
    450: (SNOW, NONE, SNOW),
}

def extract_weather(js):
    today = datetime.datetime.now()
    
    part = js[0]['timeSeries'][0]
    dates = part['timeDefines']
    weathers = part['areas'][AREA_SUB]['weatherCodes']
    for date, weather in zip(reversed(dates), reversed(weathers)):
        d = datetime.datetime.fromisoformat(date)
        if d.month == today.month and d.day == today.day:
            return CODEMAP[int(weather)]
                
    return None


def get_weather():
    try:
        r = requests.get(URL)
        r.raise_for_status()
        js = r.json()
        print(js)
        return extract_weather(js)
    except:
        return None
    
