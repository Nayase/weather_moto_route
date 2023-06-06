"""
経路の天気を表示するプログラム
# python bike_weather_app.py 10:00(出発時刻) 仙台(出発地) 石巻(到着地) ・・・
"""
import datetime
from fnmatch import translate
import googlemaps
import urllib.request, json
import urllib.parse
import datetime
import requests
import json
from pprint import pprint

ENDPOINT = 'https://maps.googleapis.com/maps/api/directions/json?'
ENDPOINT2 = 'https://maps.googleapis.com/maps/api/geocode/json?'
WEA_API_KEY = "YOUR_API_KEY" 
GOO_API_KEY = "YOUR_API_KEY"
URL_FORMAT = "https://maps.googleapis.com/maps/api/staticmap?center={}"\
    "&zoom={}&size={}&format={}{}&maptype=roadmap"\
    "&key={}"

def get_route(origin_lat, origin_lng, destination_lat, destination_lng, travel_mode, avoid, unix_time):
    
    nav_request = 'language=en&origin={},{}&destination={},{}&avoid={}&mode={}&departure_time={}&key={}'.format(origin_lat,origin_lng,destination_lat,destination_lng,avoid,travel_mode,unix_time,GOO_API_KEY)
    nav_request = urllib.parse.quote_plus(nav_request, safe='=&')
    request = ENDPOINT + nav_request

    #Google Maps Platform Directions APIを実行
    response = urllib.request.urlopen(request).read()
    directions = json.loads(response)
    
    half_len = int(len(directions['routes'][0]['legs'][0]['steps'])/2)
    #道のりの半分の位置を割り出し，天気を求める
    half_lat = directions['routes'][0]['legs'][0]['steps'][half_len-1]['end_location']['lat']
    half_lng = directions['routes'][0]['legs'][0]['steps'][half_len-1]['end_location']['lng']
    
    

    for key in directions['routes']:
        for key2 in key['legs']:
            duration = datetime.datetime.utcfromtimestamp(key2['duration']['value'])
    
    return half_lat, half_lng, duration

def get_lat_lon(city_name):
    gmaps = googlemaps.Client(key=GOO_API_KEY)
    
    #出発地の座標を得る
    geocode_result = gmaps.geocode(city_name)

    for i in range(len(geocode_result)):
        judge = geocode_result[i]['address_components'][len(geocode_result[i]['address_components'])-1]['long_name'] == 'Japan' or geocode_result[i]['address_components'][len(geocode_result[i]['address_components'])-2]['long_name'] == 'Japan'
        if judge:
            lat = geocode_result[i]['geometry']['location']['lat']
            lon = geocode_result[i]['geometry']['location']['lng']
    
    return lat, lon

def get_place(lat, lng):
    nav_request = 'language=ja&latlng={},{}&key={}'.format(lat,lng,GOO_API_KEY)
    nav_request = urllib.parse.quote_plus(nav_request, safe='=&')
    request = ENDPOINT2 + nav_request

    #Google Maps Platform Directions APIを実行
    response = urllib.request.urlopen(request).read()
    pre_place = json.loads(response)
    print("ぷりんと:")
    pprint(pre_place['results'][0])
    address_len = len(pre_place['results'][0]['address_components'])
    for i in range(len(pre_place['results'][0]['address_components'])):
        if pre_place['results'][0]['address_components'][i]['types'][0] == 'country':
            city = pre_place['results'][0]['address_components'][i - 2]['long_name']
    
            prefecture = pre_place['results'][0]['address_components'][i - 1]['long_name']
    
    
    
    return city, prefecture


