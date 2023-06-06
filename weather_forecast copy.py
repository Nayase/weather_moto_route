"""
OpenWeatherMapから現在の気象データを取得して表示する。
"""
import datetime
import googlemaps
import requests
import json
from pprint import pprint

GOO_API_KEY = "YOUR_API_KEY"
URL_FORMAT = "https://maps.googleapis.com/maps/api/staticmap?center={}"\
    "&zoom={}&size={}&format={}{}&maptype=roadmap"\
    "&key={}"

def get_lat_lon(city_name):
    gmaps = googlemaps.Client(key=GOO_API_KEY)
    
    #出発地の座標を得る
    geocode_result = gmaps.geocode(city_name)
    # for k, v in geocode_result[0].items():
    #     print("key : " + k)
    #     print(v)
    #     print("-" * 10)
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lon = geocode_result[0]["geometry"]["location"]["lng"]
    
    return lat, lon

def get_current_weather(city_name):
    WEA_API_KEY = "YOUR_API_KEY"  
    #api = "http://api.openweathermap.org/data/2.5/weather?units=metric&q={city}&APPID={key}"
    api = "http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API}"
    lat_g, lon_g = get_lat_lon(city_name)
    url = api.format(lat=lat_g,lon = lon_g,API=WEA_API_KEY)

    # 気象情報を取得
    response = requests.get(url).json()
    # APIレスポンスの表示
    #jsonText = json.dumps(response, indent=2)
    
    #pprint(response)
    #print(response["weather"][0]["main"])

    return response

def main():
    dec_time = []
    date_time = []
    weather = []
    departure_time = datetime.datetime.now()
    # 都市を指定する。
    city_name = input("都市名を入力してください:")
    response = get_current_weather(city_name)
    pprint(response)
    #各地の天気予報の表示
    for i in range(40):
        date_time.append(response['list'][i]['dt_txt'])
        weather.append(response['list'][i]['weather'][0]['description']) 
        dec_time.append(datetime.datetime.strptime(date_time[i], '%Y-%m-%d %H:%M:%S') - departure_time)
        print("date_time = ", date_time[i])
        print("date_time - now = ", dec_time[i])
        print(weather[i])
    #指定した時間に一番近い天気の表示を行う．
    for i in range(40):
        dec_time[i] = abs(dec_time[i])
        
    ans_index = dec_time.index(min(dec_time))
    print("now_weather = ", weather[ans_index])
    

if __name__ == "__main__":
    main()