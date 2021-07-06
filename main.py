import json
import logging
import requests
from enum import Enum, auto


class Mode(Enum):
    AMBASSADOR = auto()
    SIDECAR = auto()
    STANDALONE = auto()


MODE = Mode.STANDALONE
breed_url = "https://dog.ceo/api/breed/{}/images/random/{}"
random_url = "https://dog.ceo/api/dsfdsfdshjklfdshjafklasd"
slack_url = "<slack_webhook>"

dog_params = [("labrador", 3), ("chow", 2), ("shiba", 1), ("cat", 4), ("samoyed", 2)]

if MODE == Mode.STANDALONE:
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format=f"[%(asctime)s :: %(levelname)s] :: %(name)s :: %(message)s",
        handlers=[logging.StreamHandler()],
    )

    def get_dogs(url):
        resp = requests.get(url)
        result = resp.json()
        msg = f'{resp.status_code} - {resp.url} Message: {result["message"]}'
        if result["status"] == "success":
            logger.info(msg)
        else:
            logger.error(msg)
            headers = {"Content-type": "application/json"}
            text = ":rotating_light: Error detected :rotating_light:\n" + msg
            resp = requests.post(slack_url, json={"text": text}, headers=headers)
            logger.info(resp.text)

    logger.info("Starting the python app")

    for breed, no_img in dog_params:
        url = breed_url.format(breed, no_img)
        get_dogs(url)

    get_dogs(random_url)


elif MODE == Mode.SIDECAR:
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format=f"[%(asctime)s :: %(levelname)s] :: %(name)s :: %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler("py.log")],
    )

    def get_dogs(url):
        resp = requests.get(url)
        result = resp.json()
        msg = f'{resp.status_code} - {resp.url} Message: {result["message"]}'
        if result["status"] == "success":
            logger.info(msg)
        else:
            logger.error(msg)

    logger.info("Starting the python app")

    for breed, no_img in dog_params:
        url = breed_url.format(breed, no_img)
        get_dogs(url)

    get_dogs(random_url)
elif MODE == Mode.AMBASSADOR:
    for breed, no_img in dog_params:
        body = {"url": breed_url.format(breed, no_img)}
        resp = requests.post("http://localhost:5000/", json=body)
        print(resp.text)
    body = {"url": random_url}
    resp = requests.post("http://localhost:5000/", json=body)
    print(resp.text)
