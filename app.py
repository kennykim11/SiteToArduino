import os

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

import iot_api_client as iot
from iot_api_client.rest import ApiException
from iot_api_client.configuration import Configuration

from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
THING_ID = os.environ['THING_ID']
PROPERTY_ID = os.environ['PROPERTY_ID']
DEVICE_ID = os.environ['DEVICE_ID']
HELP_URL = "https://github.com/kennykim11/SiteToArduino"

def get_token():
    oauth_client = BackendApplicationClient(client_id=CLIENT_ID)
    token_url = "https://api2.arduino.cc/iot/v1/clients/token"

    oauth = OAuth2Session(client=oauth_client)
    token = oauth.fetch_token(
        token_url=token_url,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        include_client_id=True,
        audience="https://api2.arduino.cc/iot",
    )
    return token

@app.route('/publish/', methods=['POST'])
@cross_origin()
def post_something():
    body = request.get_json()
    thing_id = body.get("thing_id") or THING_ID
    property_id = body.get("property_id") or PROPERTY_ID
    device_id = body.get("device_id") or DEVICE_ID
    value = body.get("value")

    if value:
        response_body = {"device_id": device_id, "value": value}

        try:
            client_config = Configuration(host="https://api2.arduino.cc/iot")
            client_config.access_token = get_token().get("access_token")
            client = iot.ApiClient(client_config)
            properties_api = iot.PropertiesV2Api(client)
            resp = properties_api.properties_v2_publish(thing_id, property_id, response_body)
        except ApiException as e:
            return jsonify({
                "ERROR": f"Exception when calling PropertiesV2Api->propertiesV2Publish: {e}"
            })
        return jsonify({
            "SUCCESS": ""
        })
    else:
        return jsonify({
            "ERROR": "No value given"
        })


@app.route('/')
def index():
    return f"""<h1>Look at the following docs for more information: {HELP_URL}"""

if __name__ == '__main__':
    app.run(threaded=True, port=5000)