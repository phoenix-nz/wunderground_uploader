"""
Downloads data from weatherman 2 and will return it in a format usable by uploader

Example:
```
    station_ip = 'YOUR STATION IP'
    weather_data = weatherman_get_data(station_ip)
```
"""

# from ast import AsyncFunctionDef
import requests
from datetime import datetime
from datetime import timezone
import json
import traceback

def conv_mySQLDate(rawDate):
    # convert from rawData String yyyy.MM.dd /hh:mm (localTime to 
    # YYYY-MM-DD HH:MM:SS in UT
    date = datetime.strptime(rawDate, "%Y.%m.%d /%Hh%M")
    date = date.astimezone(timezone.utc)
    return date.strftime('%Y-%m-%d %H:%M:%S')

def conv_miles(rawKm):
    # convert from km to miles (or km/h to miles/h)
    miles = 0.621371192 * float(rawKm);
    return miles

def conv_fahrenheit(rawCelcius):
    # convert Celcius to Fahrenheit
    fahrenheit = (1.8 * float(rawCelcius)) + 32.0;
    return fahrenheit

def conv_inch(rawMM):
    # convert mm to inches
    inch = 0.03937 * float(rawMM)
    return inch

def conv_pressureInch(rawPressure):
    # convert millibar to pressure inch?
    psi = 0.0295301 * float(rawPressure)
    return psi

def conv_wattSquareMeter(rawLux):
    # convert lux to w/m²
    watt = 0.0079 * float(rawLux)
    return watt

def convert(raw, config):
    output = dict()
    for item in raw["vars"]:
        if item["homematic_name"] in config["vars"]:
            converter = config["vars"][item["homematic_name"]]
            rawValue = item["value"]
            convValue = 0
            if 'conv' in converter and converter['conv'] is not None:
                if ("conv_" + converter["conv"]) in globals():
                    convValue = globals()["conv_" + converter["conv"]](rawValue)
                else:
                    print("unknown converter " + converter["conv"])
                    convValue = float(rawValue)
            else:
                convValue = float(rawValue)
            output[converter["name"]] = convValue
    for key in config:
        if key != "vars":
            value = config[key]
            convValue = 0
            if isinstance(value, str):
                convValue = value
            elif 'path' in value:
                aPath = value["path"].split("/")
                try:
                    rawValue = raw
                    for j in aPath:
                        rawValue = rawValue[j]    
                except Exception as e:
                    print("Failed to read path from config " + key)
                    print(e)
                    rawValue = None
                if rawValue is not None:
                    convValue = rawValue
                    if ("conv_" + value["conv"]) in globals():
                        convValue = globals()["conv_" + value["conv"]](rawValue)
                    else:
                        print("unknown converter " + value["conv"])
            output[key] = convValue
    
    return output

def weatherman_get_data(station_ip, conf_file):
    """ Pull data from Weatherman 2 Weather station
    will include as much data as possible

    :param station_ip: The weatherman 2 IP address
    """

    data = json.dumps('{}')
    try:
        w_data_raw = requests.get('http://' + station_ip + '/?json')
        if w_data_raw.status_code == 200:
            data = json.loads(w_data_raw.text)
    except Exception as e:
        print("Failed to read data from Weatherman 2")
        print(e)
        return None
    try:
        conf = open(conf_file)
        data_conf = json.load(conf)
        conf.close()
    except Exception as e:
        print("Failed to read config file " + conf_file)
        print(e)
        return None
    
    try:
        convData = convert(data, data_conf)
    except Exception as e:
        print("Conversion failed")
        print(e)
        return None

    return convData
