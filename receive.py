#!usr/bin/python
# -*- coding: utf-8 -*-

import cgi # CGIモジュールのインポート
import cgitb
import sys

cgitb.enable() # デバッグに使うので、本番環境では記述しない

form = cgi.FieldStorage() # フォームデータを取得する

print("Content-Type: text/html; charset=UTF-8") # HTMLを記述するためのヘッダ
print("")

# フォームのデータが入力されていない場合
if "text" not in form:
    print("<h1>Error!</h1>")
    print("<br>")
    print("テキストを入力してください！")
    print("<a href='/'><button type='submit'>戻る</button></a>")
    sys.exit()

text = form.getvalue("text") # データの値を取得する

print(text)