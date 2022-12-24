from flask import Flask,abort,send_file
import io,requests,json,logging
logging.basicConfig(level=logging.INFO)

ua = {'User-Agent': 'Mozilla/5.0'}

app = Flask(__name__)

@app.route("/")
def index():
   json_data = {'status': 'ok'}
   return json_data

@app.route("/lrc/<string:musicId>")
def getlrc(musicId):
   if (musicId == ''):
      abort(404)
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

@app.route("/lrc/<string:musicId>.lrc")
def getlrcfile(musicId):
   if (musicId == ''):
      abort(500)
   else:
      try:
         r = requests.get('https://cloudmusic.mikan.ac.cn/lrc/' + musicId, headers=ua)
      finally:
         if r.status_code == 200:
            Buffer = io.BytesIO()
            Buffer.write(r.content)
            Buffer.seek(0)
            return send_file(Buffer, attachment_filename=musicId + '.lrc', as_attachment=True)
         else:
            abort(r.status_code)
