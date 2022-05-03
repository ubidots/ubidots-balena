# Ubidots BalenaBlock

Send data to Ubidots from your Balena app.

## Table of Contents

1. [Add to your project](#add-to-your-project)
2. [Configuration](#configuration)
3. [Send data](#send-data)
    1. [Send data to device](#send-data-to-device)
    2. [Send data to variable](#send-data-to-variable)
4. [Receive data](#receive-data)
    1. [Receive variable last value](#receive-variable-last-value)
    2. [Receive variable last dot](#receive-variable-last-dot)
5. [Examples](#examples)

## Add to your project

Edit your `docker-compose.yml` to include the `ubidots-balena` block container along with its required network and volume:

```yml
version: '2'

services:
  
  ubidots-balena:
    image: bh.cr/sales6/ubidots
    networks:
      - ubidots-mqtt
    restart: always
    volumes:
      - ubidots-config:/ubidots/config

networks:
  ubidots-mqtt:

volumes:
  ubidots-config:
```

You can use a specific version of the `ubidots-balena` block by changing its `image` entry as follows:

```yml
    image: bh.cr/sales6/ubidots/x.y.z
```

Then, add `ubidots-mqtt` network to your application container and make it depends on the `ubidots-balena` block container. e.g.:

```yml
version: '2'

services:
  
  main:
    build: ./main
    depends_on:
      - ubidots-balena
    networks:
      - ubidots-mqtt
    restart: unless-stopped
  
  ubidots-balena:
    image: bh.cr/sales6/ubidots
    networks:
      - ubidots-mqtt
    restart: always
    volumes:
      - ubidots-config:/ubidots/config

networks:
  ubidots-mqtt:

volumes:
  ubidots-config:
```

## Configuration

The following environment variables are available for block configuration:

| Environment variable | Required? |   Default value    | Description |
|----------------------|-----------|--------------------|-------------|
| UBIDOTS_TOKEN        |    Yes    |        N/A         | Ubidots account [token][token] the block will be using to send data |
| UBIDOTS_DEVICE_LABEL |    No     | Balena device UUID | Ubidots API device [label][label] |

[label]: https://help.ubidots.com/en/articles/1330905-automatically-provision-devices-and-variables-with-ubidots-api-labels
[token]: https://help.ubidots.com/en/articles/590078-find-your-token-from-your-ubidots-account

## Send data

### Send data to device

Build message payload according to our [docs][pub_device_payload] then publish to `/` topic. For example:

```
payload = {
  "temperature": 27,
  "humidity": 55,
  "pressure": 78
}

mqtt.publish("/", payload)
```

[pub_device_payload]: https://docs.ubidots.com/v1.6/reference/publish-data-to-a-device#payload

### Send data to variable

Build message payload according to our [docs][pub_variable_payload] then publish to `<variable>` topic. For example, send data to `temperature` variable:

```
payload = {
  "value": 27
}

mqtt.publish("temperature", payload)
```

[pub_variable_payload]: https://docs.ubidots.com/v1.6/reference/publish-data-to-a-variable#payload


## Receive data

### Receive variable last value

Subscribe to `<variable>/lv` topic to receive just the last value of a variable. For example, get last value of `temperature` variable:

```
message_callback(message) {
  print("{message.topic}: {message.payload}")
}

mqtt.set_message_callback = message_callback
mqtt.subscribe("temperature/lv")

// When a message is received on variable topic, the callback will print:
// temperature: 27

```

### Receive variable last dot

Subscribe to `<variable>` topic to receive the last dot of a variable. For example, get last dot of `temperature` variable:

```
message_callback(message) {
  print("{message.topic}: {message.payload}")
}

mqtt.set_message_callback = message_callback
mqtt.subscribe("temperature")

// When a message is received on variable topic, the callback will print:
// temperature: {"value": 27, "timestamp": 1634311791000, "context": {}, "created_at": 1634311791000}

```

## Examples

You can find some sample projects in [examples](examples) folder that can give you a better idea of how to use this block in your app.
