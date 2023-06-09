# weather_moto_route
経路の天気を表示するウェブアプリのソースコードを載せます。

## 開発背景
私はバイクに乗って遠出するのが好きなのだが、バイクという乗り物は天候によって影響を受けやすいので、旅の経路上の天気というものは非常に興味のある事柄なのである。しかし、そのような道中の天気を表示してくれるサービスが表立ってあるわけではないことに気づき、自分で開発することを試みた。

## プログラムの概要
このプログラムは「目的地までの経路に沿った天気を教えてくれるウェブアプリ」である.入力は出発地，目的地，出発時刻，移動手段(車か徒歩)，高速道路利用の可否(移動手段 が車の場合のみ)である.この入力に従って，渡航距離が 10km 未満の場合は出発地と目的地 の 2 地点のみ，10km 以上 200km 未満であれば出発地，中間地点，目的地の 3 地点，200km 以上であれば出発地，第一，第二，第三中間地点，目的地の 5 地点の天気を出力する.
## 利用した Web サービスの情報
利用した Web サービスは Google の geocoding API, Directions API, Maps Static API である.
geocoding API は地名と緯度経度の値の変換を行い，Directions API は 2 地点の経路を導出し， 所要時間と距離を算出する.そして，Maps Static API で地図上に導出された経路と天気のア イコンを載せた地図を出力した.また， Open Weather Map の 5Day / 3Hour Forecast API を用 いて，これから 5 日間の 3 時間ごとの天気予報の情報を得ることができた.

## 実行例
<img width="886" alt="Screen Shot 2022-07-21 at 13 22 32" src="https://github.com/Nayase/weather_moto_route/assets/89143880/3f1640b9-86a7-4e46-9810-b56e0ace8463">

図 1:入力画面 1(出発地:仙台，目的地:東京，出発時刻:2022/7/21 15:24，交通手段:車，高速道 路:使わない)
<img width="708" alt="Screen Shot 2022-07-21 at 13 22 50" src="https://github.com/Nayase/weather_moto_route/assets/89143880/19e601e9-8042-4065-a75b-b862c9ab7d77">

図 2:出力画面 1(経路画像，出発地，中間地点(3 つ)，目的地の天気)
