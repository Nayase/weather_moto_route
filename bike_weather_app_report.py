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
WEA_API_KEY = "7fbaaa87096b13d72001396daaf8825e" 
GOO_API_KEY = "AIzaSyCRJeZTodQ3sfwKMshfcVC7YoPHmIAGVDg"
# WEA_API_KEY = "あなたのOpen Weather MapのAPI Keyを入力してください" 
# GOO_API_KEY = "あなたのGoogle Cloud PlatformのAPI Keyを入力してください"
URL_FORMAT = "https://maps.googleapis.com/maps/api/staticmap?center={}"\
    "&zoom={}&size={}&format={}{}&maptype=roadmap"\
    "&path={}"\
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
            duration = key2['duration']['value']
    
    return half_lat, half_lng, duration, directions

def get_lat_lon(city_name):
    gmaps = googlemaps.Client(key=GOO_API_KEY)
    
    #出発地の座標を得る
    geocode_result = gmaps.geocode(city_name)
    # pprint(geocode_result)
    # pprint(geocode_result[0])
    for i in range(len(geocode_result)):
        judge = geocode_result[i]['address_components'][len(geocode_result[i]['address_components'])-1]['long_name'] == 'Japan' or geocode_result[i]['address_components'][len(geocode_result[i]['address_components'])-2]['long_name'] == 'Japan'
        if judge:
            lat = geocode_result[i]['geometry']['location']['lat']
            lon = geocode_result[i]['geometry']['location']['lng']
        
    # pprint(geocode_result[0]['geometry'])
    # for k, v in geocode_result[0].items():
    #     print("key : " + k)
    #     print(v)
    #     print("-" * 10)
    
    return lat, lon

def get_place(lat, lng):
    nav_request = 'language=ja&latlng={},{}&key={}'.format(lat,lng,GOO_API_KEY)
    nav_request = urllib.parse.quote_plus(nav_request, safe='=&')
    request = ENDPOINT2 + nav_request

    #Google Maps Platform Directions APIを実行
    response = urllib.request.urlopen(request).read()
    #print(response)
    pre_place = json.loads(response)
    #pprint(pre_place)
    # print("ぷりんと:")
    # pprint(pre_place['results'][0])
    for i in range(len(pre_place['results'][0]['address_components'])):
        if pre_place['results'][0]['address_components'][i]['types'][0] == 'country':
            city = pre_place['results'][0]['address_components'][i - 1]['long_name']
    
            prefecture = pre_place['results'][0]['address_components'][i - 2]['long_name']
    
    return city, prefecture


