const axios = require('axios');
const winston = require('winston');
const util = require('util');

let Mode = {
    'AMBASSADOR': 1,
    'SIDECAR': 2,
    'STANDALONE': 3
};
const MODE = Mode.STANDALONE;
let breed_url = "https://dog.ceo/api/breed/%s/images/random/%s";
let random_url = "https://dog.ceo/api/dsfdsfdshjklfdshjafklasd";
let slack_url = "<slack_webhook>";
let dog_params = [
    {"breed":"labrador", "no_img":3}, 
    {"breed":"chow", "no_img":2},
    {"breed":"shiba", "no_img":1},
    {"breed":"cat", "no_img":4},
    {"breed":"samoyed", "no_img":2}
];
if (MODE == Mode.STANDALONE) {
    const logger = winston.createLogger({
        level: 'info',
        format: winston.format.combine(
            winston.format.timestamp(),
            winston.format.json()
        ),
        transports: [
        new winston.transports.Console],
    });

    const get_dogs = url => {
        axios.get(url)
        .then(res => {
            logger.info(`${res.status} - ${res.config.url} Message: ${res.data.message}`);
        })
        .catch(err => {
            msg = `${err.response.status} error - ${err.response.config.url} Message: ${err.response.data.message}`;
            logger.error(msg);
            let body = { "text":  ":rotating_light: Error detected :rotating_light:\n" + msg};
            axios.post(slack_url, body)
            .then(res => {
                logger.info(res.data);
            })
            .catch(err => {
                logger.error(res.data);
            });
        });
    }

    logger.info("Starting the JS app")

    dog_params.forEach(dog => {
        let url = util.format(breed_url, dog.breed, dog.no_img);
        get_dogs(url);
    })

    get_dogs(random_url);
}
else if (MODE === Mode.SIDECAR) {
    const logger = winston.createLogger({
        level: 'info',
        format: winston.format.combine(
            winston.format.timestamp(),
            winston.format.json()
        ),
        transports: [
        new winston.transports.File({ filename: 'js.log'})    ],
    });

    const get_dogs = url => {
        axios.get(url)
        .then(res => {
            logger.info(`${res.status} - ${res.config.url} Message: ${res.data.message}`);
        })
        .catch(err => {
            logger.error(`${err.response.status} error - ${err.response.config.url} Message: ${err.response.data.message}`);
        });
    }

    logger.info("Starting the JS app")

    dog_params.forEach(dog => {
        let url = util.format(breed_url, dog.breed, dog.no_img);
        get_dogs(url);
    })

    get_dogs(random_url);
}
else if (MODE == Mode.AMBASSADOR) {
    dog_params.forEach(dog => {
        let body = { "url":  util.format(breed_url, dog.breed, dog.no_img)};
        axios.post("http://localhost:5000/", body)
        .then(res => {
            console.log(res.data.message);
        })
        .catch(err => {
            console.log(res.data.message);
        });
    });
    let body = { "url":  random_url};
    axios.post("http://localhost:5000/", body)
    .then(res => {
        console.log(res.data.message);
    })
    .catch(err => {
        console.log(res.data.message);
    });
}