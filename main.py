import os
from subprocess import Popen
from pprint import pprint

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

import iot_api_client as iot
from iot_api_client.rest import ApiException
from iot_api_client.configuration import Configuration


#Popen("secrets.bat", shell=True).wait()
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

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

# configure and instance the API client
client_config = Configuration(host="https://api2.arduino.cc/iot")
client_config.access_token = token.get("access_token")
client = iot.ApiClient(client_config)

# as an example, interact with the devices API
devices_api = iot.DevicesV2Api(client)

try:
    resp = devices_api.devices_v2_list()
    print(resp)
except ApiException as e:
    print("Got an exception: {}".format(e))


properties_api = iot.PropertiesV2Api(client)
id = "b46aeba2-d955-493f-8443-e0436fc0e28e"
pid = "941f19bd-1e18-4bd5-9160-30089aa19fc7"
value = {"device_id": "09ed2ad5-cd6b-4231-98c7-b1ee3c6c05bd", "value": "1234"}

try:
    resp = properties_api.properties_v2_publish_with_http_info(id, pid, value)
    print(resp)
except ApiException as e:
    print("Exception when calling PropertiesV2Api->propertiesV2Publish: %s\n" % e)