def translate_weather(id):
    #id:200番台(雷雨)
    if id == 200:
        jp = "雷雨"
        icon = "11d"
    elif id == 201:
        jp = "雷雨"
        icon = "11d"
    elif id == 202:
        jp = "雷雨"
        icon = "11d"
    elif id == 210:
        jp = "弱い雷雨"
        icon = "11d"
    elif id == 211:
        jp = "雷雨"
        icon = "11d"
    elif id == 212:
        jp = "激しい雷雨"
        icon = "11d"
    elif id == 221:
        jp = "雷雨"
        icon = "11d"
    elif id == 230:
        jp = "小雨混じりの雷雨"
        icon = "11d"
    elif id == 231:
        jp = "雷雨"
        icon = "11d"
    elif id == 232:
        jp = "激しい雷雨"
        icon = "11d"
    #id:300番台(小雨)
    elif id == 300:
        jp = "小雨"
        icon = "09d"
    elif id == 301:
        jp = "小雨"
        icon = "09d"
    elif id == 302:
        jp = "小雨"
        icon = "09d"
    elif id == 310:
        jp = "小雨"
        icon = "09d"
    elif id == 311:
        jp = "小雨"
        icon = "09d"
    elif id == 312:
        jp = "小雨"
        icon = "09d"
    elif id == 313:
        jp = "時雨"
        icon = "09d"
    elif id == 314:
        jp = "時雨"
        icon = "09d"
    elif id == 321:
        jp = "時雨"
        icon = "09d"
    #id:500番台(雨)
    elif id == 500:
        jp = "弱い雨"  
        icon = "10d"  
    elif id == 501:
        jp = "雨"
        icon = "10d" 
    elif id == 502:
        jp = "一時的に強い雨"
        icon = "10d" 
    elif id == 503:
        jp = "強い雨"
        icon = "10d" 
    elif id == 504:
        jp = "強い雨"
        icon = "10d" 
    elif id == 511:
        jp = "みぞれ"
        icon = "13d" 
    elif id == 520:
        jp = "雨"
        icon = "09d" 
    elif id == 521:
        jp = "雨"
        icon = "09d" 
    elif id == 522:
        jp = "雨"
        icon = "09d" 
    elif id == 531:
        jp = "雨"  
        icon = "09d"  
    #id:600番台(雪)
    elif id == 600:
        jp = "弱い雪"
        icon = "13d" 
    elif id == 601:
        jp = "雪"
        icon = "13d" 
    elif id == 602:
        jp = "大雪"
        icon = "13d" 
    elif id == 611:
        jp = "みぞれ"
        icon = "13d" 
    elif id == 612:
        jp = "みぞれ"
        icon = "13d" 
    elif id == 613:
        jp = "みぞれ"
        icon = "13d" 
    elif id == 615:
        jp = "みぞれ"
        icon = "13d" 
    elif id == 616:
        jp = "雨混じりの雪"
        icon = "13d" 
    elif id == 620:
        jp = "雪"
        icon = "13d" 
    elif id == 621:
        jp = "雪"
        icon = "13d" 
    elif id == 622:
        jp = "雪"
        icon = "13d" 
    #id:700番台(霧)
    elif id == 701:
        jp = "霧"
        icon = "50d" 
    elif id == 711:
        jp = "煙"
        icon = "50d" 
    elif id == 721:
        jp = "霞"
        icon = "50d" 
    elif id == 731:
        jp = "砂塵旋風"
        icon = "50d" 
    elif id == 741:
        jp = "濃霧"
        icon = "50d" 
    elif id == 751:
        jp = "黄砂"
        icon = "50d" 
    elif id == 761:
        jp = "埃"
        icon = "50d" 
    elif id == 762:
        jp = "火山灰"
        icon = "50d" 
    elif id == 771:
        jp = "突風"
        icon = "50d" 
    elif id == 781:
        jp = "トルネード"
        icon = "50d" 
    #id:800番台(晴れ)
    elif id == 800:
        jp = "快晴"
        icon = "01d" 
    #id:900番台(曇り)
    elif id == 801:
        jp = "晴れ時々曇り"
        icon = "02d" 
    elif id == 802:
        jp = "曇り時々晴れ"
        icon = "03d" 
    elif id == 803:
        jp = "曇り時々晴れ"
        icon = "04d" 
    elif id == 804:
        jp = "曇り"
        icon = "04d" 
    
    return jp, icon

def get_current_weather(city_name):
    api = "http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API}"
    lat_g, lon_g = get_lat_lon(city_name)
    url = api.format(lat=lat_g,lon = lon_g,API=WEA_API_KEY)

    # 気象情報を取得
    response = requests.get(url).json()
    # APIレスポンスの表示
    # jsonText = json.dumps(response, indent=2)

    return response
        

def dl_image(filename, img_format, url):
    file_name = "{}.{}".format(filename, img_format[:3])
    res = requests.get(url)
    if res.status_code == 200:
        with open(f"./templates/map_data/{file_name}", "wb") as f:
            f.write(res.content)
            f.close()
    else:
        print("失敗")
    return file_name


def make_url(lat, lng, path, departure_icon,middle_icons,destination_icon, zoom, size, img_format, custom_icon):
    location = "{},{}".format(lat, lng)
    size_param = "{}x{}".format(*size)
    icon_param = "&markers=icon:{}|{}".format(f"https://openweathermap.org/img/wn/{departure_icon[2]}.png", f"{departure_icon[0]},{departure_icon[1]}")
    for i in range(len(middle_icons)):
        icon_param += "&markers=icon:{}|{}".format(f"http://openweathermap.org/img/wn/{middle_icons[i][2]}.png", f"{middle_icons[i][0]},{middle_icons[i][1]}")
    icon_param += "&markers=icon:{}|{}".format(f"http://openweathermap.org/img/wn/{destination_icon[2]}.png", f"{destination_icon[0]},{destination_icon[1]}")
    # print(icon_param)
    url = URL_FORMAT.format(
        location, zoom, size_param, img_format, icon_param, path, GOO_API_KEY)
    return url


