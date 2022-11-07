from flask import Flask
import requests
import json

ua = {'User-Agent': 'Mozilla/5.0'}

app = Flask(__name__)

@app.route("/")
def index():
   return 'EOF'

@app.route("/lrc/<string:musicId>.lrc")
def getlrc(musicId):
   if (musicId == ''):
      return 'EOF'
   else:
      raw = requests.get('https://cloudmusic.mikan.fun/lyric?id=' + musicId, headers=ua)
      rc = raw.content.decode()
      jsonfile = json.loads(rc)
      result = jsonfile['lrc']['lyric']
      return result