"""
Downloads data from weatherman 2 and will return it in a format usable by uploader

Example:
```
    station_ip = 'YOUR STATION IP'
    weather_data = weatherman_get_data(station_ip)
```
"""

import requests
import datetime
import json

dict_keys = {
    "w_temperatur": { 
        "name": "tempf", 
        "conv": "fahrenheit"
    },
    "w_windchill": { 
        "name": "tempf", 
        "conv": "fahrenheit"
    }
""""
https://support.weather.com/s/article/PWS-Upload-Protocol?language=en_US
{"modultyp":"weatherman","vars":[{"name":"0","homematic_name":"w_ip","desc":"weatherman_ip","type":"string","unit":"","value":"192.168.2.130"},{"name":"1","homematic_name":"w_temperatur","desc":"aussentemperatur","type":"number","unit":"gradC","value":"11.1"},{"name":"21","homematic_name":"w_windchill","desc":"gefuehlte_temperatur","type":"number","unit":"gradC","value":"11.1"},{"name":"9","homematic_name":"w_taupunkt","desc":"taupunkt_temperatur","type":"number","unit":"gradC","value":"10.9"},{"name":"14","homematic_name":"w_himmeltemperatur","desc":"himmel_temperatur","type":"number","unit":"gradC","value":"0.0"},{"name":"2","homematic_name":"w_feuchte_rel","desc":"rel_feuchte","type":"number","unit":"%","value":"99.0"},{"name":"17","homematic_name":"w_feuchte_abs","desc":"abs_feuchte","type":"number","unit":"g/m3","value":"10.0"},{"name":"18","homematic_name":"w_regensensor_wert","desc":"regenmelderwert","type":"number","unit":"","value":"0"},{"name":"7","homematic_name":"w_regenmelder","desc":"regenstatus","type":"boolean","unit":"","value":"false"},{"name":"8","homematic_name":"w_regenstaerke","desc":"regenstaerke","type":"number","unit":"mm/h","value":"0.0"},{"name":"19","homematic_name":"w_regen_letzte_h","desc":"regen_pro_h","type":"number","unit":"mm","value":"0.0"},{"name":"20","homematic_name":"w_regen_mm_heute","desc":"regen_mm_heute","type":"number","unit":"mm","value":"0.0"},{"name":"32","homematic_name":"w_regenstunden_heute","desc":"regenstunden_heute","type":"number","unit":"h","value":"0.0"},{"name":"27","homematic_name":"w_regen_mm_gestern","desc":"regen_mm_gestern","type":"number","unit":"mm","value":"1.0"},{"name":"3","homematic_name":"w_barometer","desc":"nn_luftdruck","type":"number","unit":"mb","value":"1005.57"},{"name":"11","homematic_name":"w_barotrend","desc":"luftdrucktrend","type":"string","unit":"","value":"stabil"},{"name":"4","homematic_name":"w_wind_mittel","desc":"avg_windgeschwindigkeit","type":"number","unit":"km/h","value":"0.0"},{"name":"5","homematic_name":"w_wind_spitze","desc":"peak_windgeschwindigkeit","type":"number","unit":"km/h","value":"0.0"},{"name":"24","homematic_name":"w_windstaerke","desc":"bft_windgeschwindigkeit","type":"number","unit":"bft","value":"0"},{"name":"23","homematic_name":"w_windrichtung","desc":"windrichtung","type":"string","unit":"","value":"NW"},{"name":"6","homematic_name":"w_wind_dir","desc":"windwinkel","type":"number","unit":"grad","value":"315"},{"name":"10","homematic_name":"w_lux","desc":"helligkeit","type":"number","unit":"lux","value":"0.0"},{"name":"28","homematic_name":"w_uv_index","desc":"uv-index","type":"number","unit":"uv_index","value":"0.000"},{"name":"22","homematic_name":"w_sonne_diff_temp","desc":"sonnen_difftemperatur","type":"number","unit":"gradC","value":"0.0"},{"name":"15","homematic_name":"w_sonnentemperatur","desc":"sonnen_temperatur","type":"number","unit":"gradC","value":"0.0"},{"name":"16","homematic_name":"w_sonne_scheint","desc":"sonne_scheint","type":"boolean","unit":"","value":"false"},{"name":"26","homematic_name":"w_sonnenstunden_heute","desc":"Sonnenstunden_heute","type":"number","unit":"h","value":"0.0"},{"name":"12","homematic_name":"w_elevation","desc":"sonne_elevation","type":"number","unit":"grad","value":"-35.6"},{"name":"13","homematic_name":"w_azimut","desc":"sonne_azimut","type":"number","unit":"grad","value":"5.5"},{"name":"30","homematic_name":"w_minuten_vor_sa","desc":"minuten_vor_sa","type":"number","unit":"min","value":"325"},{"name":"31","homematic_name":"w_minuten_vor_su","desc":"minuten_vor_su","type":"number","unit":"min","value":"1079"}],"Systeminfo":{"MAC-Adresse":"84:cc:a8:9f:a4:03","Homematic_CCU_ip":"192.168.2.250","WLAN_ssid":"phoenix-wlan","WLAN_Signal_dBm":"-59","sec_seit_reset":"81041","zeitpunkt":"2022.09.15 /01h30","firmware":"wm2_25_2"}}
action [action=updateraw] -- always supply this parameter to indicate you are making a weather observation upload
ID [ID as registered by wunderground.com]
PASSWORD [Station Key registered with this PWS ID, case sensitive]
dateutc - [YYYY-MM-DD HH:MM:SS (mysql format)] In Universal Coordinated Time (UTC) Not local time
winddir - [0-360 instantaneous wind direction]
windspeedmph - [mph instantaneous wind speed]
windgustmph - [mph current wind gust, using software specific time period]
windgustdir - [0-360 using software specific time period]
windspdmph_avg2m  - [mph 2 minute average wind speed mph]
winddir_avg2m - [0-360 2 minute average wind direction]
windgustmph_10m - [mph past 10 minutes wind gust mph ]
windgustdir_10m - [0-360 past 10 minutes wind gust direction]
humidity - [% outdoor humidity 0-100%]
dewptf- [F outdoor dewpoint F]
tempf - [F outdoor temperature]
* for extra outdoor sensors use temp2f, temp3f, and so on
rainin - [rain inches over the past hour)] -- the accumulated rainfall in the past 60 min
dailyrainin - [rain inches so far today in local time]
baromin - [barometric pressure inches]
weather - [text] -- metar style (+RA)
clouds - [text] -- SKC, FEW, SCT, BKN, OVC
soiltempf - [F soil temperature]
* for sensors 2,3,4 use soiltemp2f, soiltemp3f, and soiltemp4f
soilmoisture - [%]
* for sensors 2,3,4 use soilmoisture2, soilmoisture3, and soilmoisture4
leafwetness  - [%]
+ for sensor 2 use leafwetness2
solarradiation - [W/m^2]
UV - [index]
visibility - [nm visibility]
indoortempf - [F indoor temperature F]
indoorhumidity - [% indoor humidity 0-100]
softwaretype - [text] ie: WeatherLink, VWS, WeatherDisplay
"""
}

def weatherman_get_data(station_ip):
    """ Pull data from Weatherman 2 Weather station
    will include as much data as possible

    :param station_ip: The weatherman 2 IP address
    """

    try:
        w_data_raw = requests.get(station_ip + '/?json')
        if w_data_raw.status_code == 200:
            w_data_conv = convert(w_data_raw.text())
    except Exception:
        print("Failed to read data from Weatherman 2")
    
def convert(w_data_raw):
    data = json.loads(w_data_raw)
    w_data_conv = dict()
    for var in data["vars"]:
        if data["vars"][var]["homematic_name"]
        w_data_conv[]

  


if __name__ == '__main__':
    station_id = 'YOUR STATION ID HERE'
    station_key = 'YOUR STATION KEY HERE'
    weather_data = dict(
        tempf=47.84,
        humidity=94.0
    )
    utc_timestamp = 1579559564
    wunderground_upload_data_point(station_id, station_key, weather_data, utc_timestamp)
