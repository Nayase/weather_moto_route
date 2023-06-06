"""
まず初めに，ルートを決定するプログラムを作る．
入力:(出発地) (到着地) 出力:(所要時間)
"""

import urllib.request, json
import urllib.parse
import datetime
from pprint import pprint

#Google Maps Platform Directions API endpoint
endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
api_key = 'YOUR_API_KEY'

#出発地、目的地を入力
# origin = input('出発地を入力: ').replace(' ','+')
# destination = input('目的地を入力: ').replace(' ','+')
origin = '仙台'
destination = '東京'

print(origin)
print(destination)

#UNIX時間の算出
#dep_time = input('出発時間を入力: yyyy/mm/dd hh:mm 形式 ')
dep_time = '2022/10/10 10:00'
dtime = datetime.datetime.strptime(dep_time, '%Y/%m/%d %H:%M')
unix_time = int(dtime.timestamp())
print(unix_time)

#移動手段決定
travel_mode_flag = input('移動手段: 1:drive,2:walk').replace(' ','+')

global travel_mode
if travel_mode_flag == "1":
    travel_mode = "driving"
elif travel_mode_flag == "2": 
    travel_mode = "walking"
else:
    print("error")
print("移動手段")
print(travel_mode)

if travel_mode == "driving":
    #高速使うか
    avoid_highway = input('高速を使いますか?: 1:使う 2:使わない').replace(' ','+')
    global avoid
    if avoid_highway == "1":
        avoid = "highways"
    elif avoid_highway == "2": 
        avoid = None
    else:
        print("error")
else:
    avoid = None
print(avoid)



nav_request = 'language=ja&origin={}&destination={}&avoid={}&mode={}&departure_time={}&key={}'.format(origin,destination,avoid,travel_mode,unix_time,api_key)
nav_request = urllib.parse.quote_plus(nav_request, safe='=&')
request = endpoint + nav_request

#Google Maps Platform Directions APIを実行
response = urllib.request.urlopen(request).read()

directions = json.loads(response)
#pprint(directions)
half_len = int(len(directions['routes'][0]['legs'][0]['steps'])/2)
print(directions['routes'][0]['legs'][0]['steps'][half_len-1]['end_location']['lat'])
#pprint(directions)


for key in directions['routes']:
    print("############")
    for key2 in key['legs']:
        print(key2['distance']['text'])
        #if travel_mode_flag == "1":
        print(key2['duration']['text'])
        #elif travel_mode_flag == "2":
        #    print(key2['duration_in_traffic']['text'])