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
    raise ValueError("set your environment to ENV (development, staging, production)")
        
db = firestore.client()

def sent_number(request):
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
    if not request_args['action']:
        raise ValueError("JSON is invalid, or missing a 'action' property")

    action = request_args['action']

    if action == "join":
        if not (request_args['roomId'] and request_args['userId'] and request_args['region']):
            raise ValueError("Need parameters: title, name, region'")

        room_id = request_args['roomId']
        user_id = request_args['userId']
        region = request_args['region']

        room = db.collection('rooms').document(room_id).get().to_dict()
        print(room, flush=True)

        if room.get("chimeMeetingId"):
            # meetingがすでに終了している場合はエラーになるので、違うIDで再発行する。
            try:
                meeting = client.get_meeting(
                    MeetingId=room["chimeMeetingId"]
                )
            except: 
                meeting = client.create_meeting(
                    MediaRegion=region,
                )
                db.collection('rooms').document(room_id).update({'chimeMeetingId': meeting['Meeting']['MeetingId']})
        else:
            meeting = client.create_meeting(
                MediaRegion=region,
            )
            db.collection('rooms').document(room_id).update({'chimeMeetingId': meeting['Meeting']['MeetingId']})

        print(meeting['Meeting'], flush=True)
            

        attendee = client.create_attendee(
            MeetingId=meeting['Meeting']['MeetingId'],
            ExternalUserId=user_id,
        )

        JoinInfo = {
            "JoinInfo": {
                "Meeting": meeting,
                "Attendee": attendee
            }
        }

        response = flask.jsonify(JoinInfo)
        response.headers.set('Access-Control-Allow-Origin', '*')
        response.headers.set('Access-Control-Allow-Headers', "Origin, X-Requested-With, Content-Type, Accept")
        response.headers.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    else:
        raise ValueError("action value is invalid")

    return response