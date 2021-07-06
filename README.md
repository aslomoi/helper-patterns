# About

This repo contains basic examples to highlight helper container design patterns.

The patterns show are:

- Sidecar
- Ambassador

These patterns are shown against simulated applications. The purpose of each 'application' is to retrieve images of dogs from [Dog API]("https://dog.ceo/dog-api/"). The helper patterns are used to monitor the API requests and send a Slack notification upon an error.

# Usage

## Requirements

### Python dependencies

```
flask
requests
```

### Node.js dependencies

```
axios
winston
```

### Slack Webhook

Upon encountering an error, an HTTP POST request is made to a Slack Webhook.

Set up an Incoming Webhook using the [Slack API Documentation]("https://api.slack.com/messaging/webhooks").

Update `slack_url / SLACK_URL` variables in the code with the Webhook URL from the above documentation. NB: There are placeholder values `"<slack_webhook>"` which need to be replaced.

## Running

There are two main scripts, written in Python and Node.js, which simulate different applications. Run them respectively with:

```
python main.py
node main.js
```

Each of these main application contains an enum to simulate the different design patterns. Set the `Mode` to either `STANDALONE, SIDECAR or AMBASSADOR` to use that particular pattern.

The helper scripts should be run in another terminal window when using the corresponding mode:

```
python ambassador.py
or
python sidecar.py [ py.log | js.log ]
```