def translate_weather(id):
    #id:200番台(雷雨)
    if id == 200:
        jp = "雷雨"
    elif id == 201:
        jp = "雷雨"
    elif id == 202:
        jp = "雷雨"
    elif id == 210:
        jp = "弱い雷雨"
    elif id == 211:
        jp = "雷雨"
    elif id == 212:
        jp = "激しい雷雨"
    elif id == 221:
        jp = "雷雨"
    elif id == 230:
        jp = "小雨混じりの雷雨"
    elif id == 231:
        jp = "雷雨"
    elif id == 232:
        jp = "激しい雷雨"
    #id:300番台(小雨)
    elif id == 300:
        jp = "小雨"
    elif id == 301:
        jp = "小雨"
    elif id == 302:
        jp = "小雨"
    elif id == 310:
        jp = "小雨"
    elif id == 311:
        jp = "小雨"
    elif id == 312:
        jp = "小雨"
    elif id == 313:
        jp = "時雨"
    elif id == 314:
        jp = "時雨"
    elif id == 321:
        jp = "時雨"
    #id:500番台(雨)
    elif id == 500:
        jp = "弱い雨"    
    elif id == 501:
        jp = "雨"
    elif id == 502:
        jp = "一時的に強い雨"
    elif id == 503:
        jp = "強い雨"
    elif id == 504:
        jp = "強い雨"
    elif id == 511:
        jp = "みぞれ"
    elif id == 520:
        jp = "雨"
    elif id == 521:
        jp = "雨"
    elif id == 522:
        jp = "雨"
    elif id == 531:
        jp = "雨"   
    #id:600番台(雪)
    elif id == 600:
        jp = "弱い雪"
    elif id == 601:
        jp = "雪"
    elif id == 602:
        jp = "大雪"
    elif id == 611:
        jp = "みぞれ"
    elif id == 612:
        jp = "みぞれ"
    elif id == 613:
        jp = "みぞれ"
    elif id == 615:
        jp = "みぞれ"
    elif id == 616:
        jp = "雨混じりの雪"
    elif id == 620:
        jp = "雪"
    elif id == 621:
        jp = "雪"
    elif id == 622:
        jp = "雪"
    #id:700番台(霧)
    elif id == 701:
        jp = "霧"
    elif id == 711:
        jp = "煙"
    elif id == 721:
        jp = "霞"
    elif id == 731:
        jp = "砂塵旋風"
    elif id == 741:
        jp = "濃霧"
    elif id == 751:
        jp = "黄砂"
    elif id == 761:
        jp = "埃"
    elif id == 762:
        jp = "火山灰"
    elif id == 771:
        jp = "突風"
    elif id == 781:
        jp = "トルネード"
    #id:800番台(晴れ)
    elif id == 800:
        jp = "快晴"
    #id:900番台(曇り)
    elif id == 801:
        jp = "晴れ時々曇り"
    elif id == 802:
        jp = "曇り時々晴れ"
    elif id == 803:
        jp = "曇り時々晴れ"
    elif id == 804:
        jp = "曇り"
    
    return jp

def get_current_weather(city_name):
    api = "http://api.openweathermap.org/data/2.5/forecast?lat={lat_a}&lon={lon_a}&appid={API}"
    
    lat_g, lon_g = get_lat_lon(city_name)
    url = api.format(lat_a=lat_g,lon_a = lon_g,API=WEA_API_KEY)
    
    # 気象情報を取得
    response = requests.get(url).json()

    return response
        

def dl_image(filename, img_format, url):
    file_name = "{}.{}".format(filename, img_format[:3])
    res = requests.get(url)
    if res.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(res.content)
    else:
        print("失敗")


def make_url(lat, lng, zoom, size, img_format, custom_icon):
    location = "{},{}".format(lat, lng)
    size_param = "{}x{}".format(*size)
    if custom_icon is None:
        icon_param = ""
    else:
        icon_param = "&markers=icon:{}|{}".format(custom_icon, location)
    url = URL_FORMAT.format(
        location, zoom, size_param, img_format, icon_param, GOO_API_KEY)
    return url


def get_map_image(
        place, zoom, size=(600, 300), img_format="png",
        custom_icon=None, filename=None):
    """
    place : 場所\n
    zoom  : 1)世界 5)大陸 10)市 15)通り 20)建物\n
    size  : (width, height) 最大 640x640\n
    img_format : png(png8), png32, gif, jpg, jpg-baseline\n
    custom_icon : IconのURL
    """
    gmaps = googlemaps.Client(key=GOO_API_KEY)
    geocode_result = gmaps.geocode(place)

    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lng = geocode_result[0]["geometry"]["location"]["lng"]
    url = make_url(lat, lng, zoom, size, img_format, custom_icon)
    if filename is None:
        filename = place
    dl_image(filename, img_format, url)

