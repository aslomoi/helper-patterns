import time
import sys
import re
import requests

SLACK_URL = "<slack_webhook>"


def follow(f):
    f.seek(0, 2)  # Go to the end of the file
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)  # Sleep briefly
            continue
        yield line


def slack_msg(msg):
    headers = {"Content-type": "application/json"}
    text = ":rotating_light: Error detected :rotating_light:\n" + msg
    resp = requests.post(SLACK_URL, json={"text": text}, headers=headers)
    print(resp.status_code)


if __name__ == "__main__":
    if len(args := sys.argv) == 2:
        filename = args[1]
    else:
        filename = "py.log"

    print(f"*** Listening to {filename} ***")
    with open(filename) as f:
        line = follow(f)
        for l in line:
            if re.search("error", l, re.IGNORECASE):
                print("**** ERROR detected ****")
                slack_msg(l)

            print(l)

