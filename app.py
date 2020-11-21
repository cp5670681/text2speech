import json
import io

import requests
from flask import Flask, request
from wechatpy import parse_message
from wechatpy.replies import TextReply, VoiceReply
from flask_caching import Cache

cache = Cache()

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 1 * 60 * 60  # 默认过期时间 5分钟
cache.init_app(app)


with open('config.json', encoding='utf-8') as f:
    config = json.load(f)

@cache.cached(key_prefix='get_access_token')
def get_access_token():

    params = {
        'grant_type': 'client_credential',
        'appid': config['appid'],
        'secret': config['app_secret']
    }
    r = requests.get('https://api.weixin.qq.com/cgi-bin/token', params=params)
    access_token = r.json().get('access_token')
    return access_token

def upload(text):
    access_token = get_access_token()
    r = requests.get('http://tts.baidu.com/text2audio?lan=zh&ie=UTF-8&spd=5&text={}'.format(text))
    files = {
        'media': ('voice.mp3', io.BytesIO(r.content), 'application/audio/x-mpeg')
    }
    r2 = requests.post('https://api.weixin.qq.com/cgi-bin/media/upload?access_token={}&type=voice'.format(access_token), files=files)
    media_id = r2.json()['media_id']
    return media_id

upload('你好')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return request.args.get('echostr')
    xml = request.get_data().decode()
    print(xml)
    msg = parse_message(xml)
    if msg.type == 'text':
        media_id = upload(msg.content)
        reply = VoiceReply(media_id=media_id, message=msg)
        return reply.render()
    return ''


if __name__ == '__main__':
    app.run()
