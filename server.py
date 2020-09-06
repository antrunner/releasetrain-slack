from flask import Flask, jsonify, request
from slack import WebClient
from slack.errors import SlackApiError
import os

client = WebClient(token=os.environ['RT_SLACK_API_TOKEN'])

app = Flask(__name__) 
 
@app.route('/', methods=["POST"]) 
def index():
	release= request.json["versionProductName"] 
	release+= " v" + request.json["versionNumber"]
	release+= "\n" + request.json["versionReleaseNotes"]
	try:
	    response = client.chat_postMessage(
	        channel='#general',
	        text=release)
	    #assert response["message"]["text"] == release
	except SlackApiError as e:
	    # You will get a SlackApiError if "ok" is False
	    assert e.response["ok"] is False
	    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
	    print("Got an error: {e.response['error']}")
	
	return "\nOK\n"

app.run(debug=False) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)