def get_map_image(
        place, zoom, path, departure_icon, middle_icons, destination_icon, size=(640, 640), img_format="png",
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
    # for k, v in geocode_result[0].items():
    #     print("key : " + k)
    #     print(v)
    #     print("-" * 10)

    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lng = geocode_result[0]["geometry"]["location"]["lng"]
    # path = f"color:0x0000ff|weight:5|{lat},{lng}|38.259834,140.882184"
    url = make_url(lat, lng, path, departure_icon,middle_icons,destination_icon, zoom, size, img_format, custom_icon)
    if filename is None:
        filename = datetime.datetime.now()
    # print(url)
    save_filename = dl_image(filename, img_format, url)
    return url

def local_weather(city_name, destination_name, departure_time, travel_mode, avoid):
    
    dec_time = []
    dec_time_1 = []
    dec_time_2 = []
    date_time = []
    weather = []
    date_time_1 = []
    weather_1 = []
    date_time_2 = []
    weather_2 = []
    
    unix_time = int(departure_time.timestamp())
        
    origin_lat, origin_lng = get_lat_lon(city_name)
    destination_lat, destination_lng = get_lat_lon(destination_name)
        
    middle_lat, middle_lng, move_time, directions = get_route(origin_lat, origin_lng, destination_lat, destination_lng, travel_mode, avoid, unix_time)
    
    distance = directions['routes'][0]['legs'][0]['distance']['value']
    #距離に応じて中間地点を増やす条件分岐
    if distance < 10000:
        culc_time = 0
    elif distance >= 10000 and distance < 200000:
        culc_time = 1
    elif distance >= 200000:
        culc_time = 2
    
    middle_time_set = []
    prefecture_set = []
    middle_city_set = []
    middle_city_lat_lng = []
    
    if culc_time == 0:
        middle_city_set.append(destination_name)
    if culc_time > 0:
        mm_lat, mm_lng, middle_move_time, directions_2 = get_route(origin_lat, origin_lng, middle_lat, middle_lng, travel_mode, avoid, unix_time)
        prefecture, middle_city = get_place(middle_lat, middle_lng)
        middle_time_set.append(datetime.datetime.utcfromtimestamp(middle_move_time))
        prefecture_set.append(prefecture)
        middle_city_set.append(middle_city)
        middle_city_lat_lng.append([middle_lat, middle_lng])
    if culc_time > 1:
        mm_lat2, mm_lng2, middle_move_time2, directions_3 = get_route(middle_lat, middle_lng, destination_lat, destination_lng, travel_mode, avoid, unix_time+middle_move_time)
        mm_lat3, mm_lng3, middle_move_time3, directions_4 = get_route(origin_lat, origin_lng, mm_lat, mm_lng, travel_mode, avoid, unix_time)
        mm_lat4, mm_lng4, middle_move_time4, directions_5 = get_route(origin_lat, origin_lng, mm_lat2, mm_lng2, travel_mode, avoid, unix_time)
        prefecture2, middle_city2 = get_place(mm_lat, mm_lng)
        prefecture3, middle_city3 = get_place(mm_lat2, mm_lng2)
        # middle_time_set.append(middle_move_time2)
        prefecture_set.append(prefecture)
        middle_city_set.append(middle_city)
        prefecture_set[0] = prefecture2
        middle_city_set[0] = middle_city2
        middle_city_lat_lng.append([middle_lat, middle_lng])
        middle_city_lat_lng[0] = [mm_lat, mm_lng]
        prefecture_set.append(prefecture3)
        middle_city_set.append(middle_city3)
        middle_city_lat_lng.append([mm_lat2, mm_lng2])
        middle_time_set.append(datetime.datetime.utcfromtimestamp(middle_move_time))
        middle_time_set[0] = datetime.datetime.utcfromtimestamp(middle_move_time)
        middle_time_set.append(datetime.datetime.utcfromtimestamp(middle_move_time4))

    middle_time = []
    if culc_time > 0:
        for i in range(len(middle_time_set)):
            middle_time.append(departure_time + datetime.timedelta(hours=middle_time_set[i].hour, minutes=middle_time_set[i].minute))
        # middle_time = departure_time + datetime.timedelta(hours=middle_move_time.hour, minutes=middle_move_time.minute)
    move_time = datetime.datetime.utcfromtimestamp(move_time)
    arrive_time = departure_time + datetime.timedelta(hours=move_time.hour, minutes=move_time.minute)
    #print(f'arrive_time = {arrive_time}')
    
    response_1 = []
    
    response = get_current_weather(city_name)
    if culc_time > 0:
        for i in range(len(middle_city_set)):
            response_1.append(get_current_weather(middle_city_set[i]))
    response_2 = get_current_weather(destination_name)
    
    #各地の天気予報の表示
    for i in range(40):
        date_time.append(response['list'][i]['dt_txt'])
        weather.append(response['list'][i]['weather'][0]['id']) 
        if culc_time > 0:
            date_time_1.append([response_1[j]['list'][i]['dt_txt'] for j in range(len(middle_city_set))])
            weather_1.append([response_1[j]['list'][i]['weather'][0]['id'] for j in range(len(middle_city_set))]) 
        date_time_2.append(response_2['list'][i]['dt_txt'])
        weather_2.append(response_2['list'][i]['weather'][0]['id'])         
        dec_time.append(datetime.datetime.strptime(date_time[i], '%Y-%m-%d %H:%M:%S') - departure_time)
        if culc_time > 0:
            dec_time_1.append([(datetime.datetime.strptime(date_time[i], '%Y-%m-%d %H:%M:%S') - middle_time[j]) for j in range(len(middle_time))])
        dec_time_2.append(datetime.datetime.strptime(date_time_2[i], '%Y-%m-%d %H:%M:%S') - arrive_time)
    #指定した時間に一番近い天気の表示を行う．
    for i in range(40):
        dec_time[i] = abs(dec_time[i])
        if culc_time > 0:
            for j in range(len(middle_time)):
                dec_time_1[i][j] = abs(dec_time_1[i][j])
        dec_time_2[i] = abs(dec_time_2[i])
        
    ans1_index = []
    
    ans_index = dec_time.index(min(dec_time))
    if culc_time > 0:
        for i in range(len(middle_time)):
            ans1_index.append(dec_time_1[i].index(min(dec_time_1[i])))
    ans2_index = dec_time_2.index(min(dec_time_2))
    
    jp1_weather = []
    icon_1 = []
    middle_icons = []
    
    jp_weather, icon = translate_weather(weather[ans_index])
    if culc_time > 0:
        for i in range(len(ans1_index)):
            jp1, icon_temp = translate_weather(weather_1[i][ans1_index[i]])
            icon_1.append(icon_temp)
            jp1_weather.append(jp1)
    jp2_weather, icon_2 = translate_weather(weather_2[ans2_index])
    
    departure_icon = [origin_lat, origin_lng, icon]
    if culc_time > 0:
        for i in range(len(icon_1)):
            middle_icons.append([*middle_city_lat_lng[i], icon_1[i]])
    destination_icon = [destination_lat, destination_lng, icon_2]
    
    path = 'weight:3%7Ccolor:0xff0000ff%7Cenc:' + directions['routes'][0]['overview_polyline']['points']
    
    #zoomの決定
    if distance < 5000:
        zoom = 11
    elif distance >= 5000 and distance < 10000:
        zoom = 11
    elif distance >= 10000 and distance < 100000:
        zoom = 10
    elif distance >= 100000 and distance < 200000:
        zoom = 10
    elif distance >=  200000 and distance < 300000:
        zoom = 7
    elif distance >=  300000 and distance < 500000:
        zoom = 7
    else:
        zoom = 6
    middle_index = int(len(middle_city_set)/2)
    # print(middle_index)
    url = f"{get_map_image(middle_city_set[middle_index], zoom, path, departure_icon, middle_icons, destination_icon)}"
  
    middle_texts = []
    
    departure_text = f"{city_name} の天気: {jp_weather}"
    if culc_time > 0:
        for i in range(len(prefecture_set)):
            middle_texts.append(f"{prefecture_set[i]},{middle_city_set[i]} の天気: {jp1_weather[i]}")
    destination_text = f"{destination_name} の天気: {jp2_weather}"
    
    return departure_text, middle_texts, destination_text, url
    

def main():
    
    # 都市を指定する。
    city_name = input("出発地を入力してください:")
    destination_name = input("目的地を入力してください:")
    pre_departure_time = input("出発時刻を入力してください(YYYY/MM/DD hh:mm):")
    departure_time = datetime.datetime.strptime(pre_departure_time, '%Y/%m/%d %H:%M')

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

    departure_text, middle_texts, destination_text, save_name = local_weather(city_name, destination_name, departure_time, travel_mode, avoid)
    
    print(departure_text)
    for middle_text in middle_texts:
        print(middle_text)
    print(destination_text)


if __name__ == "__main__":
    
    main()