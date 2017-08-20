from os import getenv

from flask import Flask, request, redirect, jsonify, send_file, Response
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.urls import url_quote

from requests import get
from magic import from_buffer
from PIL import Image

import s3

app = Flask(__name__, static_url_path='', static_folder='build')
app.wsgi_app = ProxyFix(app.wsgi_app)

LOGIN_API_KEY = getenv('LOGIN_API_KEY')
LOGIN_HOST = getenv('LOGIN_HOST')
HODIS = 'http://hodis.datasektionen.se'

def verify_token(token):
    payload = {'format': 'json', 'api_key': LOGIN_API_KEY}
    response = get('https://{}/verify/{}'.format(LOGIN_HOST, token), params=payload)
    if response.status_code == 200:
        return response.json()['user']
    else:
        return False

@app.route('/')
def index():
    user = verify_token(request.args.get('token'))
    if user:
        return app.send_static_file('index.html')
    else:
        return redirect('https://{}/login?callback={}?token='.format(LOGIN_HOST, url_quote(request.base_url)))


def path(user):     return '{}/{}/{}'.format(user[0], user[1], user)
def personal(path): return 'personal_images/{}'.format(path)
def original(path): return 'original_images/{}'.format(path)

@app.route('/me')
def me():
    user = verify_token(request.args.get('token'))
    return jsonify({
        'uid': user,
        'personal': s3.exists(personal(path(user)))
    })

missing = s3.get('missing.svg')['Body'].read()

@app.route('/user/<user>/image')
def user_image(user):
    if request.method == 'GET':
        if s3.exists(personal(path(user))):
            obj = s3.get(personal(path(user)))
            return send_file(obj['Body'], mimetype=obj['ContentType'])
        elif s3.exists(original(path(user))):
            obj = s3.get(original(path(user)))
            return send_file(obj['Body'], mimetype=obj['ContentType'])
        else:
            return Response(missing, content_type='image/svg')

    elif request.method == 'POST':
        image = request.files['file']
        mimetype = from_buffer(image.stream.read(1024, mime=True))
        return s3.put(personal(path(user)), image, mimetype)

    elif request.method == 'DELETE':
        return s3.delete(personal(path(user)))

@app.route('/user/<user>/image/<int:size>')
def user_image_resize(user, size):
    if s3.exists(personal(path(user))):
        tmp = s3.get(personal(path(user)))['Body']
        image = Image.open(tmp)
        image.thumbnail((size, size), Image.ANTIALIAS)
        tmp.seek(0)
        image.save(tmp, 'JPEG')
        tmp.seek(0)
        return tmp
    elif s3.exists(original(path(user))):
        return s3.get(original(path(user)))['Body']
    else:
        return missing

# Redirects to the old API
@app.route('/users/<query>')
def users(query):
    return redirect(HODIS + '/users/' + query)

@app.route('/ugkthid/<id>')
def ugkthid(id):
    return redirect(HODIS + '/ugkthid/' + id)

@app.route('/user/<user>')
def user(user):
    return redirect(HODIS + '/uid/' + user)

