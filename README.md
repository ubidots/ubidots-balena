# Ubidots BalenaBlock

**Work in progress...**

## Usage

Define `UBIDOTS_TOKEN` environment variable for your fleet/device with your
Ubidots account token.

Edit your `docker-compose.yml` to include the block conatiner and required networks and volumes:

```yml
version: '2'

services:
  
  ubidots-balena:
    build: ./ubidots-balena
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

Add `ubidots-mqtt` network to your application container and make it depends on the block container. e.g.:
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
    build: ./ubidots-balena
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
