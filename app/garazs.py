from flask import Flask, g
from flask_restful import Api, Resource, reqparse
import json
from datetime import datetime
from flask_httpauth import HTTPBasicAuth
from user import check_password, init_users_file

STATUS_JSON = './status.json'

init_users_file(force=False)

app = Flask(__name__)
api = Api(app)

auth = HTTPBasicAuth()

# @auth.get_password
# def get_password(username):
#     if username in USERS_PWS.keys():
#         g.username = username
#         return USERS_PWS[username]
#     return None

@auth.verify_password
def verify_password(username, password):
    if check_password(user=username, pwd=password):
        g.username = username
        return True
    else:
        return False

class controllerAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('desiredStatus', type=str, location='json')
        self.reqparse.add_argument('openCounter', type=int, location='json')
        self.reqparse.add_argument('state', type=str, location='json')
        super().__init__()

    def get(self, device):
        with open(STATUS_JSON, 'r') as status_json:
            status = json.load(status_json)
        return status[device]['desiredStatus']

    def put(self, device):
        # modify the desired status if the door was opened manually or gate action was triggered
        args = self.reqparse.parse_args()
        desiredStatus = args['desiredStatus']
        # openCounter = args['openCounter']
        with open(STATUS_JSON, 'r+') as status_json:
            status = json.load(status_json)
            status[device]['desiredStatus'] = desiredStatus
            # if device == 'door':
            #     status[device]['openCounter'] = openCounter
            status['lastChange']['user'] = g.username
            status['lastChange']['timeStamp'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            status['lastChange']['device'] = device
            status_json.seek(0)
            json.dump(status, status_json, indent=4)
            status_json.truncate()
        return 'recieved'

    def post(self, device):
        # update state of door if necessary
        if device == 'door' and g.username == 'controller':
            args = self.reqparse.parse_args()
            state = args['state']
            openCounter = args['openCounter']
            with open(STATUS_JSON, 'r+') as status_json:
                status = json.load(status_json)
                status[device]['openCounter'] = openCounter
                status[device]['state'] = state
                status_json.seek(0)
                json.dump(status, status_json, indent=4)
                status_json.truncate()
            return 'recieved'

class clientAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('desiredStatus', type=str, location='json')
        super().__init__()

    def get(self, device):
        # return the status of the device
        with open(STATUS_JSON, 'r') as status_json:
            status = json.load(status_json)
        return status[device]

    def put(self, device):
        args = self.reqparse.parse_args()
        desiredStatus = args['desiredStatus']
        with open(STATUS_JSON, 'r+') as status_json:
            status = json.load(status_json)
            status[device]['desiredStatus'] = desiredStatus
            status['lastChange']['user'] = g.username
            status['lastChange']['timeStamp'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            status['lastChange']['device'] = device
            status_json.seek(0)
            json.dump(status, status_json, indent=4)
            status_json.truncate()
        return {'Result': 'OK', 'user': g.username, 'Device': device}


api.add_resource(controllerAPI, '/controller/<string:device>')
api.add_resource(clientAPI, '/client/<string:device>')

# use only for development:

# if __name__ == '__main__':
#     app.run(debug=True, port=9090, host='0.0.0.0')