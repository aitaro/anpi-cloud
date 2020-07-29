import uuid
import flask
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

if os.environ.get('ENV') == "development":
    firebase_admin.initialize_app()
elif os.environ.get('ENV') == "production":
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
    'projectId': 'anpi-cloud-prod', # ここを環境によって変える
    })
else:    
    raise ValueError("set your environment to ENV (production)")
        
db = firestore.client()

def send_message(request):
    # preflight request時
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
        }
        return ('', 204, headers)

    request_args = request.get_json()
    print(request.get_json(), flush=True)

    JoinInfo = {
        "JoinInfo": "OK"
    }

    response = flask.jsonify(JoinInfo)
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Headers', "Origin, X-Requested-With, Content-Type, Accept")
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    return response