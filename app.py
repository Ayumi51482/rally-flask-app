from oauth2client.service_account import ServiceAccountCredentials
import os
from oauth2client.service_account import ServiceAccountCredentials

# 環境変数から認証情報のパスを取得
json_keyfile = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

# 認証情報を設定
creds = ServiceAccountCredentials.from_json_keyfile_name(
    json_keyfile,
    ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
)

# Flaskアプリの作成
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

# 認証情報のセットアップ
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'rally-kf73-21a154fc2a7e.json',
    ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
)
client = gspread.authorize(creds)

## 送信画面のルーティング
@app.route('/')
def index():
     return render_template('index.html', current_time=current_time_jst)

##フォーム送信のルーティング
@app.route('/submit', methods=['POST'])
def submit():
    # 現在時刻を取得
    jst = pytz.timezone('Asia/Tokyo')
    current_day_jst = datetime.datetime.now(jst).strftime('%Y-%m-%d')
    current_time_jst = datetime.datetime.now(jst).strftime('%H:%M:%S')

    # フォームデータを取得
    selected_items = request.form.getlist('clear_count')  # 選択されたチェックボックスのリスト
    age_group = request.form.get('age_group')  # 年代

    # AAA, BBB, CCC の選択状態を確認して 1 or 0 に変換
    aaa = 1 if 'AAA' in selected_items else 0
    bbb = 1 if 'BBB' in selected_items else 0
    ccc = 1 if 'CCC' in selected_items else 0

    # スプレッドシートにデータを記録
    sheet.append_row([current_day_jst, current_time_jst, aaa, bbb, ccc, age_group])

    return redirect(url_for('index'))

## Flaskアプリ起動は不要、Renderが勝手に呼び出す