def main():
    
    dec_time = []
    dec_time_1 = []
    dec_time_2 = []
    date_time = []
    weather = []
    date_time_1 = []
    weather_1 = []
    date_time_2 = []
    weather_2 = []
    
    # 都市を指定する。
    city_name = input("出発地を入力してください:")
    destination_name = input("目的地を入力してください:")
    pre_departure_time = input("出発時刻を入力してください(YYYY/MM/DD hh:mm):")
    departure_time = datetime.datetime.strptime(pre_departure_time, '%Y/%m/%d %H:%M')
    
    unix_time = int(departure_time.timestamp())

    #移動手段決定
    travel_mode_flag = input('移動手段: 1:車,2:徒歩').replace(' ','+')

    global travel_mode
    if travel_mode_flag == "1":
        travel_mode = "driving"
    elif travel_mode_flag == "2": 
        travel_mode = "walking"
    else:
        print("error")

    if travel_mode == "driving":
        #高速使うかの分岐
        avoid_highway = input('高速を使いますか?: 1:使う 2:使わない').replace(' ','+')
        global avoid
        if avoid_highway == "1":
            avoid = None
        #高速道路を回避するので，2を選んだ場合にavoidに"highways"を代入する.
        elif avoid_highway == "2": 
            avoid = "highways"
        else:
            print("error")
    else:
        avoid = None
        
    origin_lat, origin_lng = get_lat_lon(city_name)
    destination_lat, destination_lng = get_lat_lon(destination_name)
        
    middle_lat, middle_lng, move_time = get_route(origin_lat, origin_lng, destination_lat, destination_lng, travel_mode, avoid, unix_time)
    
    mm_lat, mm_lng, middle_move_time = get_route(origin_lat, origin_lng, middle_lat, middle_lng, travel_mode, avoid, unix_time)
    prefecture, middle_city = get_place(middle_lat, middle_lng)
    
    middle_time = departure_time + datetime.timedelta(hours=middle_move_time.hour, minutes=middle_move_time.minute)
    arrive_time = departure_time + datetime.timedelta(hours=move_time.hour, minutes=move_time.minute)
    
    response = get_current_weather(city_name)
    response_1 = get_current_weather(middle_city)
    response_2 = get_current_weather(destination_name)
    #各地の天気予報の表示
    for i in range(40):
        date_time.append(response['list'][i]['dt_txt'])
        weather.append(response['list'][i]['weather'][0]['id']) 
        date_time_1.append(response_1['list'][i]['dt_txt'])
        weather_1.append(response_1['list'][i]['weather'][0]['id']) 
        date_time_2.append(response_2['list'][i]['dt_txt'])
        weather_2.append(response_2['list'][i]['weather'][0]['id'])         
        dec_time.append(datetime.datetime.strptime(date_time[i], '%Y-%m-%d %H:%M:%S') - departure_time)
        dec_time_1.append(datetime.datetime.strptime(date_time[i], '%Y-%m-%d %H:%M:%S') - middle_time)
        dec_time_2.append(datetime.datetime.strptime(date_time_2[i], '%Y-%m-%d %H:%M:%S') - arrive_time)

    #指定した時間に一番近い天気の表示を行う．
    for i in range(40):
        dec_time[i] = abs(dec_time[i])
        dec_time_1[i] = abs(dec_time_1[i])
        dec_time_2[i] = abs(dec_time_2[i])
        
    ans_index = dec_time.index(min(dec_time))
    ans1_index = dec_time_1.index(min(dec_time_1))
    ans2_index = dec_time_2.index(min(dec_time_2))
    
    jp_weather = translate_weather(weather[ans_index])
    jp1_weather = translate_weather(weather_1[ans1_index])
    jp2_weather = translate_weather(weather_2[ans2_index])
    
    print(f"{city_name} の天気: {jp_weather}")
    print(f"{prefecture},{middle_city} の天気: {jp1_weather}")
    print(f"{destination_name} の天気: {jp2_weather}")


if __name__ == "__main__":
    main()