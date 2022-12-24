from flask import Flask,abort
import requests
import json
import logging
logging.basicConfig(level=logging.INFO)

ua = {'User-Agent': 'Mozilla/5.0'}

app = Flask(__name__)

@app.route("/")
def index():
   json_data = {'status': 'ok'}
   return json_data

@app.route("/lrc/<string:musicId>.lrc")
def getlrc(musicId):
   if (musicId == ''):
      abort(500)
   else:
      try:
         raw = requests.get('https://cloudmusic.mikan.ac.cn/lyric?id=' + musicId, headers=ua)
         rc = raw.content.decode()
         jsonfile = json.loads(rc)
         result = jsonfile['lrc']['lyric']
      except Exception as e:
         logging.error(e)
         abort(500)
      except KeyError as e:
         logging.error(e)
         abort(500)
      else:
         logging.info('Successfully fetched lyric of '+musicId)
         return result
