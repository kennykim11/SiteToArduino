import os
from threading import Thread

from pprint import pprint

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

import iot_api_client as iot
from iot_api_client.rest import ApiException
from iot_api_client.configuration import Configuration

import discord
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
DISCORD_CHANNELS = ['test', 'help']

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

app.store = []

# def get_token():
#     oauth_client = BackendApplicationClient(client_id=CLIENT_ID)
#     token_url = "https://api2.arduino.cc/iot/v1/clients/token"
#
#     oauth = OAuth2Session(client=oauth_client)
#     token = oauth.fetch_token(
#         token_url=token_url,
#         client_id=CLIENT_ID,
#         client_secret=CLIENT_SECRET,
#         include_client_id=True,
#         audience="https://api2.arduino.cc/iot",
#     )
#     return token
#
# @app.route('/publish/', methods=['POST'])
# def post_something():
#     body = request.get_json(force=True) # Forced because no-cors JS fetch request requires text Content-Type header
#     thing_id = body.get("thing_id") or THING_ID
#     property_id = body.get("property_id") or PROPERTY_ID
#     device_id = body.get("device_id") or DEVICE_ID
#     value = body.get("value")
#
#     if value:
#         response_body = {"device_id": "Nope", "value": value}
#
#         try:
#             client_config = Configuration(host="https://api2.arduino.cc/iot")
#             client_config.access_token = get_token().get("access_token")
#             client = iot.ApiClient(client_config)
#             properties_api = iot.PropertiesV2Api(client)
#             devices_api = iot.DevicesV2Api(client)
#             resp = properties_api.properties_v2_publish(thing_id, property_id, response_body)
#         except ApiException as e:
#             return jsonify({
#                 "ERROR": f"Exception when calling PropertiesV2Api->propertiesV2Publish: {e}"
#             })
#         #resp = devices_api.devices_v2_update_properties(device_id, {"input": True, "properties": [{"name": "text", "type": "json", "value": value}]})
#         print(resp)
#         return jsonify({
#             "SUCCESS": ""
#         })
#     else:
#         return jsonify({
#             "ERROR": "No value given"
#         })

class DiscordClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.channel.name in DISCORD_CHANNELS:
            if message.content.startswith('!alert '):
                text = message.content[7:]
                app.store += [text]
                print(text)


@app.route('/push', methods=['POST'])
def push_string():
    body = request.get_data()
    if body:
        app.store += [body]
        return 'Success'
    else:
        return 'Fail'

@app.route('/pop', methods=['GET'])
def pop_string():
    if app.store:
        return app.store.pop(0)
    return ''


@app.route('/')
def index():
    return f"""<h1>Look at the following docs for more information: {HELP_URL}"""

if __name__ == '__main__':
    client = DiscordClient()
    #Thread(target=lambda: app.run(port=5000)).start()
    client.run(DISCORD_TOKEN)