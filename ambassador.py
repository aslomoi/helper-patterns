from flask import Flask, request
import requests
import json

SLACK_URL = "<slack_webhook>"

app = Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    data = request.get_json(force=True)
    resp = requests.get(data["url"])
    result = resp.json()
    if result["status"] == "success":
        print(result["message"])
    else:
        print("*** Error ***")
        msg = f'{resp.status_code}: {resp.url}\nMessage: {result["message"]}'
        print(msg)
        slack_msg(msg)
    return json.dumps(result)


def slack_msg(msg):
    headers = {"Content-type": "application/json"}
    text = ":rotating_light: Error detected :rotating_light:\n" + msg
    resp = requests.post(SLACK_URL, json={"text": text}, headers=headers)
    print(resp.status_code)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

